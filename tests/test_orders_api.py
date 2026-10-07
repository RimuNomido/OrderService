from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.orders import app


@pytest.mark.asyncio
async def test_create_order(order_test_data):
    product_id = order_test_data['product_id']
    user_id = order_test_data['user_id']

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url='http://test'
    ) as client:
        response = await client.post(
            "/orders/create",
            json={
                "user_id": user_id,
                "product_id": product_id,
                "quantity": 1,
            }
        )

        assert response.status_code == 201

        data = response.json()

        assert 'order_id' in data
        assert isinstance(data['order_id'], int)

        order_id = data['order_id']

        get_response = await client.get(f"/orders/{order_id}")

        assert get_response.status_code == 200

        order = get_response.json()

        assert order['order_id'] == order_id
        assert order['status'] == 'accepted'
        assert len(order['items']) == 1

        item = order['items'][0]

        assert item['product']['product_id'] == product_id
        assert item['quantity'] == 1
