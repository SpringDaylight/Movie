"""
Check if genres are imported in the database
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from db import get_db
from models import Movie, MovieGenre
from sqlalchemy import func

def check_genres():
    db = next(get_db())
    
    try:
        # Count movies
        movie_count = db.query(Movie).count()
        print(f"Total movies: {movie_count}")
        
        # Count genres
        genre_count = db.query(MovieGenre).count()
        print(f"Total genre records: {genre_count}")
        
        # Get sample movie with genres
        movie = db.query(Movie).first()
        if movie:
            print(f"\nSample movie: {movie.title} (ID: {movie.id})")
            genres = db.query(MovieGenre).filter(MovieGenre.movie_id == movie.id).all()
            print(f"Genres: {[g.genre for g in genres]}")
        
        # Get genre distribution
        print("\nGenre distribution:")
        genre_stats = db.query(
            MovieGenre.genre, 
            func.count(MovieGenre.id).label('count')
        ).group_by(MovieGenre.genre).order_by(func.count(MovieGenre.id).desc()).all()
        
        for genre, count in genre_stats[:20]:
            print(f"  {genre}: {count}")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_genres()
