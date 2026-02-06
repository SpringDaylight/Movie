from fastapi import FastAPI, HTTPException

from utils.validator import validate_request

from domain.a1_preference import analyze_preference
from domain.a2_movie_vector import process_movie_vector
from domain.a3_prediction import predict_satisfaction
from domain.a4_explanation import explain_prediction
from domain.a5_emotional_search import emotional_search
from domain.a6_group_simulation import simulate_group
from domain.a7_taste_map import build_taste_map

app = FastAPI()

# In-memory mock data (temporary until DB is decided)
MOVIES = [
    {
        "id": 1,
        "title": "Dummy Movie",
        "genres": ["drama"],
        "category": "popular",
        "overview": "A warm growth story.",
        "release_year": 2024,
    },
    {
        "id": 2,
        "title": "Bright Comedy",
        "genres": ["comedy"],
        "category": "trending",
        "overview": "Light and funny.",
        "release_year": 2022,
    },
]

REVIEWS = [
    {
        "id": 101,
        "movie_id": 1,
        "user_id": "me",
        "rating": 4.5,
        "comment": "Great story and emotions.",
        "likes": 2,
    }
]

COMMENTS = [
    {"id": 201, "review_id": 101, "user_id": "user_1", "comment": "Agree!"}
]

USER = {"id": "me", "name": "Demo User"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze/preference")
def analyze_preference_endpoint(body: dict) -> dict:
    try:
        validate_request("a1_preference_request.json", body)
        return analyze_preference(body)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/movie/vector")
def movie_vector_endpoint(body: dict) -> dict:
    try:
        validate_request("a2_movie_vector_request.json", body)
        return process_movie_vector(body)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/predict/satisfaction")
def predict_satisfaction_endpoint(body: dict) -> dict:
    try:
        validate_request("a3_predict_request.json", body)
        return predict_satisfaction(body)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/explain/prediction")
def explain_prediction_endpoint(body: dict) -> dict:
    try:
        validate_request("a4_explain_request.json", body)
        return explain_prediction(body)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/search/emotional")
def emotional_search_endpoint(body: dict) -> dict:
    try:
        validate_request("a5_search_request.json", body)
        return emotional_search(body)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/group/simulate")
def group_simulate_endpoint(body: dict) -> dict:
    try:
        validate_request("a6_group_request.json", body)
        return simulate_group(body)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/map/taste")
def taste_map_endpoint(body: dict) -> dict:
    try:
        validate_request("a7_map_request.json", body)
        return build_taste_map(body)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ---- Mock API endpoints (no DB yet) ----
@app.get("/api/movies")
def list_movies(
    query: str | None = None,
    genres: str | None = None,
    category: str | None = None,
    sort: str | None = None,
    page: int | None = None,
) -> dict:
    items = MOVIES[:]
    if query:
        items = [m for m in items if query.lower() in m["title"].lower()]
    if genres:
        gset = {g.strip() for g in genres.split(",") if g.strip()}
        items = [m for m in items if gset.intersection(set(m.get("genres", [])))]
    if category:
        items = [m for m in items if m.get("category") == category]
    if sort == "year_desc":
        items.sort(key=lambda x: x.get("release_year", 0), reverse=True)
    if page:
        size = 20
        start = (page - 1) * size
        items = items[start : start + size]
    return {"items": items}


@app.get("/api/movies/{movie_id}")
def get_movie(movie_id: int) -> dict:
    for m in MOVIES:
        if m["id"] == movie_id:
            return m
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/api/movies/{movie_id}/reviews")
def list_movie_reviews(movie_id: int) -> dict:
    items = [r for r in REVIEWS if r["movie_id"] == movie_id]
    return {"items": items}


@app.post("/api/movies/{movie_id}/reviews")
def create_movie_review(movie_id: int, body: dict) -> dict:
    new_id = max([r["id"] for r in REVIEWS] or [100]) + 1
    review = {
        "id": new_id,
        "movie_id": movie_id,
        "user_id": USER["id"],
        "rating": body.get("rating", 0),
        "comment": body.get("comment", ""),
        "likes": 0,
    }
    REVIEWS.append(review)
    return review


@app.get("/api/reviews/{review_id}")
def get_review(review_id: int) -> dict:
    for r in REVIEWS:
        if r["id"] == review_id:
            return r
    raise HTTPException(status_code=404, detail="Review not found")


@app.put("/api/reviews/{review_id}")
def update_review(review_id: int, body: dict) -> dict:
    for r in REVIEWS:
        if r["id"] == review_id:
            r["rating"] = body.get("rating", r["rating"])
            r["comment"] = body.get("comment", r["comment"])
            return r
    raise HTTPException(status_code=404, detail="Review not found")


@app.post("/api/reviews/{review_id}/likes")
def like_review(review_id: int) -> dict:
    for r in REVIEWS:
        if r["id"] == review_id:
            r["likes"] += 1
            return {"likes": r["likes"]}
    raise HTTPException(status_code=404, detail="Review not found")


@app.delete("/api/reviews/{review_id}/likes")
def unlike_review(review_id: int) -> dict:
    for r in REVIEWS:
        if r["id"] == review_id:
            r["likes"] = max(0, r["likes"] - 1)
            return {"likes": r["likes"]}
    raise HTTPException(status_code=404, detail="Review not found")


@app.get("/api/reviews/{review_id}/comments")
def list_comments(review_id: int) -> dict:
    items = [c for c in COMMENTS if c["review_id"] == review_id]
    return {"items": items}


@app.post("/api/reviews/{review_id}/comments")
def create_comment(review_id: int, body: dict) -> dict:
    new_id = max([c["id"] for c in COMMENTS] or [200]) + 1
    comment = {
        "id": new_id,
        "review_id": review_id,
        "user_id": USER["id"],
        "comment": body.get("comment", ""),
    }
    COMMENTS.append(comment)
    return comment


@app.get("/api/users/me")
def get_me() -> dict:
    return USER


@app.get("/api/users/me/reviews")
def list_my_reviews() -> dict:
    items = [r for r in REVIEWS if r["user_id"] == USER["id"]]
    return {"items": items}


@app.get("/api/users/me/taste-analysis")
def taste_analysis_stub() -> dict:
    return {
        "summary": "Taste analysis is not finalized yet.",
        "tags": ["warm", "growth"],
    }
