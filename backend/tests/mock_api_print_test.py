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


def http_get(path: str) -> dict:
    with urlopen(f"{BASE_URL}{path}", timeout=10) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)


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


def print_case(title: str, request_obj, response_obj) -> None:
    print(f"\n=== {title} ===")
    print("Request:")
    print(json.dumps(request_obj, ensure_ascii=False, indent=2))
    print("Response:")
    print(json.dumps(response_obj, ensure_ascii=False, indent=2))

def validate_keys(title: str, response_obj: dict, required_keys: list[str]) -> bool:
    missing = [k for k in required_keys if k not in response_obj]
    if missing:
        print(f"[FAIL] {title} (missing keys: {missing})")
        return False
    print(f"[PASS] {title} (keys: {', '.join(required_keys)})")
    return True


def run_tests() -> None:
    passed = 0
    failed = 0

    movies = http_get("/api/movies")
    print_case("GET /api/movies", {}, movies)
    if validate_keys("GET /api/movies", movies, ["items"]):
        passed += 1
    else:
        failed += 1

    movie = http_get("/api/movies/1")
    print_case("GET /api/movies/1", {}, movie)
    if validate_keys("GET /api/movies/1", movie, ["id", "title", "genres"]):
        passed += 1
    else:
        failed += 1

    movie_reviews = http_get("/api/movies/1/reviews")
    print_case("GET /api/movies/1/reviews", {}, movie_reviews)
    if validate_keys("GET /api/movies/1/reviews", movie_reviews, ["items"]):
        passed += 1
    else:
        failed += 1

    new_review_payload = {"rating": 4.0, "comment": "Nice movie."}
    new_review = http_post("/api/movies/1/reviews", new_review_payload)
    print_case("POST /api/movies/1/reviews", new_review_payload, new_review)
    if validate_keys(
        "POST /api/movies/1/reviews",
        new_review,
        ["id", "movie_id", "user_id", "rating", "comment", "likes"],
    ):
        passed += 1
    else:
        failed += 1

    review_id = new_review.get("id", 101)
    review = http_get(f"/api/reviews/{review_id}")
    print_case(f"GET /api/reviews/{review_id}", {}, review)
    if validate_keys(
        f"GET /api/reviews/{review_id}",
        review,
        ["id", "movie_id", "user_id", "rating", "comment", "likes"],
    ):
        passed += 1
    else:
        failed += 1

    update_payload = {"rating": 4.5, "comment": "Updated review."}
    updated = http_put(f"/api/reviews/{review_id}", update_payload)
    print_case(f"PUT /api/reviews/{review_id}", update_payload, updated)
    if validate_keys(
        f"PUT /api/reviews/{review_id}",
        updated,
        ["id", "movie_id", "user_id", "rating", "comment", "likes"],
    ):
        passed += 1
    else:
        failed += 1

    liked = http_post(f"/api/reviews/{review_id}/likes", {})
    print_case(f"POST /api/reviews/{review_id}/likes", {}, liked)
    if validate_keys(
        f"POST /api/reviews/{review_id}/likes",
        liked,
        ["likes"],
    ):
        passed += 1
    else:
        failed += 1

    unliked = http_delete(f"/api/reviews/{review_id}/likes")
    print_case(f"DELETE /api/reviews/{review_id}/likes", {}, unliked)
    if validate_keys(
        f"DELETE /api/reviews/{review_id}/likes",
        unliked,
        ["likes"],
    ):
        passed += 1
    else:
        failed += 1

    comments = http_get(f"/api/reviews/{review_id}/comments")
    print_case(f"GET /api/reviews/{review_id}/comments", {}, comments)
    if validate_keys(
        f"GET /api/reviews/{review_id}/comments",
        comments,
        ["items"],
    ):
        passed += 1
    else:
        failed += 1

    comment_payload = {"comment": "Agree!"}
    comment = http_post(f"/api/reviews/{review_id}/comments", comment_payload)
    print_case(f"POST /api/reviews/{review_id}/comments", comment_payload, comment)
    if validate_keys(
        f"POST /api/reviews/{review_id}/comments",
        comment,
        ["id", "review_id", "user_id", "comment"],
    ):
        passed += 1
    else:
        failed += 1

    me = http_get("/api/users/me")
    print_case("GET /api/users/me", {}, me)
    if validate_keys("GET /api/users/me", me, ["id", "name"]):
        passed += 1
    else:
        failed += 1

    my_reviews = http_get("/api/users/me/reviews")
    print_case("GET /api/users/me/reviews", {}, my_reviews)
    if validate_keys("GET /api/users/me/reviews", my_reviews, ["items"]):
        passed += 1
    else:
        failed += 1

    taste = http_get("/api/users/me/taste-analysis")
    print_case("GET /api/users/me/taste-analysis", {}, taste)
    if validate_keys("GET /api/users/me/taste-analysis", taste, ["summary", "tags"]):
        passed += 1
    else:
        failed += 1

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
