# 영화 특성 벡터 처리 로직
def process_movie_vector(movie_payload: dict) -> dict:
    """
    A-2: 영화 입력 -> 영화 프로필
    """
    movie_id = movie_payload.get("movie_id", "dummy_movie")
    title = movie_payload.get("title", "Dummy Movie")
    profile = {
        "movie_id": movie_id,
        "title": title,
        "emotion_scores": {
            "warm": 0.4,
            "calm": 0.4,
            "excited": 0.2,
        },
        "narrative_traits": {
            "growth": 0.6,
            "relationship": 0.4,
        },
        "direction_mood": {
            "bright": 0.5,
            "stylish": 0.5,
        },
        "character_relationship": {
            "relationship_focus": 0.7,
            "ensemble": 0.3,
        },
        "ending_preference": {
            "happy": 0.3,
            "open": 0.4,
            "bittersweet": 0.3,
        },
    }

    # 최소 임베딩 자리표시자
    profile["embedding_text"] = f"Title: {title}. Emotions: warm, calm. Narrative: growth."
    profile["embedding"] = []
    return profile
