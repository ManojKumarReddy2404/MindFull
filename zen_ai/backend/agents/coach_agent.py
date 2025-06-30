from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from .analyzer_agent import perform_analysis_logic

router = APIRouter()

class AnalyzeInput(BaseModel):
    mood_tags: List[str]
    needs: List[str]
    preferred_session: str

class CoachInput(BaseModel):
    quiz_answers: List[str]

@router.post("/generate_plan")
def generate_plan(data: AnalyzeInput):
    plan = {
        "session": data.preferred_session,
        "steps": []
    }

    if "calm" in data.needs:
        plan["steps"].append("Begin with 5 minutes of mindful breathing.")
    if "rest" in data.needs:
        plan["steps"].append("Do a 10-minute body scan meditation.")
    if "focus" in data.needs:
        plan["steps"].append("Try 5-minute visualization of your goal.")

    return {
        "plan": plan,
        "message": "Your meditation plan is ready!"
    }

@router.post("/generate_visualization_plan")
def generate_visualization_plan(data: CoachInput):
    # Step 1: Analyze quiz answers to get mood, preferred session, and needs
    analyzed_data = perform_analysis_logic(data.quiz_answers)
    
    # Step 2: Generate a plan based on the analysis
    plan = {
        "session": analyzed_data.get("preferred_session", "visualization"),
        "steps": []
    }
    
    needs = analyzed_data.get("needs", [])
    if "calm" in needs:
        plan["steps"].append("Begin with 5 minutes of mindful breathing.")
    if "rest" in needs:
        plan["steps"].append("Do a 10-minute body scan meditation.")
    if "focus" in needs:
        plan["steps"].append("Try a 5-minute visualization of your goal.")

    # Add a default step if no other steps are generated
    if not plan["steps"]:
        plan["steps"].append("Take a moment to focus on your breath and the feeling you want to cultivate.")
        
    return {
        "plan": plan,
        "message": "Your visualization plan is ready!"
    }