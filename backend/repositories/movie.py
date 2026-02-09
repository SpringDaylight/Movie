"""
Movie repository with custom queries
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_

from models import Movie, MovieGenre, MovieTag, Review
from repositories.base import BaseRepository


class MovieRepository(BaseRepository[Movie]):
    """Movie repository with custom queries"""
    
    def __init__(self, db: Session):
        super().__init__(Movie, db)
    
    def get_with_details(self, movie_id: int) -> Optional[Movie]:
        """Get movie with genres and tags"""
        return (
            self.db.query(Movie)
            .options(joinedload(Movie.genres), joinedload(Movie.tags))
            .filter(Movie.id == movie_id)
            .first()
        )
    
    def search(
        self,
        query: Optional[str] = None,
        genres: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Movie]:
        """Search movies by title and genres"""
        db_query = self.db.query(Movie).options(
            joinedload(Movie.genres),
            joinedload(Movie.tags)
        )
        
        # Text search
        if query:
            db_query = db_query.filter(
                or_(
                    Movie.title.ilike(f"%{query}%"),
                    Movie.synopsis.ilike(f"%{query}%")
                )
            )
        
        # Genre filter
        if genres:
            db_query = db_query.join(MovieGenre).filter(
                MovieGenre.genre.in_(genres)
            )
        
        return db_query.offset(skip).limit(limit).all()
    
    def get_by_genre(self, genre: str, limit: int = 20) -> List[Movie]:
        """Get movies by genre"""
        return (
            self.db.query(Movie)
            .join(MovieGenre)
            .filter(MovieGenre.genre == genre)
            .options(joinedload(Movie.genres), joinedload(Movie.tags))
            .limit(limit)
            .all()
        )
    
    def get_popular(self, limit: int = 20) -> List[Movie]:
        """Get popular movies (by review count)"""
        from sqlalchemy import func
        
        return (
            self.db.query(Movie)
            .outerjoin(Review)
            .group_by(Movie.id)
            .order_by(func.count(Review.id).desc())
            .options(joinedload(Movie.genres), joinedload(Movie.tags))
            .limit(limit)
            .all()
        )
    
    def add_genre(self, movie_id: int, genre: str) -> bool:
        """Add genre to movie"""
        movie_genre = MovieGenre(movie_id=movie_id, genre=genre)
        self.db.add(movie_genre)
        self.db.commit()
        return True
    
    def add_tag(self, movie_id: int, tag: str) -> bool:
        """Add tag to movie"""
        movie_tag = MovieTag(movie_id=movie_id, tag=tag)
        self.db.add(movie_tag)
        self.db.commit()
        return True
