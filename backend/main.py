"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import movies, reviews, users

# Create FastAPI app
app = FastAPI(
    title="Movie Recommendation API",
    description="정서·서사 기반 영화 취향 시뮬레이션 & 감성 검색 서비스",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies.router)
app.include_router(reviews.router)
app.include_router(users.router)


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Movie Recommendation API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """Health check for load balancer"""
    return {"status": "healthy"}


# Lambda handler (for AWS Lambda deployment)
def handler(event, context):
    """
    Lambda entrypoint
    """
    from mangum import Mangum
    handler = Mangum(app)
    return handler(event, context)
