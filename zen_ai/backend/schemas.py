from pydantic import BaseModel

class UserInput(BaseModel):
    user_message: str

class QuizAnswers(BaseModel):
    answers: list[str]

class FeedbackInput(BaseModel):
    session_id: str
    user_input: str

class MeditationResponse(BaseModel):
    meditation_text: str
    voice_output: str
    music_output: str 