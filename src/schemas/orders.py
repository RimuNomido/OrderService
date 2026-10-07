from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class CreateOrder(BaseModel):

    user_id: int
    product_id: int
    quantity: int = Field(gt=0)

class AddProduct(BaseModel):
    name: str
    price: Decimal = Field(gt=0)
    stock: int = Field(gt=0)

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int = Field(validation_alias='id')
    name: str
    price: Decimal
    stock: int

class ProductOrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int = Field(validation_alias='id')
    name: str

class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product: ProductOrderItemResponse
    quantity: int
    price: Decimal

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int = Field(validation_alias='id')
    status: str
    created_at: datetime
    items: list[OrderItemResponse] = Field(validation_alias='order_items')