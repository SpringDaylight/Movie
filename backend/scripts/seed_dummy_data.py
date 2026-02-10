"""
Seed dummy data for users, reviews, and taste analysis
"""
import sys
import random
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.append(str(Path(__file__).resolve().parents[1]))

from db import get_db
from models import User, Review, TasteAnalysis, Comment, ReviewLike


# Sample data
SAMPLE_USERS = [
    {"id": "user001", "name": "김영화", "avatar_text": "따뜻한 드라마"},
    {"id": "user002", "name": "이시네", "avatar_text": "긴장감 넘치는 스릴러"},
    {"id": "user003", "name": "박무비", "avatar_text": "웃음 가득한 코미디"},
    {"id": "user004", "name": "최필름", "avatar_text": "감동적인 로맨스"},
    {"id": "user005", "name": "정액션", "avatar_text": "박진감 넘치는 액션"},
    {"id": "user006", "name": "강판타지", "avatar_text": "환상적인 모험"},
    {"id": "user007", "name": "윤공포", "avatar_text": "오싹한 호러"},
    {"id": "user008", "name": "임SF", "avatar_text": "미래지향적 SF"},
    {"id": "user009", "name": "한애니", "avatar_text": "따뜻한 애니메이션"},
    {"id": "user010", "name": "송범죄", "avatar_text": "치밀한 범죄 스릴러"},
]

REVIEW_TEMPLATES = [
    "정말 감동적인 영화였습니다. 오랜만에 여운이 남는 작품을 봤네요.",
    "기대 이상이었어요! 스토리 전개가 탄탄하고 배우들의 연기도 훌륭했습니다.",
    "시간 가는 줄 모르고 봤습니다. 강력 추천합니다!",
    "생각보다 평범했어요. 기대가 너무 컸나봅니다.",
    "영상미가 정말 뛰어났습니다. 극장에서 꼭 봐야 할 영화!",
    "스토리는 좋았지만 러닝타임이 조금 길게 느껴졌어요.",
    "배우들의 케미가 정말 좋았습니다. 속편이 기대되네요!",
    "예상치 못한 반전에 깜짝 놀랐습니다. 재미있게 봤어요.",
    "OST가 정말 인상적이었습니다. 영화와 완벽한 조화!",
    "가족과 함께 보기 좋은 영화입니다. 따뜻한 감동을 받았어요.",
    "액션 신이 정말 박진감 넘쳤습니다. 손에 땀을 쥐게 하네요!",
    "코미디 요소가 적절히 섞여있어서 지루하지 않았어요.",
    "메시지가 명확하고 감동적이었습니다. 생각할 거리를 많이 남겨주네요.",
    "비주얼이 압도적이었습니다. CG 기술이 정말 발전했네요.",
    "배우들의 연기력이 돋보였습니다. 특히 주연 배우가 인상적!",
]

TASTE_ANALYSIS_TEMPLATES = [
    "당신은 감성적이고 따뜻한 이야기를 선호하시는군요. 인간관계와 성장을 다룬 드라마에 높은 점수를 주셨습니다.",
    "긴장감과 스릴을 즐기시는 것 같습니다. 예측 불가능한 전개와 반전이 있는 작품을 좋아하시네요.",
    "유머와 재치가 넘치는 작품을 선호하십니다. 밝고 경쾌한 분위기의 영화에 높은 평가를 하셨어요.",
    "로맨틱하고 감성적인 스토리를 좋아하시는군요. 사랑과 관계에 대한 깊이 있는 탐구를 즐기십니다.",
    "박진감 넘치는 액션과 스펙터클을 선호하십니다. 시각적 쾌감과 역동성을 중요하게 생각하시네요.",
    "상상력이 풍부한 판타지 세계관을 즐기십니다. 현실을 벗어난 모험과 마법에 매료되시는군요.",
    "공포와 긴장감을 즐기시는 것 같습니다. 심리적 공포와 서스펜스를 선호하시네요.",
    "미래지향적이고 철학적인 SF 작품을 좋아하십니다. 기술과 인간성에 대한 질문을 즐기시네요.",
    "따뜻하고 감동적인 애니메이션을 선호하십니다. 순수하고 아름다운 이야기에 높은 점수를 주셨어요.",
    "치밀하고 복잡한 범죄 스릴러를 즐기십니다. 논리적 추리와 긴장감을 중요하게 생각하시네요.",
]

COMMENT_TEMPLATES = [
    "저도 같은 생각이에요!",
    "공감합니다. 정말 좋은 영화였죠.",
    "저는 조금 다르게 느꼈는데, 그래도 재미있게 봤어요.",
    "좋은 리뷰 감사합니다!",
    "이 부분 정말 인상적이었죠!",
    "저도 다시 보고 싶네요.",
    "추천해주셔서 감사합니다!",
    "동의합니다. 배우들 연기가 정말 좋았어요.",
]


