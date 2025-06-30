from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import httpx
from pathlib import Path
import uuid
from datetime import datetime
from zen_ai.backend.settings import VOICE_CONFIG

router = APIRouter()

class VoiceInput(BaseModel):
    text: str
    voice: str = "Rachel"

@router.post("/generate_voice")
async def generate_voice(input_data: VoiceInput):
    # Use the API key from environment variables
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY not found")

    # Create voice_output directory if it doesn't exist
    output_dir = Path("voice_output")
    output_dir.mkdir(exist_ok=True)

    # Prepare the API request
    url = "https://api.elevenlabs.io/v1/text-to-speech"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    # Get voice ID based on the voice name
    voice_id = await get_voice_id(input_data.voice)
    
    data = {
        "text": input_data.text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    try:
        # Make request to ElevenLabs API
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{url}/{voice_id}", json=data, headers=headers)
            response.raise_for_status()
            audio_content = response.content

            # Save the audio file
            output_path = output_dir / f"{input_data.voice}.mp3"
            with open(output_path, "wb") as f:
                f.write(audio_content)

            return {"file_path": str(output_path)}

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error calling ElevenLabs API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

async def get_voice_id(voice_name: str) -> str:
    """Get ElevenLabs voice ID for a given voice name."""
    try:
        # Map voice names to their IDs
        voice_map = {
            "Rachel": "21m00Tcm4TlvDq8ikWAM",
            "Domi": "AZnzlk1XvdvUeBnXmlld",
            "Bella": "EXAVITQu4vr4xnSDxMaL",
            "Antoni": "ErXwobaYiN019PkySvjV",
            "Elli": "MF3mGyEYCl7XYWbV9V6O",
            "Josh": "TxGEqnHWrfWFTfGW9XjX",
            "Arnold": "VR6AewLTigWG4xSOukaG",
            "Adam": "pNInz6obpgDQGcFmaJgB",
            "Sam": "yoZ06aMxZJJ28mfd3POQ"
        }
        return voice_map.get(voice_name, voice_map["Rachel"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting voice ID: {str(e)}")

async def synthesize_voice(text: str, voice_name: str = "Rachel") -> dict:
    """
    Synthesize voice using ElevenLabs API.
    Returns a dictionary with the file path of the generated audio.
    """
    try:
        # Get voice ID
        voice_id = await get_voice_id(voice_name)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"voice_{timestamp}_{unique_id}.mp3"
        output_path = Path("zen_ai/voice_output") / filename

        # ElevenLabs API endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        # Get API key from environment
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY not found")

        # Prepare request headers and data
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        # Make API request
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"ElevenLabs API error: {response.text}"
                )
            
            # Save audio file
            audio_data = response.content
            with open(output_path, "wb") as f:
                f.write(audio_data)

        return {
            "file_path": str(output_path),
            "voice_name": voice_name,
            "timestamp": timestamp
        }

    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"ElevenLabs API connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice synthesis error: {str(e)}")

async def get_voice_for_mood(mood: str) -> str:
    """Get appropriate voice for the given mood."""
    return VOICE_CONFIG["voices"].get(mood.lower(), VOICE_CONFIG["default_voice"])

def select_voice(user_preference: str) -> str:
    """
    Select a voice ID based on user preference.
    Only uses free voices available in ElevenLabs.
    """
    # Map of free ElevenLabs voices
    voice_map = {
        "rachel": "21m00Tcm4TlvDq8ikWAM",  # Female voice, clear and professional
        "domi": "AZnzlk1XvdvUeBnXmlld",    # Female voice, warm and friendly
        "bella": "EXAVITQu4vr4xnSDxMaL",   # Female voice, calm and soothing
        "antoni": "ErXwobaYiN019PkySvjV",   # Male voice, deep and authoritative
        "elli": "MF3mGyEYCl7XYWbV9V6O",    # Female voice, young and energetic
        "josh": "TxGEqnHWrfWFTfGW9XjX",    # Male voice, natural and conversational
        "arnold": "VR6AewLTigWG4xSOukaG",   # Male voice, deep and powerful
        "adam": "pNInz6obpgDQGcFmaJgB",    # Male voice, clear and professional
        "sam": "yoZ06aMxZJJ28mfd3POQ"      # Male voice, natural and friendly
    }

    # Normalize user preference for matching
    normalized_preference = user_preference.lower().strip()

    # Try to find an exact match first
    if normalized_preference in voice_map:
        return voice_map[normalized_preference]

    # If no exact match, try to find a partial match
    for voice_name, voice_id in voice_map.items():
        if voice_name in normalized_preference or normalized_preference in voice_name:
            return voice_id

    # Default to Rachel if no match is found
    return voice_map["rachel"] 