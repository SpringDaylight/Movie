# 설명 생성 로직
def explain_prediction(payload: dict) -> dict:
    """
    A-4: 예측 결과 → 자연어 설명
    """
    return {
        "summary": "이 영화는 당신이 선호하는 관계 중심 서사와 잔잔한 정서를 가지고 있습니다.",
        "reasons": [
            "관계 중심의 이야기 구조",
            "여운이 남는 열린 결말"
        ],
        "notice": "이 결과는 확률 기반 예측입니다."
    }
