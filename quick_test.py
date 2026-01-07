import requests

BASE_URL = "http://localhost:8000"

endpoints = [
    "/api/weather",
    "/api/sales",
    "/api/traffic",
    "/api/inventory"
]

print("Quick API Test")
print("=" * 40)

for endpoint in endpoints:
    try:
        response = requests.get(BASE_URL + endpoint)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ {endpoint}: OK ({len(data)} items)")
        else:
            print(f"✗ {endpoint}: Failed - {response.status_code}")
    except Exception as e:
        print(f"✗ {endpoint}: Error - {e}")