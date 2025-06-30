import asyncio
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)

async def run_full_meditation_flow(
    user_input: str,
    quiz_answers: Dict[str, Any],
    voice_pref: str,
    music_pref: str
) -> Dict[str, Any]:
    """
    A simplified, non-blocking dummy version of the meditation flow.
    This function simulates an async operation and returns a fixed response
    to prevent the server from crashing on startup.
    """
    logging.info("Executing DUMMY run_full_meditation_flow...")
    await asyncio.sleep(1)  # Simulate a non-blocking operation

    # Return a dictionary matching the expected structure
    return {
        "coach_response": f"This is a dummy meditation script based on your input: '{user_input}'.",
        "voice_id": "dummy_voice_id",
        "music_style": "dummy_music_style",
        "end_of_flow": True
    }