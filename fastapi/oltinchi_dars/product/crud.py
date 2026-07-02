from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from product.models import Product
from product.schema import CreateProductSchema, UpdateProductSchema


async def get_product_or_404(session: AsyncSession, product_id: int) -> Product:
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    return product


async def create_product(session: AsyncSession, data: CreateProductSchema):
    product = Product(**data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)

    return product


async def product_list(session: AsyncSession, search: str = None, in_stock: bool = None):
    query = select(Product)

    if search:
        query = query.where(Product.name.ilike(f'%{search}%'))

    if in_stock is not None:
        query = query.where(Product.in_stock == in_stock)

    query = query.order_by(Product.id.desc())

    result = await session.execute(query)
    return result.scalars().all()


async def product_detail(session: AsyncSession, product_id: int):
    return await get_product_or_404(session, product_id)


async def update_product(session: AsyncSession, data: UpdateProductSchema, product_id: int):
    product = await get_product_or_404(session, product_id)

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    await session.commit()
    await session.refresh(product)

    return product


async def delete_product(session: AsyncSession, product_id: int):
    product = await get_product_or_404(session, product_id)

    await session.delete(product)
    await session.commit()

    return {'message': 'Product deleted'}
