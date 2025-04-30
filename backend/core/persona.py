# backend/core/persona.py

def get_persona_prompt(persona: str, seed: str, guess: str) -> str:
    if persona.lower() == "cheery":
        return (
            f"Hey there! In a fun and casual way, tell me: Does '{guess}' beat '{seed}'? "
            "Reply only 'YES' or 'NO'."
        )
    else:  # serious or default
        return (
            f"Strictly respond with 'YES' or 'NO': Does '{guess}' beat '{seed}'?"
        )
