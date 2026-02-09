import json
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
ROOT_DIR = Path(__file__).resolve().parents[1]


def http_post(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=10) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)

def http_put(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="PUT",
    )
    with urlopen(req, timeout=10) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)


def http_delete(path: str) -> dict:
    req = Request(f"{BASE_URL}{path}", method="DELETE")
    with urlopen(req, timeout=10) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)


def http_get(path: str) -> dict:
    with urlopen(f"{BASE_URL}{path}", timeout=10) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)


def wait_for_health(timeout_sec: int = 20) -> None:
    start = time.time()
    while time.time() - start < timeout_sec:
        try:
            data = http_get("/health")
            if data.get("status") == "ok":
                return
        except URLError:
            pass
        time.sleep(0.5)
    raise RuntimeError("Server health check failed")


def assert_has_keys(obj: dict, keys: list[str]) -> None:
    missing = [k for k in keys if k not in obj]
    if missing:
        raise AssertionError(f"Missing keys: {missing}")


def print_case(title: str, payload: dict, response: dict) -> None:
    print(f"\n=== {title} ===")
    print("Request:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("Response:")
    print(json.dumps(response, ensure_ascii=False, indent=2))

def validate_keys(title: str, response_obj: dict, required_keys: list[str]) -> tuple[int, int]:
    missing = [k for k in required_keys if k not in response_obj]
    if missing:
        print(f"[FAIL] {title} (missing keys: {missing})")
        return (0, 1)
    print(f"[PASS] {title} (keys: {', '.join(required_keys)})")
    return (1, 0)


def run_tests() -> None:
    passed = 0
    failed = 0

    # A1 -> user_profile
    a1_payload = {
        "text": "감동적인 성장 드라마 좋아해요",
        "dislikes": "무서워요,어두운 분위기예요",
    }
    a1 = http_post("/analyze/preference", a1_payload)
    print_case("A1 /analyze/preference", a1_payload, a1)
    assert_has_keys(
        a1,
        [
            "user_text",
            "emotion_scores",
            "narrative_traits",
            "ending_preference",
            "dislike_tags",
        ],
    )
    p, f = validate_keys(
        "A1 /analyze/preference",
        a1,
        ["user_text", "emotion_scores", "narrative_traits", "ending_preference", "dislike_tags"],
    )
    passed += p
    failed += f

    # A2 -> movie_profile
    a2_payload = {
        "movie_id": 1,
        "title": "Dummy Movie",
        "overview": "감동적인 성장 서사를 가진 영화",
        "genres": ["드라마"],
        "keywords": ["성장", "감동"],
        "directors": ["감독A"],
        "cast": ["배우A", "배우B"],
    }
    a2 = http_post("/movie/vector", a2_payload)
    print_case("A2 /movie/vector", a2_payload, a2)
    assert_has_keys(
        a2,
        [
            "movie_id",
            "title",
            "emotion_scores",
            "narrative_traits",
            "direction_mood",
            "character_relationship",
            "ending_preference",
            "embedding_text",
            "embedding",
        ],
    )
    p, f = validate_keys(
        "A2 /movie/vector",
        a2,
        [
            "movie_id",
            "title",
            "emotion_scores",
            "narrative_traits",
            "direction_mood",
            "character_relationship",
            "ending_preference",
            "embedding_text",
            "embedding",
        ],
    )
    passed += p
    failed += f

    # A3 uses outputs from A1/A2
    a3_payload = {
        "user_profile": {
            "emotion_scores": a1.get("emotion_scores", {}),
            "narrative_traits": a1.get("narrative_traits", {}),
            "ending_preference": a1.get("ending_preference", {}),
            "dislike_tags": a1.get("dislike_tags", []),
            "boost_tags": ["감동적이에요"],
        },
        "movie_profile": {
            "movie_id": a2.get("movie_id"),
            "title": a2.get("title", "Unknown"),
            "emotion_scores": a2.get("emotion_scores", {}),
            "narrative_traits": a2.get("narrative_traits", {}),
            "ending_preference": a2.get("ending_preference", {}),
        },
        "boost_tags": ["감동적이에요"],
    }
    a3 = http_post("/predict/satisfaction", a3_payload)
    print_case("A3 /predict/satisfaction", a3_payload, a3)
    assert_has_keys(
        a3,
        ["movie_id", "title", "probability", "confidence", "raw_score", "match_rate", "breakdown"],
    )
    p, f = validate_keys(
        "A3 /predict/satisfaction",
        a3,
        ["movie_id", "title", "probability", "confidence", "raw_score", "match_rate", "breakdown"],
    )
    passed += p
    failed += f

    # A4 uses output from A3
    a4_payload = {
        "movie_title": a3.get("title", "Unknown"),
        "match_rate": a3.get("match_rate", 70.0),
        "key_factors": [
            {"category": "emotion", "tag": "감동적이에요", "score": 0.8},
            {"category": "story_flow", "tag": "성장", "score": 0.6},
        ],
        "user_text": a1.get("user_text", ""),
    }
    a4 = http_post("/explain/prediction", a4_payload)
    print_case("A4 /explain/prediction", a4_payload, a4)
    assert_has_keys(
        a4,
        ["movie_title", "match_rate", "explanation", "key_factors", "disclaimer"],
    )
    p, f = validate_keys(
        "A4 /explain/prediction",
        a4,
        ["movie_title", "match_rate", "explanation", "key_factors", "disclaimer"],
    )
    passed += p
    failed += f

    # A5 standalone search (no dependency)
    a5_payload = {
        "text": "가볍고 밝은 영화 추천",
        "genres": ["코미디"],
        "year_from": 2020,
    }
    a5 = http_post("/search/emotional", a5_payload)
    print_case("A5 /search/emotional", a5_payload, a5)
    assert_has_keys(a5, ["intent", "expanded_query", "hybrid_query"])
    p, f = validate_keys(
        "A5 /search/emotional",
        a5,
        ["intent", "expanded_query", "hybrid_query"],
    )
    passed += p
    failed += f

    # A6 uses A1 user profile + A2 movie profile
    a6_payload = {
        "members": [
            {
                "user_id": "user_1",
                "profile": {
                    "emotion_scores": a1.get("emotion_scores", {}),
                    "narrative_traits": a1.get("narrative_traits", {}),
                    "ending_preference": a1.get("ending_preference", {}),
                },
                "likes": ["감동적이에요"],
                "dislikes": a1.get("dislike_tags", []),
            },
            {
                "user_id": "user_2",
                "profile": {
                    "emotion_scores": {"잔잔해요": 0.8},
                    "narrative_traits": {"관계": 0.5},
                    "ending_preference": {"happy": 0.3, "open": 0.4, "bittersweet": 0.3},
                },
                "likes": ["잔잔해요"],
                "dislikes": [],
            },
        ],
        "movie_profile": {
            "movie_id": a2.get("movie_id"),
            "title": a2.get("title", "Unknown"),
            "emotion_scores": a2.get("emotion_scores", {}),
            "narrative_traits": a2.get("narrative_traits", {}),
            "ending_preference": a2.get("ending_preference", {}),
        },
        "penalty_weight": 0.7,
        "boost_weight": 0.5,
    }
    a6 = http_post("/group/simulate", a6_payload)
    print_case("A6 /group/simulate", a6_payload, a6)
    assert_has_keys(a6, ["group_score", "members", "comment"])
    p, f = validate_keys(
        "A6 /group/simulate",
        a6,
        ["group_score", "members", "comment"],
    )
    passed += p
    failed += f

    # A7 uses user text
    a7_payload = {
        "user_text": a1.get("user_text", "잔잔한 힐링 영화 좋아해요"),
        "k": 8,
        "limit": 50,
    }
    a7 = http_post("/map/taste", a7_payload)
    print_case("A7 /map/taste", a7_payload, a7)
    assert_has_keys(a7, ["clusters", "user_location"])
    p, f = validate_keys(
        "A7 /map/taste",
        a7,
        ["clusters", "user_location"],
    )
    passed += p
    failed += f

    # Mock REST APIs
    movies = http_get("/api/movies")
    print_case("GET /api/movies", {}, movies)
    p, f = validate_keys("GET /api/movies", movies, ["items"])
    passed += p
    failed += f

    movie = http_get("/api/movies/1")
    print_case("GET /api/movies/1", {}, movie)
    p, f = validate_keys("GET /api/movies/1", movie, ["id", "title", "genres"])
    passed += p
    failed += f

    movie_reviews = http_get("/api/movies/1/reviews")
    print_case("GET /api/movies/1/reviews", {}, movie_reviews)
    p, f = validate_keys("GET /api/movies/1/reviews", movie_reviews, ["items"])
    passed += p
    failed += f

    new_review_payload = {"rating": 4.0, "comment": "Nice movie."}
    new_review = http_post("/api/movies/1/reviews", new_review_payload)
    print_case("POST /api/movies/1/reviews", new_review_payload, new_review)
    p, f = validate_keys(
        "POST /api/movies/1/reviews",
        new_review,
        ["id", "movie_id", "user_id", "rating", "comment", "likes"],
    )
    passed += p
    failed += f

    review_id = new_review.get("id", 101)
    review = http_get(f"/api/reviews/{review_id}")
    print_case(f"GET /api/reviews/{review_id}", {}, review)
    p, f = validate_keys(
        f"GET /api/reviews/{review_id}",
        review,
        ["id", "movie_id", "user_id", "rating", "comment", "likes"],
    )
    passed += p
    failed += f

    update_payload = {"rating": 4.5, "comment": "Updated review."}
    updated = http_put(f"/api/reviews/{review_id}", update_payload)
    print_case(f"PUT /api/reviews/{review_id}", update_payload, updated)
    p, f = validate_keys(
        f"PUT /api/reviews/{review_id}",
        updated,
        ["id", "movie_id", "user_id", "rating", "comment", "likes"],
    )
    passed += p
    failed += f

    liked = http_post(f"/api/reviews/{review_id}/likes", {})
    print_case(f"POST /api/reviews/{review_id}/likes", {}, liked)
    p, f = validate_keys(f"POST /api/reviews/{review_id}/likes", liked, ["likes"])
    passed += p
    failed += f

    unliked = http_delete(f"/api/reviews/{review_id}/likes")
    print_case(f"DELETE /api/reviews/{review_id}/likes", {}, unliked)
    p, f = validate_keys(f"DELETE /api/reviews/{review_id}/likes", unliked, ["likes"])
    passed += p
    failed += f

    comments = http_get(f"/api/reviews/{review_id}/comments")
    print_case(f"GET /api/reviews/{review_id}/comments", {}, comments)
    p, f = validate_keys(f"GET /api/reviews/{review_id}/comments", comments, ["items"])
    passed += p
    failed += f

    comment_payload = {"comment": "Agree!"}
    comment = http_post(f"/api/reviews/{review_id}/comments", comment_payload)
    print_case(f"POST /api/reviews/{review_id}/comments", comment_payload, comment)
    p, f = validate_keys(
        f"POST /api/reviews/{review_id}/comments",
        comment,
        ["id", "review_id", "user_id", "comment"],
    )
    passed += p
    failed += f

    me = http_get("/api/users/me")
    print_case("GET /api/users/me", {}, me)
    p, f = validate_keys("GET /api/users/me", me, ["id", "name"])
    passed += p
    failed += f

    my_reviews = http_get("/api/users/me/reviews")
    print_case("GET /api/users/me/reviews", {}, my_reviews)
    p, f = validate_keys("GET /api/users/me/reviews", my_reviews, ["items"])
    passed += p
    failed += f

    taste = http_get("/api/users/me/taste-analysis")
    print_case("GET /api/users/me/taste-analysis", {}, taste)
    p, f = validate_keys("GET /api/users/me/taste-analysis", taste, ["summary", "tags"])
    passed += p
    failed += f

    print(f"\nSummary: {passed} passed, {failed} failed")


def main() -> None:
    server = None
    try:
        server = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
            ],
            cwd=str(ROOT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        wait_for_health()
        run_tests()
    finally:
        if server is not None:
            server.terminate()
            try:
                server.wait(timeout=5)
            except Exception:
                server.kill()


if __name__ == "__main__":
    main()
