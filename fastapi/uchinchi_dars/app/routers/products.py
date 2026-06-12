from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import *
from app.schemas import *
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as async_paginate

router = APIRouter(prefix="/products",tags=["Products"])

@router.post("",response_model=ProductResponse,status_code=status.HTTP_201_CREATED)
async def create_new_product(product_in: ProductCreate,db: AsyncSession = Depends(get_db)):
    return await create_product(db=db,product_in=product_in)

@router.get("",response_model=Page[ProductResponse], status_code=status.HTTP_200_OK)
async def read_products(db: AsyncSession = Depends(get_db)):
    query = await get_products(db=db)
    return await async_paginate(db,query)

@router.patch("/{product_id}",response_model=ProductUpdate,status_code=status.HTTP_200_OK)
async def update_existing_product(product_id: int, product_in: ProductUpdate, db: AsyncSession = Depends(get_db)):
    db_product = await get_product_by_id(product_id,db)
    if not db_product:
        raise HTTPException (status_code=404,detail="Mahsulot topilmadi")

    return await update_product(db,db_product,product_in)

@router.delete("/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_product(product_id: int, db: AsyncSession = Depends(get_db)):
    db_product = await get_product_by_id(db,product_id)
    if not db_product:
        raise HTTPException(status_code=404,detail="Mahsulot topilmadi")
    await delete_product(db,product_id)
    return None
