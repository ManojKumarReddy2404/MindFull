from zen_ai.backend.agents.analyzer_agent import perform_analysis_logic
from zen_ai.backend.agents.multi_role_agent import run_dynamic_meditation
from zen_ai.backend.agents.voice_agent import select_voice
from zen_ai.backend.agents.music_agent import select_music_style
import json

async def run_full_meditation_flow(user_input: str, quiz_answers: list, voice_pref: str, music_pref: str) -> dict:
    print("--- Starting Meditation Flow ---")
    print(f"Initial inputs: user_input='{user_input}', quiz_answers={quiz_answers}, voice_pref='{voice_pref}', music_pref='{music_pref}'")

    # Step 1: Analyze quiz answers to get mood, preferred session, and needs
    print("\n[Step 1] Analyzing quiz answers...")
    analyzed_data = perform_analysis_logic(quiz_answers)
    print(f"[Step 1] Analysis complete. Result: {json.dumps(analyzed_data, indent=2)}")

    # Step 2: Generate dynamic meditation text based on analyzed data
    print("\n[Step 2] Generating dynamic meditation text...")
    meditation_text = run_dynamic_meditation(analyzed_data)
    print(f"[Step 2] Meditation text generated. Length: {len(meditation_text) if meditation_text else 0} characters.")

    # Step 3: Select voice ID based on user preference
    print(f"\n[Step 3] Selecting voice for preference: '{voice_pref}'...")
    selected_voice_id = select_voice(voice_pref)
    print(f"[Step 3] Voice selected. ID: {selected_voice_id}")

    # Step 4: Select music style based on user preference and needs
    print(f"\n[Step 4] Selecting music style for preference: '{music_pref}' and needs: {analyzed_data.get('needs', [])}...")
    selected_music_style = select_music_style(music_pref, analyzed_data.get("needs", []))
    print(f"[Step 4] Music style selected: {selected_music_style}")

    final_output = {
        "coach_response": meditation_text,
        "voice_id": selected_voice_id,
        "music_style": selected_music_style
    }
    print("\n--- Meditation Flow Complete ---")
    print(f"Final output: {json.dumps(final_output, indent=2)}")

    return final_output