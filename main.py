from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine, get_db

# Создание таблиц
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend API", description="API for business data")

@app.get("/api/weather", response_model=List[schemas.WeatherData])
def get_weather_data(db: Session = Depends(get_db)):
    """Get weather data: days of week and temperature"""
    weather_data = db.query(models.Weather).order_by(models.Weather.date).all()
    return weather_data

@app.get("/api/sales", response_model=List[schemas.SalesData])
def get_sales_data(db: Session = Depends(get_db)):
    """Get sales data: months and sales amount in PLN"""
    # Создаем порядок месяцев для правильной сортировки
    month_order = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    # Получаем все данные
    sales_data = db.query(models.Sales).all()
    
    # Сортируем в Python по порядку месяцев
    sorted_data = sorted(sales_data, key=lambda x: month_order.get(x.month, 13))
    
    return sorted_data

@app.get("/api/traffic", response_model=List[schemas.TrafficSourceData])
def get_traffic_data(db: Session = Depends(get_db)):
    """Get traffic sources data: source names and percentages"""
    traffic_data = db.query(models.TrafficSource).order_by(
        models.TrafficSource.percentage.desc()
    ).all()
    return traffic_data

@app.get("/api/inventory", response_model=List[schemas.InventoryData])
def get_inventory_data(db: Session = Depends(get_db)):
    """Get inventory data: product types and quantities"""
    inventory_data = db.query(models.Inventory).order_by(
        models.Inventory.quantity.desc()
    ).all()
    return inventory_data

@app.get("/")
def read_root():
    return {"message": "Visit /docs for documentation"}