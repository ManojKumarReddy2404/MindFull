import asyncio
import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)

async def run_analysis(quiz_answers: List[str], user_input: str) -> Dict[str, Any]:
    """
    A simplified, non-blocking dummy version of the analysis flow.
    This prevents the server from crashing on startup.
    """
    logging.info("Executing DUMMY run_analysis...")
    await asyncio.sleep(0.5) # Simulate non-blocking work
    return {
        "coach_response": "This is a dummy coach response from the dummy analyzer.",
        "voice_id": "dummy_voice_id",
        "music_style": "calm"
    }