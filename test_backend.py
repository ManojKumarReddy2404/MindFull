import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_quiz_endpoint():
    print("Testing /quiz endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/quiz/", params={"user_message": "I am feeling stressed"})
        if response.status_code == 200:
            print("GET /quiz successful!")
            print("Response:", response.json())
        else:
            print(f"GET /quiz failed with status code {response.status_code}")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def test_meditate_endpoint():
    print("\nTesting /meditate endpoint...")
    try:
        payload = {
            "quiz_answers": ["Yes", "A little"],
            "user_input": "I feel stressed and anxious about my upcoming exams.",
            "voice_pref": "Rachel",
            "music_pref": "Calm"
        }
        print("Sending POST request to /meditate...")
        response = requests.post(f"{BASE_URL}/meditate", json=payload, timeout=60)
        print(f"Received response with status code: {response.status_code}")
        if response.status_code == 200:
            print("POST /meditate successful!")
            print("Attempting to parse JSON response...")
            json_response = response.json()
            print("Response:", json_response)
            print("JSON parsing complete.")
        else:
            print(f"POST /meditate failed with status code {response.status_code}")
            print("Attempting to read response text...")
            response_text = response.text
            print("Response:", response_text)
            print("Response text read.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during request: {e}")
    except Exception as e:
        import traceback
        print(f"An unexpected error occurred in test_meditate_endpoint:")
        traceback.print_exc()

def test_visualization_endpoint():
    print("\nTesting /generate-visualization endpoint...")
    try:
        payload = {
            "emotion": "a bit stressed",
            "focus": "an upcoming project",
            "dream": "to feel more confident in my work",
            "desired_feeling": "calm and focused"
        }
        print("Sending POST request to /generate-visualization...")
        response = requests.post(f"{BASE_URL}/generate-visualization", json=payload, timeout=60)
        print(f"Received response with status code: {response.status_code}")
        if response.status_code == 200:
            print("POST /generate-visualization successful!")
            json_response = response.json()
            print("Response:", json.dumps(json_response, indent=2))
        else:
            print(f"POST /generate-visualization failed with status code {response.status_code}")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during request: {e}")

def test_feedback_endpoint():
    print("\nTesting /feedback endpoint...")
    try:
        payload = {"session_id": "12345", "user_input": "The meditation was helpful."}
        response = requests.post(f"{BASE_URL}/feedback", json=payload)
        if response.status_code == 200:
            print("POST /feedback successful!")
            print("Response:", response.json())
        else:
            print(f"POST /feedback failed with status code {response.status_code}")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def test_root_endpoint():
    print("\nTesting root (/) endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("GET / successful!")
            print("Response:", response.json())
        else:
            print(f"GET / failed with status code {response.status_code}")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_root_endpoint()
    # test_quiz_endpoint() # Commenting out to focus on the new endpoint
    # test_meditate_endpoint()
    test_visualization_endpoint() # Testing our new endpoint
    # test_feedback_endpoint()
