import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from sqlalchemy import text

sys.path.append(str(Path(__file__).resolve().parents[1]))

from db import SessionLocal
from models import Movie, MovieCast, MovieDirector, MovieGenre, MovieKeyword, User


DEFAULT_DATASET = (
    Path(__file__).resolve().parents[3]
    / "taste-simulation-engine"
    / "model_sample"
    / "movies_dataset_final.json"
)


def _load_json(path: Path) -> list[dict]:
    for encoding in ("utf-8", "utf-8-sig", "cp949"):
        try:
            with path.open("r", encoding=encoding) as f:
                return json.load(f)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Failed to decode dataset file: {path}")


def _parse_date(value: str | None):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _normalize_str_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    out = []
    for item in value:
        if not isinstance(item, str):
            continue
        cleaned = item.strip()
        if cleaned:
            out.append(cleaned)
    return out


def _category(item: dict) -> str:
    vote_count = int(item.get("vote_count") or 0)
    vote_average = float(item.get("vote_average") or 0.0)
    if vote_count >= 1000 or vote_average >= 7.5:
        return "popular"
    return "catalog"


def seed_movies(dataset_path: Path) -> None:
    data = _load_json(dataset_path)
    db = SessionLocal()
    try:
        db.execute(text("select 1"))

        user = db.query(User).filter(User.id == "me").first()
        if not user:
            db.add(User(id="me", name="Demo User"))
            db.commit()

        loaded = 0
        for item in data:
            movie_id = item.get("id")
            title = item.get("title")
            if not movie_id or not title:
                continue

            movie = db.query(Movie).filter(Movie.id == int(movie_id)).first()
            if not movie:
                movie = Movie(id=int(movie_id), title=str(title))
                db.add(movie)

            movie.title = str(title)
            movie.original_title = item.get("original_title")
            movie.overview = item.get("overview")
            movie.runtime = item.get("runtime")
            movie.release_date = _parse_date(item.get("release_date"))
            movie.release_year = (
                movie.release_date.year if movie.release_date else None
            )
            movie.poster_url = item.get("poster_path")
            movie.vote_average = float(item.get("vote_average") or 0.0)
            movie.vote_count = int(item.get("vote_count") or 0)
            movie.category = _category(item)

            db.query(MovieGenre).filter(MovieGenre.movie_id == int(movie_id)).delete()
            db.query(MovieKeyword).filter(MovieKeyword.movie_id == int(movie_id)).delete()
            db.query(MovieDirector).filter(MovieDirector.movie_id == int(movie_id)).delete()
            db.query(MovieCast).filter(MovieCast.movie_id == int(movie_id)).delete()

            for genre in _normalize_str_list(item.get("genres")):
                db.add(MovieGenre(movie_id=int(movie_id), genre=genre))
            for keyword in _normalize_str_list(item.get("keywords")):
                db.add(MovieKeyword(movie_id=int(movie_id), keyword=keyword))
            for director in _normalize_str_list(item.get("directors")):
                db.add(MovieDirector(movie_id=int(movie_id), name=director))
            for cast_name in _normalize_str_list(item.get("cast")):
                db.add(MovieCast(movie_id=int(movie_id), name=cast_name))

            loaded += 1

        db.commit()
        print(f"Seed complete: {loaded} movies loaded from {dataset_path}")
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        default=str(DEFAULT_DATASET),
        help="Path to movies_dataset_final.json",
    )
    args = parser.parse_args()
    seed_movies(Path(args.dataset))


if __name__ == "__main__":
    main()
