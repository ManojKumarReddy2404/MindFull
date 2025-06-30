import asyncio
from agents.quiz_agent import generate_quiz
from agents.analyzer_agent import analyze_quiz
from agents.multi_role_agent import run_dynamic_meditation
from agents.voice_agent import synthesize_voice, select_voice
from agents.music_agent import generate_music, select_music_style
from agents.feedback_agent import collect_feedback
from agents.visualization_agent import generate_visualization_script

async def main():
    print("--- Running Agent Status Check ---")

    # 1. Quiz Agent
    try:
        print("\n[1/7] Testing Quiz Agent...")
        result = generate_quiz("I'm feeling stressed about work.")
        if result and isinstance(result, list):
            print("  -> Status: OK")
        else:
            print("  -> Status: FAILED - Did not return a list.")
    except Exception as e:
        print(f"  -> Status: FAILED - {e}")

    # 2. Analyzer Agent
    try:
        print("\n[2/7] Testing Analyzer Agent...")
        result = analyze_quiz(["I chose 'anxious'", "I want to feel 'calm'"])
        if result and isinstance(result, dict):
            print("  -> Status: OK")
        else:
            print("  -> Status: FAILED - Did not return a dictionary.")
    except Exception as e:
        print(f"  -> Status: FAILED - {e}")

    # 3. Multi-Role (Meditation) Agent
    try:
        print("\n[3/7] Testing Multi-Role (Meditation) Agent...")
        advice_input = {"mood_tags": ["stressed"], "preferred_session": "meditation", "needs": ["relaxation"]}
        result = run_dynamic_meditation(advice_input)
        if result and isinstance(result, str):
            print("  -> Status: OK")
        else:
            print("  -> Status: FAILED - Did not return a string.")
    except Exception as e:
        print(f"  -> Status: FAILED - {e}")

    # 4. Visualization Agent
    try:
        print("\n[4/7] Testing Visualization Agent...")
        result = generate_visualization_script('anxious', 'work', 'success', 'confident')
        if result and isinstance(result, str):
            print("  -> Status: OK")
        else:
            print("  -> Status: FAILED - Did not return a string.")
    except Exception as e:
        print(f"  -> Status: FAILED - {e}")

    # 5. Voice Agent
    try:
        print("\n[5/7] Testing Voice Agent...")
        voice_id = select_voice('calm')
        result = synthesize_voice("Hello, this is a test.", voice_id)
        if result and isinstance(result, str):
            print("  -> Status: OK")
        else:
            print("  -> Status: FAILED - Did not return a string.")
    except Exception as e:
        print(f"  -> Status: FAILED - {e}")

    # 6. Music Agent
    try:
        print("\n[6/7] Testing Music Agent...")
        music_style = select_music_style('happy', [])
        result = generate_music(music_style)
        if result and isinstance(result, str):
            print("  -> Status: OK")
        else:
            print("  -> Status: FAILED - Did not return a string.")
    except Exception as e:
        print(f"  -> Status: FAILED - {e}")

    # 7. Feedback Agent
    try:
        print("\n[7/7] Testing Feedback Agent...")
        # This agent doesn't return anything, so we just check for exceptions
        collect_feedback("test_session_123", "This was a great session!")
        print("  -> Status: OK")
    except Exception as e:
        print(f"  -> Status: FAILED - {e}")

    print("\n--- Agent Status Check Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
