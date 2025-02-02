import datetime
from decimal import Decimal
from typing import List

from tortoise.expressions import Q
from tortoise.transactions import atomic

from app.core.crud import CRUDBase
from app.models import User, Dept
from app.models.bill import Bill, BillItem, BillStatus, ItemStatus
from app.schemas.bills import BillCreate, BillUpdate, BillItemUpdate, BillItemCreate
from app.utils.exportBill import generate_pdf


class BillController(CRUDBase[Bill, BillCreate, BillUpdate]):
    def __init__(self):
        super().__init__(model=Bill)

    async def get_bill_list(self, owner_name: str = None, status: BillStatus = None, page: int = 1,
                            page_size: int = 10):
        q = Q()
        if owner_name:
            q &= Q(owner__username__contains=owner_name)
        if status:
            q &= Q(status=status)

        total = await self.model.filter(q).count()
        bills = await self.model.filter(q).prefetch_related('owner').offset((page - 1) * page_size).limit(page_size)
        result = []
        for bill in bills:
            bill_dict = {
                'id': bill.id,
                'owner_id': bill.owner_id,
                'owner_name': bill.owner.username,  # 使用关联的用户对象获取用户名
                'status': bill.status.value,
                'remark': bill.remark,
                'total_amount': str(bill.total_amount),
                'paid_amount': str(bill.paid_amount),
                'created_at': bill.created_at.isoformat(),
                'updated_at': bill.updated_at.isoformat(),
            }
            result.append(bill_dict)
        return {'data': result, 'total': total, 'page': page, 'page_size': page_size}

    async def get_bill_detail(self, bill_id: int):
        bill = await self.model.get(id=bill_id).prefetch_related('items')
        return {
            'id': bill.id,
            'owner_id': bill.owner_id,
            'status': bill.status.value,
            'remark': bill.remark,
            'total_amount': str(bill.total_amount),
            'paid_amount': str(bill.paid_amount),
            'created_at': bill.created_at.isoformat(),
            'updated_at': bill.updated_at.isoformat(),
            'items': [{
                'id': item.id,
                'product_name': item.product_name,
                'price': str(item.price),
                'quantity': str(item.quantity),
                'unit': item.unit,
                'purchase_time': item.purchase_time.isoformat(),
                'settle_time': item.settle_time.isoformat() if item.settle_time else None,
                'buyer_name': item.buyer_name,
                'status': item.status.value,
                'payment_method': item.payment_method.value if item.payment_method else None,
                'settler_name': item.settler_name,
                'amount': str(item.amount),
                'paid_amount': str(item.paid_amount),
                'remark': item.remark
            } for item in bill.items]
        }

    @atomic()
    async def create_bill(self, obj_in: BillCreate):
        # 计算账单总金额
        total_amount = Decimal('0')
        for item in obj_in.items:
            total_amount += item.price * item.quantity

        # 创建账单
        bill_data = obj_in.model_dump(exclude={'items'})
        bill_data['total_amount'] = total_amount
        bill_obj = await self.create(obj_in=bill_data)

        # 创建账单项目
        bill_items = []
        for item in obj_in.items:
            item_amount = item.price * item.quantity
            bill_items.append(
                BillItem(
                    bill=bill_obj,
                    amount=item_amount,
                    **item.model_dump()
                )
            )
        await BillItem.bulk_create(bill_items)
        return bill_obj

    @atomic()
    async def settle_bill_items(self, bill_id: int, item_ids: List[int], update_data: BillItemUpdate):
        # 获取账单和需要结算的商品
        bill = await self.get(id=bill_id)
        items = await BillItem.filter(bill_id=bill_id, id__in=item_ids)

        # 更新商品状态和支付信息
        for item in items:
            item.status = ItemStatus.PAID
            if update_data.payment_method:
                item.payment_method = update_data.payment_method
            if update_data.settler_name:
                item.settler_name = update_data.settler_name
            if update_data.settle_time:
                item.settle_time = update_data.settle_time
            if update_data.remark:
                item.remark = update_data.remark
            item.paid_amount = item.amount
            await item.save()

        # 更新账单状态和已支付金额
        bill_items = await BillItem.filter(bill_id=bill_id)
        total_amount = sum(item.amount for item in bill_items if item.status != ItemStatus.REFUNDED)
        paid_amount = sum(item.paid_amount for item in bill_items if item.status == ItemStatus.PAID)

        bill.total_amount = total_amount
        bill.paid_amount = paid_amount
        if bill.paid_amount >= bill.total_amount:
            bill.status = BillStatus.PAID
        await bill.save()

    @atomic()
    async def refund_bill_items(self, bill_id: int, item_ids: List[int]):
        # 获取账单和需要退款的商品
        bill = await self.get(id=bill_id)
        items = await BillItem.filter(bill_id=bill_id, id__in=item_ids)

        # 更新商品状态为已退款
        for item in items:
            if item.status == ItemStatus.PAID:
                item.status = ItemStatus.REFUNDED
                item.paid_amount = 0
                await item.save()

        # 更新账单状态和已支付金额
        bill_items = await BillItem.filter(bill_id=bill_id)
        total_amount = sum(item.amount for item in bill_items if item.status != ItemStatus.REFUNDED)
        paid_amount = sum(item.paid_amount for item in bill_items if item.status == ItemStatus.PAID)

        bill.total_amount = total_amount
        bill.paid_amount = paid_amount
        if bill.paid_amount < bill.total_amount:
            bill.status = BillStatus.UNPAID
        await bill.save()

    @atomic()
    async def add_bill_items(self, bill_id: int, items: List[BillItemCreate]):
        # 获取账单
        bill = await self.get(id=bill_id)

        # 计算新增商品的总金额
        total_amount = Decimal('0')
        for item in items:
            total_amount += item.price * item.quantity

        # 创建账单项目
        bill_items = []
        for item in items:
            item_amount = item.price * item.quantity
            bill_items.append(
                BillItem(
                    bill=bill,
                    amount=item_amount,
                    **item.model_dump()
                )
            )
        await BillItem.bulk_create(bill_items)

        # 更新账单总金额
        bill.total_amount += total_amount
        bill.status = BillStatus.UNPAID
        await bill.save()
        return bill

    async def export_bill(self, bill_id: int, export_time: datetime):
        bill_obj = await self.get_bill_detail(bill_id)
        owner = await User.get(id=bill_obj['owner_id'])
        dept = await Dept.get(id=owner.dept_id)
        # 构建导出信息
        export_info = {
            'owner_name': owner.username,
            'owner_phone': owner.phone,
            'owner_email': owner.email,
            'owner_alias': owner.alias,
            'owner_dept': dept.name,
            'status': bill_obj['status'],
            'total_amount': bill_obj['total_amount'],
            'paid_amount': bill_obj['paid_amount'],
            'created_at': bill_obj['created_at'],
            'items': bill_obj['items'],
            'remark': bill_obj['remark'],
            'export_time': export_time
        }
        file_name = f"{bill_id}_{owner.username}_{export_time}.pdf"
        generate_pdf(export_info, file_name)

        return file_name


bill_controller = BillController()
