from sqlalchemy import Column, Date, DateTime, Integer, String, Text, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    overview = Column(Text, nullable=True)
    release_date = Column(Date, nullable=True)
    runtime = Column(Integer, nullable=True)
    poster_url = Column(String, nullable=True)
    category = Column(String, nullable=True)
    release_year = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class MovieGenre(Base):
    __tablename__ = "movie_genres"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, nullable=False, index=True)
    genre = Column(String, nullable=False)


class MovieKeyword(Base):
    __tablename__ = "movie_keywords"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, nullable=False, index=True)
    keyword = Column(String, nullable=False)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    rating = Column(Numeric, nullable=False)
    comment = Column(Text, nullable=True)
    likes_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ReviewLike(Base):
    __tablename__ = "review_likes"

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ReviewComment(Base):
    __tablename__ = "review_comments"

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class WatchLog(Base):
    __tablename__ = "watch_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    movie_id = Column(Integer, nullable=False, index=True)
    rating = Column(Numeric, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class TasteProfile(Base):
    __tablename__ = "taste_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, unique=True, index=True)
    emotion_scores = Column(JSONB, nullable=False, default=dict)
    narrative_traits = Column(JSONB, nullable=False, default=dict)
    ending_preference = Column(JSONB, nullable=False, default=dict)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class MovieVector(Base):
    __tablename__ = "movie_vectors"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, nullable=False, unique=True, index=True)
    emotion_scores = Column(JSONB, nullable=False, default=dict)
    narrative_traits = Column(JSONB, nullable=False, default=dict)
    ending_preference = Column(JSONB, nullable=False, default=dict)
    embedding = Column(JSONB, nullable=False, default=list)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
