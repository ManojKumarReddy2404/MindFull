import boto3
import json
from zen_ai.backend.settings import (
    LLM_CONFIG,
    AWS_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)

def get_bedrock_client():
    """Initializes and returns a Bedrock runtime client."""
    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION]):
        raise ValueError("AWS credentials and region must be set in environment variables.")
    
    return boto3.client(
        service_name='bedrock-runtime',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

def run_dynamic_meditation(advice_input: dict) -> str:
    """
    Generates a dynamic meditation script using the configured Bedrock LLM.
    """
    try:
        client = get_bedrock_client()
    except ValueError as e:
        print(f"Error creating Bedrock client: {e}")
        return "There was an error setting up the meditation service. Please check your AWS credentials."

    # Extract user inputs
    mood_tags = advice_input.get("mood_tags", [])
    preferred_session = advice_input.get("preferred_session", "meditation")
    needs = advice_input.get("needs", [])

    # Determine the persona for the meditation coach
    role = "Meditation Coach"
    if preferred_session == "visualization":
        role = "Visualization Coach"
    elif "focus" in needs or "calm" in needs:
        role = "Therapist"
    elif "energy" in needs:
        role = "Motivational Coach"

    # Create a detailed, high-quality prompt for the LLM
    system_prompt = (
        f"You are a compassionate and experienced {role}. Your task is to create a personalized, guided meditation script. "
        f"The script should be approximately 3-4 paragraphs long. It should be soothing, easy to follow, and directly address the user's feelings and needs. "
        f"Start with a welcoming introduction, guide them through the main exercise, and end with a gentle, positive conclusion. "
        f"Do not include any sign-offs or introductory phrases like 'Here is the script'. Just provide the meditation text itself."
    )
    
    user_prompt = (
        f"The user is feeling {', '.join(mood_tags)} and has expressed needs for {', '.join(needs)}. "
        f"Please create a guided {preferred_session} for them."
    )

    # Generate the meditation script using Bedrock
    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": LLM_CONFIG["model_kwargs"]["max_tokens"],
            "temperature": LLM_CONFIG["model_kwargs"]["temperature"],
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_prompt}]
                }
            ]
        })

        response = client.invoke_model(
            body=body,
            modelId=LLM_CONFIG["model_id"],
            accept='application/json',
            contentType='application/json'
        )

        response_body = json.loads(response.get('body').read())
        
        if not response_body.get("content"):
            raise ValueError("LLM response is empty or invalid.")
            
        meditation_advice = response_body.get("content")[0].get("text", "").strip()
        
        if not meditation_advice:
             raise ValueError("LLM returned an empty script.")

    except Exception as e:
        print(f"Error generating content from Bedrock: {e}")
        meditation_advice = f"As your {role}, I invite you to take a moment for yourself. Breathe in, and out. Let this time be for you."

    return meditation_advice