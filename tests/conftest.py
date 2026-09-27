import pytest
import pytest_asyncio
from sqlalchemy import select, delete

from src.db.session import AsyncSessionLocal
from src.models import Product, OrderItem


@pytest_asyncio.fixture()
async def mock_product_id():
    product = Product(
        name='Сухари',
        stock=1,
        price=29
    )
    async with AsyncSessionLocal() as session:
        session.add(product)
        await session.commit()

    yield product.id

    async with AsyncSessionLocal() as session:
        await session.execute(delete(OrderItem).where(OrderItem.product_id == product.id))
        await session.execute(delete(Product).where(Product.id == product.id))
        await session.commit()