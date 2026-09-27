import pytest
from httpx import ASGITransport, AsyncClient

from src.api.orders import app


@pytest.mark.asyncio
async def test_create_order():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url='http://test'
    ) as client:
        response = await client.post(
            "/orders/create",
            json={
                "user_id": 1,
                "product_id": 1,
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

        assert item['product']['product_id'] == 1
        assert item['quantity'] == 1
