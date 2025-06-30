import requests
import json
import pytest

BASE_URL = "http://localhost:8000"

@pytest.fixture
def answers():
    """Fixture to provide sample quiz answers."""
    return ["I feel anxious", "Work stress", "Almost daily"]

def test_quiz_ask():
    """Test the /quiz/ask endpoint."""
    print("\n=== Testing /quiz/ask ===")
    response = requests.post(
        f"{BASE_URL}/quiz/ask",
        json={"user_input": "I'm feeling anxious about work"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "questions" in response_data
    assert isinstance(response_data["questions"], list)
    assert len(response_data["questions"]) > 0
    print(f"Status: {response.status_code}")
    print("Response:", json.dumps(response_data, indent=2))

def test_quiz_submit(answers):
    """Test the /quiz/submit endpoint."""
    print("\n=== Testing /quiz/submit ===")
    response = requests.post(
        f"{BASE_URL}/quiz/submit",
        json={"answers": answers}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "summary" in response_data
    assert "recommended_meditation" in response_data
    assert "duration" in response_data
    print(f"Status: {response.status_code}")
    print("Response:", json.dumps(response_data, indent=2))

@pytest.mark.parametrize("voice_pref, music_pref", [
    ("calm", "nature"),
    ("happy", "upbeat_lofi.mp3"),
    ("anxious", "calming_waves.mp3")
])
def test_meditate(answers, voice_pref, music_pref):
    """Test the /meditate endpoint with different preferences."""
    print(f"\n=== Testing /meditate with voice: {voice_pref}, music: {music_pref} ===")
    response = requests.post(
        f"{BASE_URL}/meditate",
        json={
            "quiz_answers": answers,
            "user_input": "I need to relax",
            "voice_pref": voice_pref,
            "music_pref": music_pref
        }
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "meditation_text" in response_data
    assert "voice_output" in response_data
    assert "music_output" in response_data
    print(f"Status: {response.status_code}")
    # Print a preview of the meditation text
    if "meditation_text" in response_data:
        preview = response_data["meditation_text"][:150] + "..."
        print(f"Meditation preview: {preview}")
