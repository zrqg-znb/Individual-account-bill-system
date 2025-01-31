from tortoise import fields
from enum import Enum

from .base import BaseModel, TimestampMixin


class BillStatus(str, Enum):
    UNPAID = "unpaid"  # 未结清
    PAID = "paid"  # 已结清


class ItemStatus(str, Enum):
    UNPAID = "unpaid"  # 欠款
    PAID = "paid"  # 结清
    REFUNDED = "refunded"  # 退款


class PaymentMethod(str, Enum):
    CASH = "cash"  # 现金
    ALIPAY = "alipay"  # 支付宝
    WECHAT = "wechat"  # 微信
    CREDIT = "credit"  # 记账


class Bill(BaseModel, TimestampMixin):
    owner = fields.ForeignKeyField('models.User', related_name='bills', description="所属用户", index=True)
    status = fields.CharEnumField(BillStatus, default=BillStatus.UNPAID, description="账单状态", index=True)
    remark = fields.TextField(null=True, description="备注")
    total_amount = fields.DecimalField(max_digits=10, decimal_places=2, description="总金额")
    paid_amount = fields.DecimalField(max_digits=10, decimal_places=2, default=0, description="已支付金额")

    class Meta:
        table = "bill"


class BillItem(BaseModel, TimestampMixin):
    bill = fields.ForeignKeyField('models.Bill', related_name='items', description="所属账单")
    product_name = fields.CharField(max_length=100, description="商品名称", index=True)
    price = fields.DecimalField(max_digits=10, decimal_places=2, description="商品价格")
    quantity = fields.DecimalField(max_digits=10, decimal_places=2, description="商品数量")
    unit = fields.CharField(max_length=20, description="商品单位")
    purchase_time = fields.DatetimeField(description="购买时间", index=True)
    buyer_name = fields.CharField(max_length=50, description="购买人姓名", index=True)
    status = fields.CharEnumField(ItemStatus, default=ItemStatus.UNPAID, description="商品状态", index=True)
    payment_method = fields.CharEnumField(PaymentMethod, default=PaymentMethod.CREDIT, description="结算方式")
    settler_name = fields.CharField(max_length=50, null=True, description="结算人姓名", index=True)
    remark = fields.TextField(null=True, description="备注")
    amount = fields.DecimalField(max_digits=10, decimal_places=2, description="商品总金额")
    paid_amount = fields.DecimalField(max_digits=10, decimal_places=2, default=0, description="已支付金额")

    class Meta:
        table = "bill_item"