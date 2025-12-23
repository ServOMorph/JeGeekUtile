import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_status():
    response = requests.get(f"{BASE_URL}/status")
    print("Test /status:", response.json())

def test_clipboard_copy():
    action = {
        "type": "clipboard_copy",
        "params": {
            "text": "Test automatisation auto_ia"
        }
    }
    response = requests.post(f"{BASE_URL}/action", json=action)
    print("Test clipboard_copy:", response.json())

def test_mouse_click():
    action = {
        "type": "mouse_click",
        "params": {
            "x": 100,
            "y": 100,
            "button": "left"
        }
    }
    response = requests.post(f"{BASE_URL}/action", json=action)
    print("Test mouse_click:", response.json())

if __name__ == "__main__":
    print("\n=== Tests API auto_ia ===\n")
    test_status()
    test_clipboard_copy()
    test_mouse_click()
    print("\n=== Tests terminés ===\n")
