def analyze_preference(text: str) -> dict:
    """
    A-1: 사용자 텍스트 → 취향 벡터
    """
    return {
        "emotion": ["warm"],
        "narrative": ["relationship"],
        "ending": "open",
        "confidence": 0.5
    }
