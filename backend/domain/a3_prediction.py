# 만족 확률 계산
def predict_satisfaction(payload: dict) -> dict:
    """
    A-3: 사용자 + 영화 -> 매칭 점수
    """
    user_profile = payload.get("user_profile", {})
    movie_profile = payload.get("movie_profile", {})
    movie_id = movie_profile.get("movie_id")
    title = movie_profile.get("title", "Unknown")

    def align_vector(a: dict, keys: list) -> list:
        return [float(a.get(k, 0.0)) for k in keys]

    def cosine_sim(a: list, b: list) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = sum(x * x for x in a) ** 0.5
        nb = sum(y * y for y in b) ** 0.5
        if na == 0.0 or nb == 0.0:
            return 0.0
        return dot / (na * nb)

    def sigmoid(x: float, k: float = 8.0, x0: float = 0.5) -> float:
        return 1.0 / (1.0 + pow(2.718281828, -k * (x - x0)))

    e_keys = list(user_profile.get("emotion_scores", {}).keys())
    n_keys = list(user_profile.get("narrative_traits", {}).keys())
    d_keys = list(user_profile.get("ending_preference", {}).keys())

    e_score = cosine_sim(
        align_vector(user_profile.get("emotion_scores", {}), e_keys),
        align_vector(movie_profile.get("emotion_scores", {}), e_keys),
    )
    n_score = cosine_sim(
        align_vector(user_profile.get("narrative_traits", {}), n_keys),
        align_vector(movie_profile.get("narrative_traits", {}), n_keys),
    )
    d_score = cosine_sim(
        align_vector(user_profile.get("ending_preference", {}), d_keys),
        align_vector(movie_profile.get("ending_preference", {}), d_keys),
    )

    dislike_tags = payload.get("dislike_tags")
    if not isinstance(dislike_tags, list):
        dislike_tags = user_profile.get("dislike_tags", [])
    if not isinstance(dislike_tags, list):
        dislike_tags = []

    penalty = 0.0
    movie_emotions = movie_profile.get("emotion_scores", {})
    for tag in dislike_tags:
        if tag in movie_emotions:
            penalty += float(movie_emotions.get(tag, 0.0))

    penalty_weight = 0.7
    raw_score = (0.5 * e_score) + (0.3 * n_score) + (0.2 * d_score) - (penalty_weight * penalty)
    match_rate = sigmoid(raw_score) * 100.0

    return {
        "movie_id": movie_id,
        "title": title,
        "raw_score": round(raw_score, 4),
        "match_rate": round(match_rate, 2),
    }
