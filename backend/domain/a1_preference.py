def analyze_preference(payload: dict) -> dict:
    """
    A-1: 사용자 텍스트 -> 취향 벡터
    """
    text = payload.get("text", "")
    dislikes_text = payload.get("dislikes", "")
    dislike_tags = []
    if isinstance(dislikes_text, str) and dislikes_text.strip():
        dislike_tags = [t.strip() for t in dislikes_text.split(",") if t.strip()]
    return {
        "user_text": text,
        "emotion_scores": {
            "warm": 0.6,
            "calm": 0.3,
            "sad": 0.1,
        },
        "narrative_traits": {
            "relationship": 0.7,
            "growth": 0.3,
        },
        "ending_preference": {
            "happy": 0.2,
            "open": 0.6,
            "bittersweet": 0.2,
        },
        "dislike_tags": dislike_tags,
    }