def seed_users(db):
    """Create sample users"""
    print("\n[1] Creating users...")
    created = 0
    
    for user_data in SAMPLE_USERS:
        existing = db.query(User).filter(User.id == user_data["id"]).first()
        if not existing:
            user = User(**user_data)
            db.add(user)
            created += 1
    
    db.commit()
    print(f"✓ Created {created} users (skipped {len(SAMPLE_USERS) - created} existing)")


def seed_reviews(db, num_reviews=200):
    """Create sample reviews"""
    print(f"\n[2] Creating {num_reviews} reviews...")
    
    # Get all users and movies
    users = db.query(User).all()
    from models import Movie
    movies = db.query(Movie).limit(100).all()  # Use first 100 movies
    
    if not users or not movies:
        print("✗ No users or movies found. Please seed users and movies first.")
        return
    
    created = 0
    skipped = 0
    for _ in range(num_reviews):
        user = random.choice(users)
        movie = random.choice(movies)
        
        # Check if review already exists
        existing = db.query(Review).filter(
            Review.user_id == user.id,
            Review.movie_id == movie.id
        ).first()
        
        if existing:
            skipped += 1
            continue
        
        # Create review
        rating = Decimal(random.choice([3.0, 3.5, 4.0, 4.5, 5.0]))
        content = random.choice(REVIEW_TEMPLATES)
        
        # Random date within last 6 months
        days_ago = random.randint(0, 180)
        created_at = datetime.now() - timedelta(days=days_ago)
        
        review = Review(
            user_id=user.id,
            movie_id=movie.id,
            rating=rating,
            content=content,
            created_at=created_at
        )
        db.add(review)
        
        # Commit individually to avoid batch conflicts
        try:
            db.commit()
            created += 1
        except Exception as e:
            db.rollback()
            skipped += 1
    
    print(f"✓ Created {created} reviews (skipped {skipped} duplicates)")


def seed_comments(db, num_comments=100):
    """Create sample comments"""
    print(f"\n[3] Creating {num_comments} comments...")
    
    users = db.query(User).all()
    reviews = db.query(Review).limit(50).all()  # Comment on first 50 reviews
    
    if not users or not reviews:
        print("✗ No users or reviews found.")
        return
    
    created = 0
    for _ in range(num_comments):
        user = random.choice(users)
        review = random.choice(reviews)
        content = random.choice(COMMENT_TEMPLATES)
        
        # Random date after review creation
        days_after = random.randint(0, 30)
        created_at = review.created_at + timedelta(days=days_after)
        
        comment = Comment(
            review_id=review.id,
            user_id=user.id,
            content=content,
            created_at=created_at
        )
        db.add(comment)
        created += 1
    
    db.commit()
    print(f"✓ Created {created} comments")


def seed_likes(db, num_likes=150):
    """Create sample review likes"""
    print(f"\n[4] Creating {num_likes} likes...")
    
    users = db.query(User).all()
    reviews = db.query(Review).limit(50).all()
    
    if not users or not reviews:
        print("✗ No users or reviews found.")
        return
    
    created = 0
    for _ in range(num_likes):
        user = random.choice(users)
        review = random.choice(reviews)
        
        # Check if like already exists
        existing = db.query(ReviewLike).filter(
            ReviewLike.review_id == review.id,
            ReviewLike.user_id == user.id
        ).first()
        
        if existing:
            continue
        
        is_like = random.choice([True, True, True, False])  # 75% likes, 25% dislikes
        
        like = ReviewLike(
            review_id=review.id,
            user_id=user.id,
            is_like=is_like
        )
        db.add(like)
        created += 1
    
    db.commit()
    print(f"✓ Created {created} likes")


def seed_taste_analysis(db):
    """Create taste analysis for users"""
    print("\n[5] Creating taste analysis...")
    
    users = db.query(User).all()
    created = 0
    
    for i, user in enumerate(users):
        existing = db.query(TasteAnalysis).filter(
            TasteAnalysis.user_id == user.id
        ).first()
        
        if existing:
            continue
        
        summary_text = TASTE_ANALYSIS_TEMPLATES[i % len(TASTE_ANALYSIS_TEMPLATES)]
        
        taste = TasteAnalysis(
            user_id=user.id,
            summary_text=summary_text
        )
        db.add(taste)
        created += 1
    
    db.commit()
    print(f"✓ Created {created} taste analyses")


def main():
    """Main seeding function"""
    print("=" * 60)
    print("Seeding Dummy Data")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        seed_users(db)
        seed_reviews(db, num_reviews=200)
        seed_comments(db, num_comments=100)
        seed_likes(db, num_likes=150)
        seed_taste_analysis(db)
        
        print("\n" + "=" * 60)
        print("✓ Seeding completed successfully!")
        print("=" * 60)
        
        # Print summary
        print("\nData Summary:")
        print(f"  Users: {db.query(User).count()}")
        print(f"  Reviews: {db.query(Review).count()}")
        print(f"  Comments: {db.query(Comment).count()}")
        print(f"  Likes: {db.query(ReviewLike).count()}")
        print(f"  Taste Analyses: {db.query(TasteAnalysis).count()}")
        
    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
