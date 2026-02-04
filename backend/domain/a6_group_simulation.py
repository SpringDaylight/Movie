# 그룹 취향 합성
def simulate_group(payload: dict) -> dict:
    """
    A-6: 그룹 취향 → 그룹 만족 확률
    """
    return {
        "group_score": 0.65,
        "members": [
            {"user_id": "user_1", "score": 0.7},
            {"user_id": "user_2", "score": 0.6}
        ],
        "comment": "대체로 무난하게 모두가 만족할 가능성이 있습니다."
    }
