from decimal import Decimal

import pytest_asyncio
from sqlalchemy import delete, select
from uuid import uuid4
from src.db.session import AsyncSessionLocal
from src.models import Product, OrderItem, User, Order


@pytest_asyncio.fixture()
async def mock_product_id():
    product = Product(
        name=f'Сухари-{uuid4()}',
        stock=1,
        price=Decimal(29)
    )
    async with AsyncSessionLocal() as session:
        session.add(product)
        await session.commit()
        product_id = product.id

    yield product_id

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(OrderItem.order_id).where(OrderItem.product_id == product_id))
        order_id = result.scalar_one_or_none()
        await session.execute(delete(OrderItem).where(OrderItem.product_id == product_id))
        if order_id is not None:
            await session.execute(delete(Order).where(Order.id == order_id))
        await session.execute(delete(Product).where(Product.id == product_id))
        await session.commit()

@pytest_asyncio.fixture
async def order_test_data():
    async with AsyncSessionLocal() as session:
        user = User(
            username='test',
            email=f'test-{uuid4()}@test.org'
        )
        product = Product(
            name=f'Баклажан-{uuid4()}',
            price=Decimal('99.99'),
            stock=30
        )

        session.add_all([user, product])
        await session.commit()
        user_id = user.id
        product_id = product.id

    yield {
        'user_id': user_id,
        'product_id': product_id
    }

    async with AsyncSessionLocal() as session:
        await session.execute(delete(OrderItem).where(OrderItem.product_id == product_id))
        await session.execute(delete(Order).where(Order.user_id == user_id))
        await session.execute(delete(Product).where(Product.id == product_id))
        await session.execute(delete(User).where(User.id == user_id))

        await session.commit()