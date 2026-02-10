"""
Import movie data from movies_dataset_final.json to database
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from db import engine, get_db
from models import Movie, MovieGenre, MovieTag, MovieVector


def parse_date(date_str):
    """Parse date string to date object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return None


def import_movies(json_path: str):
    """Import movies from JSON file to database"""
    
    print("=" * 60)
    print("Importing Movies from JSON to Database")
    print("=" * 60)
    
    # Load JSON data
    print(f"\n[1] Loading JSON file: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        movies_data = json.load(f)
    print(f"✓ Loaded {len(movies_data)} movies")
    
    # Get database session
    print("\n[2] Connecting to database...")
    db = next(get_db())
    
    try:
        imported_count = 0
        skipped_count = 0
        
        print("\n[3] Importing movies...")
        for movie_data in movies_data:
            movie_id = movie_data.get('id')
            
            # Check if movie already exists
            existing = db.query(Movie).filter(Movie.id == movie_id).first()
            if existing:
                print(f"  ⊘ Skipped: {movie_data.get('title')} (ID: {movie_id}) - already exists")
                skipped_count += 1
                continue
            
            # Create Movie
            movie = Movie(
                id=movie_id,
                title=movie_data.get('title'),
                release=parse_date(movie_data.get('release_date')),
                runtime=movie_data.get('runtime'),
                synopsis=movie_data.get('overview'),
                poster_url=movie_data.get('poster_path')
            )
            db.add(movie)
            
            # Create MovieGenres
            for genre in movie_data.get('genres', []):
                movie_genre = MovieGenre(
                    movie_id=movie_id,
                    genre=genre
                )
                db.add(movie_genre)
            
            # Create MovieTags (from keywords)
            for keyword in movie_data.get('keywords', []):
                movie_tag = MovieTag(
                    movie_id=movie_id,
                    tag=keyword
                )
                db.add(movie_tag)
            
            # Create MovieVector (empty for now)
            movie_vector = MovieVector(
                movie_id=movie_id,
                emotion_scores={},
                narrative_traits={},
                ending_preference={},
                embedding_vector=[]
            )
            db.add(movie_vector)
            
            imported_count += 1
            print(f"  ✓ Imported: {movie_data.get('title')} (ID: {movie_id})")
        
        # Commit all changes
        print("\n[4] Committing to database...")
        db.commit()
        print("✓ All changes committed")
        
        print("\n" + "=" * 60)
        print(f"✓ Import completed!")
        print(f"  Imported: {imported_count} movies")
        print(f"  Skipped: {skipped_count} movies (already exist)")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during import: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


def main():
    """Main function"""
    # Path to JSON file
    json_path = Path(__file__).resolve().parents[2] / "model_sample" / "movies_dataset_final.json"
    
    if not json_path.exists():
        print(f"✗ JSON file not found: {json_path}")
        sys.exit(1)
    
    import_movies(str(json_path))


if __name__ == "__main__":
    main()
