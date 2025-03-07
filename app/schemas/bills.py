from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.bill import BillStatus, ItemStatus, PaymentMethod


class BillItemBase(BaseModel):
    product_name: str = Field(..., description="商品名称")
    price: Decimal = Field(..., description="商品价格")
    quantity: Decimal = Field(..., description="商品数量")
    unit: str = Field(..., description="商品单位")
    purchase_time: datetime = Field(..., description="购买时间")
    buyer_name: str = Field(..., description="购买人姓名")
    remark: Optional[str] = Field(None, description="备注")


class BillItemCreate(BillItemBase):
    pass


class BillItemUpdate(BaseModel):
    payment_method: Optional[PaymentMethod] = Field(None, description="结算方式")
    settler_name: Optional[str] = Field(None, description="结算人姓名")
    settle_time: Optional[datetime] = Field(None, description="结算时间")
    remark: Optional[str] = Field(None, description="备注")
    bill_id: int
    item_ids: List[int]


class BillRefundBatch(BaseModel):
    bill_id: int = Field(..., description="账单ID")
    item_ids: List[int] = Field(..., description="要退款的商品ID列表")
    remark: Optional[str] = Field(None, description="退款原因")
    settler_name: Optional[str] = Field(None, description="结算人姓名")
    settle_time: Optional[datetime] = Field(None, description="结算时间")

class BillItemOut(BillItemBase):
    id: int
    status: ItemStatus
    payment_method: Optional[PaymentMethod]
    settler_name: Optional[str]
    amount: Decimal
    paid_amount: Decimal

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: str
        }


class BillBase(BaseModel):
    owner_id: int = Field(..., description="所属用户ID")
    remark: Optional[str] = Field(None, description="备注")


class BillCreate(BillBase):
    items: List[BillItemCreate] = Field(..., description="账单商品列表")


class BillUpdate(BaseModel):
    status: Optional[BillStatus] = Field(None, description="账单状态")
    remark: Optional[str] = Field(None, description="备注")


class BillOut(BillBase):
    id: int
    status: BillStatus
    total_amount: Decimal
    paid_amount: Decimal
    items: List[BillItemOut]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: str
        }


class BillAddItems(BaseModel):
    bill_id: int = Field(..., description="账单ID")
    items: List[BillItemCreate] = Field(..., description="要添加的商品列表")


class BillExportRequest(BaseModel):
    bill_id: int = Field(..., description="账单ID")
    export_time: datetime = Field(..., description="导出时间")


class BillItemRefund(BaseModel):
    item_id: int = Field(..., description="账单商品ID")
    bill_id: int = Field(..., description="账单ID")
    remark: Optional[str] = Field(None, description="退货原因")
    quantity: Decimal = Field(..., description="商品数量")
