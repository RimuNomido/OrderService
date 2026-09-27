from sqlalchemy import ForeignKey, CheckConstraint, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import Base
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import Order
    from src.models import Product

class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id'),
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id')
    )
    quantity: Mapped[int] = mapped_column(
        CheckConstraint('quantity > 0', name='check_positive_quantity'),
        nullable=False
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=8, scale=2),
        nullable=False
    )

    order: Mapped['Order'] = relationship(
        back_populates='order_items'
    )
    product: Mapped['Product'] = relationship(
        back_populates='order_items'
    )

    __table_args__ = (UniqueConstraint('order_id', 'product_id', name="uq_product_order"), {'extend_existing': True},)