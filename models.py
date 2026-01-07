from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Weather(Base):
    __tablename__ = "weather"
    
    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String, nullable=False)
    temperature_celsius = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

class Sales(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)
    sales_amount_pln = Column(Float, nullable=False)
    year = Column(Integer, nullable=False)

class TrafficSource(Base):
    __tablename__ = "traffic_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)
    period = Column(String, nullable=False)

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    product_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    warehouse_location = Column(String, nullable=False)