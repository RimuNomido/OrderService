import asyncio
import uuid
from decimal import Decimal

import pytest
from src.db.session import AsyncSessionLocal
from src.exceptions.order import InsufficientStock
from src.exceptions.product import ProductAlreadyExists
from src.models import Order, Product
from src.services.order_service import create_order, add_product

async def make_order(session, mock_product_id):
    async with session.begin():
        return await create_order(
            session,
            1,
            mock_product_id,
            1,
        )

async def make_product(session, name, price, stock):
    async with session.begin():
        return await add_product(session, name, price, stock)

@pytest.mark.asyncio
async def test_concurrent_orders(mock_product_id):
    async with AsyncSessionLocal() as session_a:
        async with AsyncSessionLocal() as session_b:
            results = await asyncio.gather(
                make_order(session_a, mock_product_id),
                make_order(session_b, mock_product_id),
                return_exceptions=True
            )

    assert any(isinstance(result, Order) for result in results)
    assert any(isinstance(result, InsufficientStock) for result in results)

    async with AsyncSessionLocal() as session:
        product = await session.get(Product, mock_product_id)
        stock = product.stock

    assert stock == 0


@pytest.mark.asyncio
async def test_add_product():
    async with AsyncSessionLocal() as session_a:
        async with AsyncSessionLocal() as session_b:
            name = f'Молоко-{uuid.uuid4()}'
            price = Decimal('99.99')
            stock = 1
            results = await asyncio.gather(
                make_product(session_a, name, price, stock),
                make_product(session_b, name, price, stock),
                return_exceptions=True
            )

    assert sum(isinstance(result, Product) for result in results) == 1
    assert sum(isinstance(result, ProductAlreadyExists) for result in results) == 1

    for result in results:
        if isinstance(result, Product):
            async with AsyncSessionLocal() as session:
                await session.delete(result)
                await session.commit()