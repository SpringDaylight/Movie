from decimal import Decimal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc

from db import SessionLocal
from models import (
    Movie,
    MovieGenre,
    MovieTag,
    Review,
    Comment,
    ReviewLike,
    TasteAnalysis,
    User,
)
from utils.validator import validate_request

from domain.a1_preference import analyze_preference
from domain.a2_movie_vector import process_movie_vector
from domain.a3_prediction import predict_satisfaction
from domain.a4_explanation import explain_prediction
from domain.a5_emotional_search import emotional_search
from domain.a6_group_simulation import simulate_group
from domain.a7_taste_map import build_taste_map

app = FastAPI(
    title="Movie Recommendation API",
    description="정서·서사 기반 영화 취향 시뮬레이션 & 감성 검색 서비스",
    version="1.0.0"
)

# CORS middleware - 프론트엔드 연결을 위해 필수
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEFAULT_USER_ID = "me"
DEFAULT_USER_NAME = "Demo User"


def _to_float(value: Decimal | float | int | None) -> float | None:
    if value is None:
        return None
    return float(value)


def _ensure_default_user(db) -> User:
    user = db.query(User).filter(User.id == DEFAULT_USER_ID).first()
    if user:
        return user
    user = User(id=DEFAULT_USER_ID, name=DEFAULT_USER_NAME)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _serialize_movie(db, movie: Movie) -> dict:
    genres = [
        row.genre
        for row in db.query(MovieGenre).filter(MovieGenre.movie_id == movie.id).all()
    ]
    tags = [
        row.tag
        for row in db.query(MovieTag).filter(MovieTag.movie_id == movie.id).all()
    ]
    return {
        "id": movie.id,
        "title": movie.title,
        "genres": genres,
        "tags": tags,
        "synopsis": movie.synopsis,
        "release": movie.release.isoformat() if movie.release else None,
        "runtime": movie.runtime,
        "poster_url": movie.poster_url,
    }


def _serialize_review(review: Review) -> dict:
    return {
        "id": review.id,
        "movie_id": review.movie_id,
        "user_id": review.user_id,
        "rating": _to_float(review.rating),
        "content": review.content,
    }


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


