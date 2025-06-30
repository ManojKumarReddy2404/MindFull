import os
import uvicorn
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import aiohttp
import uuid
from pathlib import Path
import json
from datetime import datetime

# ===== Configuration =====
class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBLyVdrG4tCLYWw4zxGRxRFjGNZAO3RKu8")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "your_elevenlabs_api_key_here")
    SUNO_API_KEY = os.getenv("SUNO_API_KEY", "your_suno_api_key_here")
    
    # Configure Google's Generative AI
    genai.configure(api_key=GOOGLE_API_KEY)
    MODEL = "gemini-pro"  # or "gemini-1.5-pro" if available
    
    VOICE_CONFIG = {
        "default_voice": "Rachel",
        "voices": {
            "happy": "Rachel",
            "sad": "Bella",
            "angry": "Josh",
            "anxious": "Elli",
        },
        "api_url": "https://api.elevenlabs.io/v1"
    }
    
    MUSIC_CONFIG = {
        "default_style": "nature sounds",
        "styles": {
            "happy": "upbeat_lofi.mp3",
            "sad": "rain_ambience.mp3",
            "anxious": "calming_waves.mp3",
            "angry": "wind_flute.mp3",
        },
        "suno_api_url": "https://api.suno.ai/v1"
    }

# ===== Models =====
class QuestionRequest(BaseModel):
    user_input: str

class QuizAnswerRequest(BaseModel):
    answers: List[str]

class VoiceInput(BaseModel):
    text: str
    voice: str = "Rachel"

class MusicInput(BaseModel):
    style: str
    duration: Optional[int] = 300
    mood: Optional[str] = None

class MeditationInput(BaseModel):
    quiz_answers: List[str]
    user_input: str
    voice_pref: str
    music_pref: str

class FeedbackInput(BaseModel):
    session_id: str
    rating: int
    feedback: str

class MeditationResponse(BaseModel):
    meditation_text: str
    voice_output: str
    music_output: str

