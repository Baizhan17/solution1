import sqlite3
from datetime import datetime, timedelta

def init_database():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Создание таблиц
    cursor.executescript('''
    DROP TABLE IF EXISTS weather;
    DROP TABLE IF EXISTS sales;
    DROP TABLE IF EXISTS traffic_sources;
    DROP TABLE IF EXISTS inventory;
    
    CREATE TABLE weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_of_week TEXT NOT NULL,
        temperature_celsius REAL NOT NULL,
        date DATE NOT NULL
    );
    
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL,
        sales_amount_pln REAL NOT NULL,
        year INTEGER NOT NULL
    );
    
    CREATE TABLE traffic_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_name TEXT NOT NULL,
        percentage REAL NOT NULL,
        period TEXT NOT NULL
    );
    
    CREATE TABLE inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_type TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        warehouse_location TEXT NOT NULL
    );
    ''')
    
    # Наполнение данными
    # Weather data
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    temperatures = [15.5, 16.2, 14.8, 18.3, 20.1, 19.5, 17.8]
    today = datetime.now()
    
    for i, (day, temp) in enumerate(zip(days, temperatures)):
        date = today - timedelta(days=6-i)
        cursor.execute(
            "INSERT INTO weather (day_of_week, temperature_celsius, date) VALUES (?, ?, ?)",
            (day, temp, date.strftime('%Y-%m-%d'))
        )
    
    # Sales data
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    sales = [120000, 115000, 135000, 140000, 160000, 175000, 
             185000, 180000, 170000, 165000, 150000, 130000]
    
    for month, amount in zip(months, sales):
        cursor.execute(
            "INSERT INTO sales (month, sales_amount_pln, year) VALUES (?, ?, ?)",
            (month, amount, 2024)
        )
    
    # Traffic sources data
    traffic_sources = [
        ('Organic Search', 35.5),
        ('Direct Traffic', 25.2),
        ('Social Media', 18.7),
        ('Email Marketing', 12.3),
        ('Paid Advertising', 8.3)
    ]
    
    for source, percentage in traffic_sources:
        cursor.execute(
            "INSERT INTO traffic_sources (source_name, percentage, period) VALUES (?, ?, ?)",
            (source, percentage, 'Q4 2024')
        )
    
    # Inventory data
    inventory_items = [
        ('Electronics', 150, 'Main Warehouse'),
        ('Clothing', 500, 'Warehouse A'),
        ('Books', 1200, 'Warehouse B'),
        ('Home Appliances', 300, 'Main Warehouse'),
        ('Sports Equipment', 250, 'Warehouse C'),
        ('Toys', 800, 'Warehouse B'),
        ('Furniture', 100, 'Warehouse A')
    ]
    
    for product_type, quantity, location in inventory_items:
        cursor.execute(
            "INSERT INTO inventory (product_type, quantity, warehouse_location) VALUES (?, ?, ?)",
            (product_type, quantity, location)
        )
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()