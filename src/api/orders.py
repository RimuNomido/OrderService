from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.orders import CreateOrder, OrderResponse, ProductResponse
from src.db.session import get_db
from src.services import order_service
from src.exceptions.order import UserNotFound, ProductNotFound, InsufficientStock, OrderNotFound

app = FastAPI()

@app.exception_handler(UserNotFound)
async def user_not_found_handler(
        request: Request,
        exc: UserNotFound,
):
    return JSONResponse(
        status_code=404,
        content={'detail': str(exc)},
    )

@app.exception_handler(ProductNotFound)
async def product_not_found_handler(
        request: Request,
        exc: ProductNotFound,
):
    return JSONResponse(
        status_code=404,
        content={'detail': str(exc)},
    )

@app.exception_handler(InsufficientStock)
async def insufficient_stock_handler(
        request: Request,
        exc: InsufficientStock,
):
    return JSONResponse(
        status_code=409,
        content={'detail': str(exc)}
    )

@app.exception_handler(OrderNotFound)
async def order_not_found_handler(
        request: Request,
        exc: OrderNotFound,
):
    return JSONResponse(
        status_code=404,
        content={'detail': str(exc)},
    )

@app.post('/orders/create', status_code=201)
async def create_order(order_data: CreateOrder, session:AsyncSession = Depends(get_db)):
    async with session.begin():
        order = await order_service.create_order(
            session,
            order_data.user_id,
            order_data.product_id,
            order_data.quantity
    )
    return {'order_id': order.id}

@app.get('/orders/{order_id}', status_code=200, response_model=OrderResponse)
async def get_order(
        order_id: int,
        session: AsyncSession = Depends(get_db)
):
    return await order_service.get_order(session, order_id)

@app.get('/users/{user_id}/orders', status_code=200, response_model=list[OrderResponse])
async def get_user_orders(
        user_id: int,
        session: AsyncSession = Depends(get_db)
):
    orders = await order_service.get_user_orders(session, user_id)
    return orders

@app.get('/products/{product_id}', status_code=200, response_model=ProductResponse)
async def get_product(
        product_id: int,
        session: AsyncSession = Depends(get_db)):
    return await order_service.get_product(session, product_id)
