# 영화 특성 벡터 처리 로직
def process_movie_vector(movie_payload: dict) -> dict:
    """
    A-2: 영화 메타데이터 → 영화 특성 벡터
    """
    return {
        "movie_id": movie_payload.get("movie_id", "dummy_movie"),
        "emotion": ["calm"],
        "narrative": ["growth"],
        "ending": "bittersweet"
    }
