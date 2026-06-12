from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Product
from app.schemas import ProductCreate,ProductUpdate

async def create_product(db: AsyncSession,product_in: ProductCreate) -> Product:
    db_product = Product(**product_in.model_dump())
    print(f"PRODUCT IN: {repr(product_in)}\n\n\n\n\nMake: {product_in.make}\n\n\n{product_in.model_dump()}")
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_product_by_id(db: AsyncSession, product_id: int) -> Product | None:
    result = await db.execute(select(Product).where(Product.id == product_id))
    print(result)
    return result.scalar_one_or_none()

async def get_products(db: AsyncSession):
    return select(Product)

async def update_product(db: AsyncSession, db_product: Product, product_in: ProductUpdate) -> Product:
    update_data = product_in.model_dump(exclude_unset=True)
    print(f"DB PRODUCT: {db_product}\n\n\n\n")
    print(update_data)

    for key, value in update_data.items():
        setattr(db_product, key, value)

    await db.commit()
    await db.refresh(db_product)
    return db_product

async def delete_product(db: AsyncSession, db_product: Product) -> None:
    await db.delete(db_product)
    await db.commit()