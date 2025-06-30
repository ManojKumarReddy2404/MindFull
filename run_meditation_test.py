import requests
import json

# Define the endpoint URL
url = "http://localhost:8000/meditate"

# Define the payload with sample user answers
# This simulates a user feeling anxious about work and seeking clarity.
payload = {
    "quiz_answers": ["Anxious", "Work", "Inner peace", "Clarity"],
    "user_input": "I'm feeling stressed about a big project at work and I want to find some mental clarity.",
    "voice_pref": "alloy",
    "music_pref": "Calm"
}

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
try:
    print("Sending request to the meditation agent...")
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120) # Increased timeout for AI generation
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    # Print the successful response
    print("\n--- Test Report ---")
    print("Request successful! The meditation agent generated the following content:")
    print(json.dumps(response.json(), indent=2))

except requests.exceptions.Timeout:
    print("\n--- Test Report ---")
    print("Error: The request timed out. The AI services may be taking too long to respond.")
except requests.exceptions.HTTPError as http_err:
    print("\n--- Test Report ---")
    print(f"Error: An HTTP error occurred: {http_err}")
    print(f"Response content: {response.text}")
except requests.exceptions.RequestException as err:
    print("\n--- Test Report ---")
    print(f"Error: A connection error occurred: {err}")