# ===== Initialize FastAPI =====
app = FastAPI(title="Zen Focus API", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Utility Functions =====
def get_voice_for_mood(mood: str) -> str:
    """Get appropriate voice for the given mood."""
    return Config.VOICE_CONFIG["voices"].get(mood.lower(), Config.VOICE_CONFIG["default_voice"])

def get_music_for_mood(mood: str) -> str:
    """Get appropriate music style for the given mood."""
    return Config.MUSIC_CONFIG["styles"].get(mood.lower(), Config.MUSIC_CONFIG["default_style"])

# ===== API Endpoints =====
@app.get("/")
async def read_root():
    """Health check endpoint."""
    return {"message": "Zen Focus API is running"}

# Quiz Agent Endpoints
@app.post("/quiz/ask")
async def ask_quiz_question(request: QuestionRequest):
    """Get quiz questions based on user input using Google's Generative AI."""
    try:
        model = genai.GenerativeModel(Config.MODEL)
        prompt = f"""
        You are a mental wellness assistant. Generate 3 thoughtful questions to understand the user's emotional state.
        User's input: {request.user_input}
        
        Return the questions as a JSON array of strings, like:
        ["Question 1", "Question 2", "Question 3"]
        """
        response = model.generate_content(prompt)
        questions = json.loads(response.text)
        return {"questions": questions[:3]}  # Return max 3 questions
    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        # Fallback questions
        return {
            "questions": [
                "How are you feeling right now?",
                "What triggered this feeling?",
                "Have you felt like this before?"
            ]
        }

@app.post("/quiz/submit")
async def submit_quiz_answers(request: QuizAnswerRequest):
    """Submit quiz answers and get a summary using Google's Generative AI."""
    try:
        model = genai.GenerativeModel(Config.MODEL)
        prompt = f"""
        Analyze these quiz answers and provide a brief summary and recommendation:
        Answers: {request.answers}
        
        Return a JSON object with:
        - summary: A short analysis of the user's emotional state
        - recommended_meditation: Type of meditation (breathing, mindfulness, etc.)
        - duration: Recommended duration in minutes (5-15)
        """
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        duration = int(result.get("duration", 5))
        duration = max(5, min(duration, 15))  # Ensure between 5-15 mins
        return {
            "summary": result.get("summary", "Let's focus on calming your mind."),
            "recommended_meditation": result.get("recommended_meditation", "breathing"),
            "duration": duration
        }
    except Exception as e:
        print(f"Error processing answers: {str(e)}")
        return {
            "summary": "You seem to be experiencing stress. Let's focus on calming techniques.",
            "recommended_meditation": "breathing",
            "duration": 5
        }

# Voice Agent
@app.post("/voice/generate")
async def generate_voice(input_data: VoiceInput):
    """Generate voice from text using ElevenLabs API."""
    if not Config.ELEVENLABS_API_KEY:
        raise HTTPException(status_code=500, detail="ElevenLabs API key not configured")
    
    # In a real implementation, this would call the ElevenLabs API
    voice_id = Config.VOICE_CONFIG["voices"].get(input_data.voice.lower(), 
                                              Config.VOICE_CONFIG["default_voice"])
    
    # Simulate voice generation
    output_path = f"voice_output/{uuid.uuid4()}.mp3"
    os.makedirs("voice_output", exist_ok=True)
    
    # Create empty file as placeholder
    with open(output_path, 'wb') as f:
        f.write(b'')  # Empty file for demo
    
    return {
        "status": "success",
        "voice_file": output_path,
        "voice_id": voice_id
    }

# Music Agent
@app.post("/music/generate")
async def generate_music(input_data: MusicInput):
    """Generate music based on style and mood."""
    # In a real implementation, this would call the Suno API
    output_path = f"music_output/{uuid.uuid4()}.mp3"
    os.makedirs("music_output", exist_ok=True)
    
    # Create empty file as placeholder
    with open(output_path, 'wb') as f:
        f.write(b'')  # Empty file for demo
    
    return {
        "status": "success",
        "music_file": output_path,
        "style": input_data.style,
        "mood": input_data.mood or "neutral"
    }

# Meditation Endpoint
@app.post("/meditate", response_model=MeditationResponse)
async def start_meditation(input_data: MeditationInput):
    """Start a meditation session with the given parameters using Google's Generative AI."""
    try:
        # Generate meditation script using Google's AI
        model = genai.GenerativeModel(Config.MODEL)
        prompt = f"""
        Create a {input_data.duration if hasattr(input_data, 'duration') else 5}-minute guided meditation script.
        User's mood/needs: {input_data.quiz_answers}
        Voice preference: {input_data.voice_pref}
        Music preference: {input_data.music_pref}
        
        Make it warm, encouraging, and focused on the user's needs.
        Include breathing instructions and body scan.
        """
        
        response = model.generate_content(prompt)
        meditation_text = response.text
        
        # Generate voice
        voice_response = await generate_voice(VoiceInput(
            text=meditation_text,
            voice=input_data.voice_pref
        ))
        
        # Generate music
        music_response = await generate_music(MusicInput(
            style=input_data.music_pref,
            mood=input_data.quiz_answers[0] if input_data.quiz_answers else "neutral"
        ))
        
        return MeditationResponse(
            meditation_text=meditation_text,
            voice_output=voice_response["voice_file"],
            music_output=music_response["music_file"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Feedback Endpoint
@app.post("/feedback")
async def submit_feedback(feedback: FeedbackInput):
    """Submit feedback for a meditation session."""
    # In a real app, you would save this to a database
    print(f"Feedback received for session {feedback.session_id}:")
    print(f"Rating: {feedback.rating}/5")
    print(f"Comments: {feedback.feedback}")
    
    return {
        "status": "success",
        "message": "Thank you for your feedback!"
    }

# ===== Run the Application =====
if __name__ == "__main__":
    # Create necessary directories
    for directory in ["voice_output", "music_output"]:
        os.makedirs(directory, exist_ok=True)
    
    # Initialize Google's Generative AI
    try:
        import google.generativeai as genai
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        print("✅ Google Generative AI configured successfully")
    except Exception as e:
        print(f"⚠️ Error initializing Google AI: {str(e)}")
    
    # Start the server
    uvicorn.run("single_file_app:app", host="0.0.0.0", port=8000, reload=True)
