from fastapi import APIRouter, Query
from typing import List

from app.controllers.bill import bill_controller
from app.models.bill import BillStatus
from app.schemas import Success
from app.schemas.bills import BillCreate, BillUpdate, BillItemUpdate, BillAddItems, BillExportRequest, BillRefundBatch, \
    BillItemRefund

router = APIRouter()


@router.get("/list", summary="查看账单列表")
async def list_bills(
        owner_name: str = Query(None, description="所属用户名称"),
        status: BillStatus = Query(None, description="账单状态"),
        page: int = Query(1, description="页码", ge=1),
        page_size: int = Query(10, description="每页数量", ge=1, le=100)
):
    result = await bill_controller.get_bill_list(owner_name, status, page, page_size)
    return Success(data=result['data'], total=result['total'], msg="获取成功", page=result['page'],
                   page_size=result['page_size'])


@router.get("/get", summary="查看账单详情")
async def get_bill(
        bill_id: int = Query(..., description="账单ID"),
):
    result = await bill_controller.get_bill_detail(bill_id)
    return Success(data=result)


@router.post("/create", summary="创建账单")
async def create_bill(
        bill_in: BillCreate,
):
    await bill_controller.create_bill(obj_in=bill_in)
    return Success(msg="创建成功")


@router.post("/update", summary="更新账单")
async def update_bill(
        bill_in: BillUpdate,
):
    await bill_controller.update(obj_in=bill_in)
    return Success(msg="更新成功")


@router.delete("/delete", summary="删除账单")
async def delete_bill(
        bill_id: int = Query(..., description="账单ID"),
):
    await bill_controller.delete(id=bill_id)
    return Success(msg="删除成功")


@router.post("/settleBatch", summary="结算商品")
async def settle_bill_batch(
        update_data: BillItemUpdate
):
    await bill_controller.settle_bill_items(update_data.bill_id, update_data.item_ids, update_data)
    return Success(msg="结算成功")


@router.post("/refundItem", summary="账单商品退货")
async def refund_bill_item(
        refund_data: BillItemRefund
):
    await bill_controller.refund_bill_item(refund_data)
    return Success(msg="退货成功")


@router.post("/refundBatch", summary="批量退款账单商品")
async def refund_bill_items_batch(
        refund_data: BillRefundBatch
):
    await bill_controller.refund_bill_items(refund_data.bill_id, refund_data.item_ids, refund_data)
    return Success(msg="退款成功")


@router.post("/addItems", summary="添加账单商品")
async def add_bill_items(
        bill_in: BillAddItems,
):
    await bill_controller.add_bill_items(bill_in.bill_id, bill_in.items)
    return Success(msg="添加成功")


@router.post("/export", summary="导出账单")
async def export_bill(
        export_request: BillExportRequest,
):
    result = await bill_controller.export_bill(export_request.bill_id, export_request.export_time)
    return Success(data=result)
