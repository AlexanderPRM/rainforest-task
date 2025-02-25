"""Module with SQLAlchemy models."""

import decimal
import uuid

import sqlalchemy as sa
from config import RelationalDatabaseSettings
from domain.order.dto import OrderStatus
from infrastructure.mixins import IDMixin, TimestampMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

metadata = sa.MetaData(schema=RelationalDatabaseSettings().SCHEMA)


class Base(DeclarativeBase):
    """Base Declarative class for SQLAlchemy models."""

    metadata = metadata


class Order(IDMixin, TimestampMixin, Base):
    """Order model.

    Args:
        IDMixin (class): UUID ID Mixin.
        TimestampMixin (class): TimeStamp Mixin.
        Base (class): Base Declarative class.

    """

    __tablename__ = 'order'

    status: Mapped[OrderStatus] = mapped_column(sa.Enum(OrderStatus))

    order_items: Mapped[list['OrderItems']] = relationship(
        'OrderItems',
        back_populates='order',
        cascade='all, delete-orphan',
    )


class Product(IDMixin, TimestampMixin, Base):
    """Product model.

    Args:
        IDMixin (class): UUID ID Mixin.
        TimestampMixin (class): TimeStamp Mixin.
        Base (class): Base Declarative class.

    """

    __tablename__ = 'product'

    name: Mapped[str] = mapped_column(sa.String(24), unique=True)
    description: Mapped[str] = mapped_column(sa.Text, nullable=True)
    price: Mapped[decimal.Decimal] = mapped_column(sa.DECIMAL(10, 2))
    cost: Mapped[decimal.Decimal] = mapped_column(sa.DECIMAL(10, 2))
    stock: Mapped[int]

    order_items: Mapped[list['OrderItems']] = relationship(
        'OrderItems',
        back_populates='product',
        cascade='all, delete-orphan',
    )


class OrderItems(IDMixin, TimestampMixin, Base):
    """OrderItems model.

    Args:
        IDMixin (class): UUID ID Mixin.
        TimestampMixin (class): TimeStamp Mixin.
        Base (class): Base Declarative class.

    """

    __tablename__ = 'order_items'

    order_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('order.id', ondelete='CASCADE'))
    product_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('product.id', ondelete='CASCADE'))
    quantity: Mapped[int]
    price: Mapped[decimal.Decimal] = mapped_column(sa.DECIMAL(10, 2))
    cost: Mapped[decimal.Decimal] = mapped_column(sa.DECIMAL(10, 2))

    order: Mapped['Order'] = relationship('Order', back_populates='order_items')
    product: Mapped['Product'] = relationship('Product', back_populates='order_items')
