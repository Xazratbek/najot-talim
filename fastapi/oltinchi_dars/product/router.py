from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
import product.crud as crud
import product.schema as schema

router = APIRouter(prefix='/product', tags=['Product'])


@router.post('/', response_model=schema.ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product_router(data: schema.CreateProductSchema, session: AsyncSession = Depends(get_db)):
    return await crud.create_product(session, data)


@router.get('/', response_model=list[schema.ProductSchema])
async def list_product_router(search: str = None, in_stock: bool = None, session: AsyncSession = Depends(get_db)):
    return await crud.product_list(session, search, in_stock)


@router.get('/{product_id}', response_model=schema.ProductSchema)
async def detail_product_router(product_id: int, session: AsyncSession = Depends(get_db)):
    return await crud.product_detail(session, product_id)


@router.patch('/{product_id}', response_model=schema.ProductSchema)
async def update_product_router(product_id: int, data: schema.UpdateProductSchema, session: AsyncSession = Depends(get_db)):
    return await crud.update_product(session, data, product_id)


@router.delete('/{product_id}')
async def delete_product_router(product_id: int, session: AsyncSession = Depends(get_db)):
    return await crud.delete_product(session, product_id)
