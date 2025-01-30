from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_system_info():
    print("\n\nTesting /system-info\n\n")
    response = client.get("/system-info")
    assert response.status_code == 200
    print(f"Status Code: {response.status_code}")
    print(f"JSON Content: {response.json()}")
    print(f"Raw Content: {response.content.decode('utf-8')}")

def test_network_info():
    print("\n\nTesting /network-info\n\n")
    response = client.get("/network-info")
    assert response.status_code == 200
    print(f"Status Code: {response.status_code}")
    print(f"JSON Content: {response.json()}")
    print(f"Raw Content: {response.content.decode('utf-8')}")