@app.get("/api/movies")
def list_movies(
    query: str | None = None,
    genres: str | None = None,
    category: str | None = None,
    sort: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    db = SessionLocal()
    try:
        q = db.query(Movie)
        if query:
            q = q.filter(Movie.title.ilike(f"%{query}%"))

        items = q.all()
        total_before_filter = len(items)
        
        if genres:
            want = {g.strip() for g in genres.split(",") if g.strip()}
            filtered = []
            for movie in items:
                movie_genres = {
                    row.genre
                    for row in db.query(MovieGenre)
                    .filter(MovieGenre.movie_id == movie.id)
                    .all()
                }
                if want.intersection(movie_genres):
                    filtered.append(movie)
            items = filtered

        total = len(items)

        if sort == "latest":
            items = sorted(items, key=lambda m: m.release or "", reverse=True)
        elif sort == "popular":
            # For popular, just use default order for now
            items = sorted(items, key=lambda m: m.id)
        else:
            items = sorted(items, key=lambda m: m.id)

        # Pagination
        start = (page - 1) * page_size
        items = items[start : start + page_size]

        return {
            "movies": [_serialize_movie(db, movie) for movie in items],
            "total": total,
            "page": page,
            "page_size": page_size
        }
    finally:
        db.close()


@app.get("/api/movies/{movie_id}")
def get_movie(movie_id: int) -> dict:
    db = SessionLocal()
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return _serialize_movie(db, movie)
    finally:
        db.close()


@app.get("/api/movies/{movie_id}/reviews")
def list_movie_reviews(movie_id: int) -> dict:
    db = SessionLocal()
    try:
        items = (
            db.query(Review)
            .filter(Review.movie_id == movie_id)
            .order_by(desc(Review.created_at), desc(Review.id))
            .all()
        )
        return {
            "reviews": [_serialize_review(review) for review in items],
            "total": len(items)
        }
    finally:
        db.close()


@app.post("/api/movies/{movie_id}/reviews")
def create_movie_review(movie_id: int, body: dict) -> dict:
    db = SessionLocal()
    try:
        _ensure_default_user(db)
        if not db.query(Movie).filter(Movie.id == movie_id).first():
            raise HTTPException(status_code=404, detail="Movie not found")
        review = Review(
            movie_id=movie_id,
            user_id=DEFAULT_USER_ID,
            rating=body.get("rating", 0),
            content=body.get("content", ""),
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        return _serialize_review(review)
    finally:
        db.close()


@app.get("/api/reviews/{review_id}")
def get_review(review_id: int) -> dict:
    db = SessionLocal()
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return _serialize_review(review)
    finally:
        db.close()


@app.put("/api/reviews/{review_id}")
def update_review(review_id: int, body: dict) -> dict:
    db = SessionLocal()
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        if "rating" in body:
            review.rating = body["rating"]
        if "content" in body:
            review.content = body["content"]
        db.commit()
        db.refresh(review)
        return _serialize_review(review)
    finally:
        db.close()


@app.post("/api/reviews/{review_id}/likes")
def like_review(review_id: int) -> dict:
    db = SessionLocal()
    try:
        _ensure_default_user(db)
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        existing = (
            db.query(ReviewLike)
            .filter(ReviewLike.review_id == review_id, ReviewLike.user_id == DEFAULT_USER_ID)
            .first()
        )
        if not existing:
            db.add(ReviewLike(review_id=review_id, user_id=DEFAULT_USER_ID, is_like=True))
            db.commit()
        
        # Count likes
        likes_count = db.query(ReviewLike).filter(ReviewLike.review_id == review_id, ReviewLike.is_like == True).count()
        return {"likes": likes_count}
    finally:
        db.close()


@app.delete("/api/reviews/{review_id}/likes")
def unlike_review(review_id: int) -> dict:
    db = SessionLocal()
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        existing = (
            db.query(ReviewLike)
            .filter(ReviewLike.review_id == review_id, ReviewLike.user_id == DEFAULT_USER_ID)
            .first()
        )
        if existing:
            db.delete(existing)
            db.commit()
        
        # Count likes
        likes_count = db.query(ReviewLike).filter(ReviewLike.review_id == review_id, ReviewLike.is_like == True).count()
        return {"likes": likes_count}
    finally:
        db.close()


@app.get("/api/reviews/{review_id}/comments")
def list_comments(review_id: int) -> dict:
    db = SessionLocal()
    try:
        items = (
            db.query(Comment)
            .filter(Comment.review_id == review_id)
            .order_by(desc(Comment.created_at), desc(Comment.id))
            .all()
        )
        return {
            "items": [
                {
                    "id": c.id,
                    "review_id": c.review_id,
                    "user_id": c.user_id,
                    "content": c.content,
                }
                for c in items
            ]
        }
    finally:
        db.close()


@app.post("/api/reviews/{review_id}/comments")
def create_comment(review_id: int, body: dict) -> dict:
    db = SessionLocal()
    try:
        _ensure_default_user(db)
        if not db.query(Review).filter(Review.id == review_id).first():
            raise HTTPException(status_code=404, detail="Review not found")
        comment = Comment(
            review_id=review_id,
            user_id=DEFAULT_USER_ID,
            content=body.get("content", ""),
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return {
            "id": comment.id,
            "review_id": comment.review_id,
            "user_id": comment.user_id,
            "content": comment.content,
        }
    finally:
        db.close()


@app.get("/api/users/me")
def get_me() -> dict:
    db = SessionLocal()
    try:
        user = _ensure_default_user(db)
        return {"id": user.id, "name": user.name, "avatar_text": user.avatar_text}
    finally:
        db.close()


@app.get("/api/users/me/reviews")
def list_my_reviews() -> dict:
    db = SessionLocal()
    try:
        _ensure_default_user(db)
        items = (
            db.query(Review)
            .filter(Review.user_id == DEFAULT_USER_ID)
            .order_by(desc(Review.created_at), desc(Review.id))
            .all()
        )
        return {
            "reviews": [_serialize_review(review) for review in items],
            "total": len(items)
        }
    finally:
        db.close()


@app.get("/api/users/me/taste-analysis")
def taste_analysis_stub() -> dict:
    db = SessionLocal()
    try:
        _ensure_default_user(db)
        profile = db.query(TasteAnalysis).filter(TasteAnalysis.user_id == DEFAULT_USER_ID).first()
        if not profile:
            return {"summary": "Taste profile is not generated yet."}
        return {
            "summary": profile.summary_text or "Taste profile loaded from database.",
        }
    finally:
        db.close()
