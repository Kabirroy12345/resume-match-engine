import requests
import json

def test_score():
    url = "http://127.0.0.1:8000/score"
    payload = {
        "resume": "Experienced Python developer with FastAPI and React skills.",
        "jd": "Looking for a Python Backend Developer with FastAPI experience.",
        "skills": ["Python", "FastAPI"]
    }
    
    try:
        print(f"Testing {url}...")
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print("Error:", response.text)
            
        # Check CORS
        print("\nChecking CORS headers...")
        resp_options = requests.options(url, headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST"
        })
        print(f"CORS Status: {resp_options.status_code}")
        print(f"Access-Control-Allow-Origin: {resp_options.headers.get('Access-Control-Allow-Origin')}")
        print(f"Access-Control-Allow-Credentials: {resp_options.headers.get('Access-Control-Allow-Credentials')}")
        
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_score()
