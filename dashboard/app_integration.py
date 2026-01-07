# dashboard/app_integration.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
import asyncio
from typing import List, Dict, Any
import time

app = FastAPI(
    title="Dashboard Consumer",
    description="Data consumer from the Data Provider API",
    version="1.0.0"
)


templates = Jinja2Templates(directory="dashboard/templates")

#DATA_PROVIDER_URL = "http://localhost:8000"
DATA_PROVIDER_URL = "https://solution1-1.onrender.com"
TIMEOUT = 10.0

async def fetch_from_provider(client: httpx.AsyncClient, endpoint: str) -> List[Dict[str, Any]]:
    """
  Receives data from the Data Provider via httpx
Demonstrates that the Consumer does NOT access the database directly, but calls Block A's endpoints.
    """
    url = f"{DATA_PROVIDER_URL}{endpoint}"
    
    try:
        #httpx used
        response = await client.get(url, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print(f"✓ Successfully received data from {endpoint}")
            return response.json()
        else:
            print(f"✗ Error {response.status_code} from request {endpoint}")
            return []
            
    except httpx.TimeoutException:
        print(f"⚠ Timeout while requesting{endpoint}")
        return []
    except httpx.RequestError as e:
        print(f"⚠ Error connecting to {endpoint}: {e}")
        return []
    except Exception as e:
        print(f"⚠ Unexpected error: {e}")
        return []

@app.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
 
    print("\n" + "="*50)
    print("STARTING DASHBOARD")
    print("="*50)
    
    start_time = time.time()
    
    # creating httpx async client
    async with httpx.AsyncClient() as client:


        weather_task = fetch_from_provider(client, "/api/weather")
        sales_task = fetch_from_provider(client, "/api/sales")
        traffic_task = fetch_from_provider(client, "/api/traffic")
        inventory_task = fetch_from_provider(client, "/api/inventory")
        
    
        results = await asyncio.gather(
            weather_task,
            sales_task, 
            traffic_task,
            inventory_task,
            return_exceptions=False  
        )
    
    weather_data, sales_data, traffic_data, inventory_data = results
    
    execution_time = round(time.time() - start_time, 3)
    
    print(f"\nDATA GATHERED:")
    print(f"  • Weather: {len(weather_data)} records")
    print(f"  • Sales: {len(sales_data)} records")
    print(f"  • Traffic: {len(traffic_data)} records")
    print(f"  • Inventory: {len(inventory_data)} records")
    print(f"  • Execution time: {execution_time} seconds")
    print("="*50 + "\n")
    
 
    context = {
        "request": request,
        "weather": weather_data,
        "sales": sales_data,
        "traffic": traffic_data,
        "inventory": inventory_data,
        "execution_time": execution_time,
        "provider_url": DATA_PROVIDER_URL
    }
    
    return templates.TemplateResponse("dashboard.html", context)

@app.get("/api/combined-data")
async def get_combined_data():
    """
  An API endpoint that returns all data in a single JSON file.

    """
    async with httpx.AsyncClient() as client:
    
        endpoints = [
            "/api/weather",
            "/api/sales",
            "/api/traffic", 
            "/api/inventory"
        ]
        
        tasks = [fetch_from_provider(client, endpoint) for endpoint in endpoints]
        weather, sales, traffic, inventory = await asyncio.gather(*tasks)
    
    return {
        "source": "Data from Provider API",
        "provider_url": DATA_PROVIDER_URL,
        "timestamp": time.time(),
        "data": {
            "weather": weather,
            "sales": sales,
            "traffic": traffic,
            "inventory": inventory
        },
        "metadata": {
            "total_records": len(weather) + len(sales) + len(traffic) + len(inventory),
            "collection_method": "httpx async requests to provider API"
        }
    }

@app.get("/health")
async def health_check():
    """
   System health check
    """
    health_status = {
        "consumer": {
            "status": "running",
            "port": 8001,
            "service": "Dashboard Consumer"
        },
        "provider": {
            "url": DATA_PROVIDER_URL,
            "status": "unknown",
            "endpoints": {}
        }
    }
    

    async with httpx.AsyncClient() as client:
        endpoints = [
            ("/api/weather", "Weather API"),
            ("/api/sales", "Sales API"),
            ("/api/traffic", "Traffic API"),
            ("/api/inventory", "Inventory API")
        ]
        
        for endpoint, name in endpoints:
            try:
                response = await client.get(f"{DATA_PROVIDER_URL}{endpoint}", timeout=5.0)
                health_status["provider"]["endpoints"][name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "status_code": response.status_code,
                    "response_time": f"{response.elapsed.total_seconds():.3f}s"
                }
            except Exception as e:
                health_status["provider"]["endpoints"][name] = {
                    "status": "error",
                    "error": str(e),
                    "status_code": None
                }
    
   
    all_healthy = all(
        ep["status"] == "healthy" 
        for ep in health_status["provider"]["endpoints"].values() 
        if "status" in ep
    )
    
    health_status["provider"]["status"] = "healthy" if all_healthy else "unhealthy"
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
