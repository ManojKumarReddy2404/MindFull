import requests
import json

# The URL of the running backend server
url = "http://127.0.0.1:8000/visualize"

# The data to send to the endpoint
payload = {
    "user_goal": "I want to feel more confident before my big presentation.",
    "user_input": "Guide me through a visualization to build my confidence."
}

# The headers for the request
headers = {
    "Content-Type": "application/json"
}

try:
    # Send the POST request
    print("--- Running Visualization Agent Test ---")
    print("Sending request to /visualize...")
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    print("Received response from /visualize.")
    
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
