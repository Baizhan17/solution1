from pydantic import BaseModel
from typing import List

class WeatherData(BaseModel):
    day_of_week: str
    temperature_celsius: float
    
    class Config:
        from_attributes = True

class SalesData(BaseModel):
    month: str
    sales_amount_pln: float
    
    class Config:
        from_attributes = True

class TrafficSourceData(BaseModel):
    source_name: str
    percentage: float
    
    class Config:
        from_attributes = True

class InventoryData(BaseModel):
    product_type: str
    quantity: int
    
    class Config:
        from_attributes = True