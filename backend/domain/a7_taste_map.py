# 취향 지도 로직
def build_taste_map(payload: dict) -> dict:
    """
    A-7: 취향 지도 출력
    """
    clusters = [
        {"cluster_id": 0, "label": "Warm·Growth", "count": 12},
        {"cluster_id": 1, "label": "Calm·Healing", "count": 8},
    ]

    return {
        "clusters": clusters,
        "user_location": {
            "x": 0.3,
            "y": 0.7,
            "nearest_cluster": 0,
            "cluster_label": clusters[0]["label"],
        },
    }
