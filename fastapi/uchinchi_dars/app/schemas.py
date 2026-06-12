from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict,Field

class ProductBase(BaseModel):
    make: str = Field(...,min_length=3,max_length=100,description="Mashina nomi")
    price: Decimal = Field(...,gt=0,description="Mahsulot narxi 0 dan katta bo'lishi shart")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    make: str | None = Field(None,min_length=3,max_length=100)
    price: Decimal | None = Field(None,gt=0)

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
