import requests
import json

# The URL of the running backend server
url = "http://127.0.0.1:8000/meditate"

# The data to send to the endpoint
payload = {
    "quiz_answers": ["I've been feeling anxious and stressed.", "I want to find a moment of peace."],
    "user_input": "Guide me through a short session to calm my mind.",
    "voice_pref": "female_calm",
    "music_pref": "calm_piano"
}

# The headers for the request
headers = {
    "Content-Type": "application/json"
}

try:
    # Send the POST request
    print("--- Running Meditation Agent Test ---")
    # Send the POST request with a 30-second timeout
    print("Sending request to /meditate...")
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    print("Received response from /meditate.")
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Print the JSON response from the server
    print("Test successful! Response:")
    print(response.json())

except requests.exceptions.RequestException as e:
    print(f"Test failed. An error occurred: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Status Code: {e.response.status_code}")
        print(f"Response Body: {e.response.text}")

finally:
    print("--- Test Complete ---")
