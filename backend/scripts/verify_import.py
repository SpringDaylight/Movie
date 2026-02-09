"""
Verify imported movie data
"""
import sys
from pathlib import Path
from sqlalchemy import func

sys.path.append(str(Path(__file__).resolve().parents[1]))

from db import get_db
from models import Movie, MovieGenre, MovieTag, MovieVector


def verify_import():
    """Verify imported data"""
    print("=" * 60)
    print("Verifying Imported Movie Data")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # Count movies
        movie_count = db.query(Movie).count()
        print(f"\n✓ Total Movies: {movie_count}")
        
        # Count genres
        genre_count = db.query(MovieGenre).count()
        print(f"✓ Total Movie Genres: {genre_count}")
        
        # Count tags
        tag_count = db.query(MovieTag).count()
        print(f"✓ Total Movie Tags: {tag_count}")
        
        # Count vectors
        vector_count = db.query(MovieVector).count()
        print(f"✓ Total Movie Vectors: {vector_count}")
        
        # Show sample movies
        print("\n" + "-" * 60)
        print("Sample Movies (first 5):")
        print("-" * 60)
        
        movies = db.query(Movie).limit(5).all()
        for movie in movies:
            print(f"\n{movie.title} (ID: {movie.id})")
            print(f"  Release: {movie.release}")
            print(f"  Runtime: {movie.runtime} min")
            print(f"  Genres: {', '.join([g.genre for g in movie.genres])}")
            print(f"  Tags: {', '.join([t.tag for t in movie.tags[:5]])}...")
        
        # Show genre distribution
        print("\n" + "-" * 60)
        print("Genre Distribution (top 10):")
        print("-" * 60)
        
        genre_stats = db.query(
            MovieGenre.genre,
            func.count(MovieGenre.id).label('count')
        ).group_by(MovieGenre.genre).order_by(func.count(MovieGenre.id).desc()).limit(10).all()
        
        for genre, count in genre_stats:
            print(f"  {genre}: {count} movies")
        
        print("\n" + "=" * 60)
        print("✓ Verification completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    verify_import()
