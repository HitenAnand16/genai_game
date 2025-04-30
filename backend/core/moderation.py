# backend/core/moderation.py

BAD_WORDS = [
    "badword1", "badword2", "badword3", "damn", "shit", "fuck",
    # You can add more real offensive words here if needed
]

def is_clean(text: str) -> bool:
    lowered = text.lower()
    return not any(bad_word in lowered for bad_word in BAD_WORDS)
