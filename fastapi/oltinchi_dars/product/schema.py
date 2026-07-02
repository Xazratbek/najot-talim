from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class CreateProductSchema(BaseModel):
    name: str = Field(max_length=120)
    desc: Optional[str] = None
    price: Decimal
    in_stock: Optional[bool] = None

    class Config:
        from_attributes = True


class UpdateProductSchema(BaseModel):
    name: Optional[str] = Field(default=None, max_length=120)
    desc: Optional[str] = None
    price: Optional[Decimal] = None
    in_stock: Optional[bool] = None

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    id: int
    name: str
    desc: Optional[str]
    price: Decimal
    in_stock: bool

    class Config:
        from_attributes = True
