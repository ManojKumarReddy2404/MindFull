import os
import logging
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# --- Agent Imports (Starting with Meditation) ---
from zen_ai.backend.agents.meditation_agent import run_full_meditation_flow

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)

# --- FastAPI App Initialization ---
app = FastAPI(title="Zen AI Coach API (Minimal Test)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class MeditationRequest(BaseModel):
    user_input: str
    quiz_answers: List[str]
    voice_pref: str
    music_pref: str

class MeditationResponse(BaseModel):
    meditation_text: str
    voice_output: str
    music_output: str

class VisualizationRequest(BaseModel):
    user_goal: str
    user_input: str

class VisualizationResponse(BaseModel):
    visualization_text: str

# --- API Endpoints (with simplified, inline logic) ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Zen AI Coach API (Minimal Test)"}

@app.post("/meditate", response_model=MeditationResponse)
async def handle_meditation_request(input_data: MeditationRequest):
    logging.info(f"Received meditation request for user input: {input_data.user_input[:50]}...")
    try:
        # Step 1: Run the core meditation agent
        logging.info("Calling run_full_meditation_flow...")
        flow_result = await run_full_meditation_flow(
            user_input=input_data.user_input,
            quiz_answers=input_data.quiz_answers,
            voice_pref=input_data.voice_pref,
            music_pref=input_data.music_pref,
        )
        logging.info(f"Meditation flow completed.")
        meditation_text = flow_result.get("coach_response")

        if not meditation_text:
            raise HTTPException(status_code=500, detail="Core agent flow did not return meditation text.")

        # Step 2 & 3: Use dummy paths for now to isolate testing
        voice_output_path = "dummy/voice.mp3"
        music_output_path = "dummy/music.mp3"
        logging.info("Using dummy paths for voice and music.")

        return MeditationResponse(
            meditation_text=meditation_text,
            voice_output=voice_output_path,
            music_output=music_output_path,
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred in meditation flow: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected internal server error occurred.")

@app.post("/visualize", response_model=VisualizationResponse)
async def handle_visualization_request(input_data: VisualizationRequest):
    logging.info("Received /visualize request")
    await asyncio.sleep(1)  # Simulate async work
    return VisualizationResponse(
        visualization_text=f"Simplified visualization for: {input_data.user_goal}"
    )