import asyncio
import pytest

from src.db.session import AsyncSessionLocal
from src.exceptions.order import InsufficientStock
from src.models import Order, Product
from src.services.order_service import create_order

async def make_order(session, mock_product_id):
    async with session.begin():
        return await create_order(
            session,
            1,
            mock_product_id,
            1,
        )

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