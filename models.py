from typing import List

from config_db import engine
from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    Table,
    String,
    Date
)
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
import enum

Base = declarative_base()
class DayEnum(enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

product_order = Table(
    "product_order",
    Base.metadata,
    Column("product_id", String, ForeignKey("products.name"), primary_key=True),
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("quantity", Integer, nullable=False),
)
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    products = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    name = Column(String, primary_key=True, index=True)
    description = Column(String)

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    orders = relationship(
        "Order",
        secondary=product_order,
        back_populates="products"
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    date = Column(Date, index=True)
    day = Column(Enum(DayEnum, name="day_enum"), index=True)

    products = relationship(
        "Product",
        secondary=product_order,
        back_populates="orders"
    )

    predictions = relationship(
        "Prediction",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True)
    result = Column(String)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    order = relationship(
        "Order",
        back_populates="predictions"
    )


Base.metadata.create_all(bind=engine)
