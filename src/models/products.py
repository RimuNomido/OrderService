from typing import TYPE_CHECKING
from src.models import Base
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Numeric, DateTime, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.models import OrderItem

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=8, scale=2),
        CheckConstraint('price > 0', name='check_price_positive'),
        nullable=False
    )
    stock: Mapped[int] = mapped_column(
        CheckConstraint('stock >= 0', name='check_stock_positive'),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    order_items: Mapped[list['OrderItem']] = relationship(
        back_populates='product'
    )



