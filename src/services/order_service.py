from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.exceptions.order import UserNotFound, ProductNotFound, InsufficientStock, OrderNotFound
from src.models import User, Product, Order, OrderItem

async def create_order(session: AsyncSession, user_id: int, product_id: int, quantity: int):
    user = await session.get(User, user_id)
    if not user:
        raise UserNotFound("Пользователя с таким id не существует!")
    product = await session.scalar(select(Product).where(Product.id == product_id).with_for_update())
    if not product:
        raise ProductNotFound("Продукта с таким id не существует!")
    if product.stock < quantity:
        raise InsufficientStock("Недостаточно товаров на складе!")

    order = Order(
        user=user,
        status='accepted',
    )
    session.add(order)
    order_item = OrderItem(
        order=order,
        product=product,
        quantity=quantity,
        price=product.price,
    )
    session.add(order_item)
    product.stock -= order_item.quantity
    await session.flush()
    return order

async def get_order(session: AsyncSession, order_id: int) -> Order:
    stmt = (select(Order)
    .where(Order.id == order_id)
    .options(
        selectinload(Order.order_items)
        .selectinload(OrderItem.product)
    )
    )
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    if order:
        return order
    else:
        raise OrderNotFound("Заказа с таким id не существует!")

async def get_user_orders(session: AsyncSession, user_id: int) -> list[Order]:
    result = await session.execute(
        select(Order)
        .where(Order.user_id == user_id).options(
        selectinload(Order.order_items)
        .selectinload(OrderItem.product)
        )
    )

    return list(result.scalars().all())

async def get_product(session: AsyncSession, product_id: int) -> Product:
    product = await session.get(Product, product_id)
    if product:
        return product
    else:
        raise ProductNotFound("Продукта с таким id не существует!")