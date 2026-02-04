# 취향 지도 로직
def build_taste_map(payload: dict) -> dict:
    """
    A-7: 취향 지도 생성
    """
    return {
        "clusters": [
            {
                "cluster_id": 0,
                "label": "잔잔한 성장 드라마",
                "movies": ["movie_1", "movie_3"]
            },
            {
                "cluster_id": 1,
                "label": "씁쓸한 로맨스",
                "movies": ["movie_2"]
            }
        ],
        "user_position": {"x": 0.3, "y": 0.7}
    }
