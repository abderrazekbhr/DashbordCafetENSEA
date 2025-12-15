from config_db import engine
from sqlalchemy import Column, Enum, ForeignKey, ForeignKey , Integer,  Table, String,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
import enum

Base = declarative_base()
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
product_order = Table(
    'product_order',
    Base.metadata,
    Column('product_id', String, ForeignKey('products.name')),
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('quantity', Integer)
    
)
    
class Product(Base):
    __tablename__ = "products"
    
    name = Column(String, primary_key=True, index=True)
    description = Column(String, index=True)
    categrory = Column(Enum("Pastry", "Sandwich", "Salad", name="category_enum"), index=True)
    orders = relationship("Order", secondary=product_order, back_populates="products")
    
    
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    
    product_name = Column(String, index=True)
    date = Column(Date, index=True)
    products = relationship("Product", secondary=product_order, back_populates="orders")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True,unique=True)
    result = Column(String, index=True)
    
Base.metadata.create_all(bind=engine)