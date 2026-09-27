from datetime import datetime
from src.models import Base
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.models import User
    from src.models import OrderItem

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id')
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    user: Mapped['User'] = relationship(
        back_populates='orders'
    )

    order_items: Mapped[list['OrderItem']] = relationship(
        back_populates='order'
    )