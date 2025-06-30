import streamlit as st
import requests
import json
from pathlib import Path
import os

# Constants
BACKEND_URL = "http://127.0.0.1:8000"

def main():
    st.set_page_config(
        page_title="Zen AI Meditation",
        page_icon="🧘",
        layout="wide"
    )

    st.title("Zen AI Meditation")
    st.markdown("Find your inner peace with AI-guided meditation")

    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = []
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = []
    if 'meditation_response' not in st.session_state:
        st.session_state.meditation_response = None

    # Step 1: Initial feeling input
    if st.session_state.step == 1:
        st.subheader("How are you feeling today?")
        user_input = st.text_area("Share your thoughts...", height=100)
        
        if st.button("Continue"):
            if user_input:
                try:
                    # Get quiz questions from backend
                    response = requests.post(
                        f"{BACKEND_URL}/quiz",
                        json={"user_message": user_input}
                    )
                    response.raise_for_status()
                    quiz_data = response.json()
                    
                    st.session_state.quiz_questions = quiz_data.get("quiz_questions", [])
                    st.session_state.user_input = user_input
                    st.session_state.step = 2
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error fetching quiz questions: {str(e)}")

    # Step 2: Quiz questions
    elif st.session_state.step == 2:
        st.subheader("Let's understand you better")
        
        # Display quiz questions
        answers = []
        for i, question in enumerate(st.session_state.quiz_questions):
            answer = st.text_input(f"Q{i+1}: {question}", key=f"q{i}")
            answers.append(answer)

        # Voice and music preferences
        st.subheader("Choose your preferences")
        col1, col2 = st.columns(2)
        
        with col1:
            voice_pref = st.selectbox(
                "Voice Preference",
                ["Rachel", "Domi", "Bella", "Antoni", "Elli", "Josh", "Arnold", "Adam", "Sam"]
            )
        
        with col2:
            music_pref = st.selectbox(
                "Music Style",
                ["calm", "nature sounds", "binaural beats", "instrumental"]
            )

        if st.button("Get Meditation"):
            if all(answers):  # Check if all questions are answered
                try:
                    # Send everything to meditate endpoint
                    meditation_data = {
                        "quiz_answers": answers,
                        "user_input": st.session_state.user_input,
                        "voice_pref": voice_pref,
                        "music_pref": music_pref
                    }
                    
                    response = requests.post(
                        f"{BACKEND_URL}/meditate",
                        json=meditation_data
                    )
                    response.raise_for_status()
                    
                    st.session_state.meditation_response = response.json()
                    st.session_state.step = 3
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error getting meditation: {str(e)}")
            else:
                st.warning("Please answer all questions")

    # Step 3: Show meditation response
    elif st.session_state.step == 3:
        st.subheader("Your Personalized Meditation")
        
        response = st.session_state.meditation_response
        if response:
            # Display meditation text
            st.markdown("### Meditation Guide")
            st.write(response["meditation_text"])
            
            # Display audio players if files exist
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Voice Guide")
                voice_path = response["voice_output"]
                if os.path.exists(voice_path):
                    st.audio(voice_path)
                else:
                    st.warning("Voice file not found")
            
            with col2:
                st.markdown("### Background Music")
                music_path = response["music_output"]
                if os.path.exists(music_path):
                    st.audio(music_path)
                else:
                    st.warning("Music file not found")
        
        if st.button("Start New Session"):
            # Reset session state
            for key in st.session_state.keys():
                del st.session_state[key]
            st.session_state.step = 1
            st.experimental_rerun()

if __name__ == "__main__":
    main() 