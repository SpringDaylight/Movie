# 감성 검색 로직
def emotional_search(query: str) -> dict:
    """
    A-5: 자연어 감성 검색
    """
    return {
        "query": query,
        "results": [
            {
                "movie_id": "movie_1",
                "title": "Dummy Movie 1",
                "emotion": ["calm", "sad"]
            },
            {
                "movie_id": "movie_2",
                "title": "Dummy Movie 2",
                "emotion": ["warm"]
            }
        ]
    }
