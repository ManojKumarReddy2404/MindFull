def select_roles(emotion_tags: list) -> list:
    # Simple logic to select roles based on emotion tags
    selected_roles = []

    if "anxious" in emotion_tags or "stressed" in emotion_tags:
        selected_roles.append("Calm_Guide")
    if "tired" in emotion_tags:
        selected_roles.append("Energy_Coach")
    if "happy" in emotion_tags:
        selected_roles.append("Joy_Amplifier")
    if "sad" in emotion_tags:
        selected_roles.append("Comfort_Provider")

    # Default role if no specific emotion tag matches
    if not selected_roles:
        selected_roles.append("General_Zen_Master")

    return selected_roles 