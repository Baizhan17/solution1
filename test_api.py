import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Test cases for all API endpoints"""
    
    print("Testing API endpoints...\n")
    
    # Test Case 1: Weather endpoint
    print("Test Case 1: /api/weather")
    print("Expected URL: GET http://localhost:8000/api/weather")
    response = requests.get(f"{BASE_URL}/api/weather")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data[:2], indent=2)}")
        print("✓ Test passed: Returns weather data in JSON format")
    else:
        print("✗ Test failed")
    print()
    
    # Test Case 2: Sales endpoint
    print("Test Case 2: /api/sales")
    print("Expected URL: GET http://localhost:8000/api/sales")
    response = requests.get(f"{BASE_URL}/api/sales")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data[:2], indent=2)}")
        print("✓ Test passed: Returns sales data in JSON format")
    else:
        print("✗ Test failed")
    print()
    
    # Test Case 3: Traffic endpoint
    print("Test Case 3: /api/traffic")
    print("Expected URL: GET http://localhost:8000/api/traffic")
    response = requests.get(f"{BASE_URL}/api/traffic")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data[:2], indent=2)}")
        print("✓ Test passed: Returns traffic data in JSON format")
    else:
        print("✗ Test failed")
    print()
    
    # Test Case 4: Inventory endpoint
    print("Test Case 4: /api/inventory")
    print("Expected URL: GET http://localhost:8000/api/inventory")
    response = requests.get(f"{BASE_URL}/api/inventory")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data[:2], indent=2)}")
        print("✓ Test passed: Returns inventory data in JSON format")
    else:
        print("✗ Test failed")

if __name__ == "__main__":
    # Запуск тестов после запуска сервера
    print("Make sure the server is running on http://localhost:8000")
    print("Run: uvicorn main:app --reload")
    input("Press Enter to run tests...")
    test_endpoints()