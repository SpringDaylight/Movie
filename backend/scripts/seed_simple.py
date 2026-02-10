"""
Simple seed script for dummy data
"""
import sys
import random
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.append(str(Path(__file__).resolve().parents[1]))

from db import get_db
from models import User, Review, TasteAnalysis, Comment, ReviewLike, Movie


def main():
    print("Seeding data...")
    db = next(get_db())
    
    try:
        # 1. Users
        users_data = [
            {"id": f"user{str(i).zfill(3)}", "name": f"사용자{i}", "avatar_text": f"영화광{i}"}
            for i in range(1, 11)
        ]
        
        for user_data in users_data:
            if not db.query(User).filter(User.id == user_data["id"]).first():
                db.add(User(**user_data))
        db.commit()
        print(f"✓ Users: {db.query(User).count()}")
        
        # 2. Reviews (50개만)
        users = db.query(User).all()
        movies = db.query(Movie).limit(50).all()
        
        for i in range(50):
            user = random.choice(users)
            movie = random.choice(movies)
            
            if db.query(Review).filter(Review.user_id == user.id, Review.movie_id == movie.id).first():
                continue
            
            review = Review(
                user_id=user.id,
                movie_id=movie.id,
                rating=Decimal(random.choice([3.0, 3.5, 4.0, 4.5, 5.0])),
                content=f"좋은 영화였습니다. {i+1}",
                created_at=datetime.now() - timedelta(days=random.randint(0, 180))
            )
            db.add(review)
            db.commit()
        
        print(f"✓ Reviews: {db.query(Review).count()}")
        
        # 3. Taste Analysis
        for user in users:
            if not db.query(TasteAnalysis).filter(TasteAnalysis.user_id == user.id).first():
                taste = TasteAnalysis(
                    user_id=user.id,
                    summary_text=f"{user.name}님은 다양한 장르를 즐기시는 것 같습니다."
                )
                db.add(taste)
        db.commit()
        print(f"✓ Taste Analysis: {db.query(TasteAnalysis).count()}")
        
        print("\n✓ Seeding completed!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
