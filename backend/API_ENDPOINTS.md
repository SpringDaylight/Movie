# API Endpoints Documentation

## Base URL
```
http://localhost:8000
```

## API 요구사항 체크리스트

| ID | 요구사항 | 엔드포인트 | 상태 |
|----|---------|-----------|------|
| MW-API-001 | 영화 목록 API | GET /api/movies | ✅ 완료 |
| MW-API-002 | 영화 상세 API | GET /api/movies/{movieId} | ✅ 완료 |
| MW-API-003 | 영화별 리뷰 리스트 API | GET /api/movies/{movieId}/reviews | ✅ 완료 |
| MW-API-004 | 리뷰 작성 API | POST /api/movies/{movieId}/reviews | ✅ 완료 |
| MW-API-005 | 리뷰 수정 API | PUT /api/reviews/{reviewId} | ✅ 완료 |
| MW-API-006 | 리뷰 상세 API | GET /api/reviews/{reviewId} | ✅ 완료 |
| MW-API-007 | 좋아요 토글 API | POST /api/reviews/{reviewId}/likes | ✅ 완료 |
| MW-API-008 | 댓글 API | GET/POST /api/reviews/{reviewId}/comments | ✅ 완료 |
| MW-API-009 | 내 정보 API | GET /api/users/me | ✅ 완료 |
| MW-API-010 | 내 리뷰 목록 API | GET /api/users/me/reviews | ✅ 완료 |
| MW-API-011 | 취향 분석 API | GET /api/users/me/taste-analysis | ✅ 완료 |
| MW-DATA-001 | 더미 데이터 시드 | - | ✅ 완료 (1000 movies, 10 users, 219 reviews) |
| MW-DATA-002 | 필터 로직 매핑 | - | ✅ 완료 (genres, category, sort) |

---

## Movies API

### 1. 영화 목록 조회 (MW-API-001)
```http
GET /api/movies?query=&genres=&category=&sort=&page=1&page_size=20
```

**Query Parameters:**
- `query` (optional): 제목/시놉시스 검색어
- `genres` (optional): 장르 필터 (쉼표로 구분, 예: "액션,드라마")
- `category` (optional): 카테고리 필터
- `sort` (optional): 정렬 방식
  - `latest` (기본값): 최신순
  - `popular`: 인기순 (리뷰 수)
  - `rating`: 평점순
- `page` (optional): 페이지 번호 (기본값: 1)
- `page_size` (optional): 페이지 크기 (기본값: 20, 최대: 100)

**Response:**
```json
{
  "movies": [
    {
      "id": 1168190,
      "title": "더 레킹 크루",
      "release": "2026-01-28",
      "runtime": 124,
      "synopsis": "...",
      "poster_url": "https://...",
      "created_at": "2026-02-09T...",
      "genres": ["액션", "코미디", "범죄"],
      "tags": ["reunion", "amused"]
    }
  ],
  "total": 1000,
  "page": 1,
  "page_size": 20
}
```

**Example:**
```bash
# 액션 영화 검색
curl "http://localhost:8000/api/movies?genres=액션&sort=popular"

# 제목 검색
curl "http://localhost:8000/api/movies?query=아바타"
```

---

### 2. 영화 상세 조회 (MW-API-002)
```http
GET /api/movies/{movieId}
```

**Response:**
```json
{
  "id": 1168190,
  "title": "더 레킹 크루",
  "release": "2026-01-28",
  "runtime": 124,
  "synopsis": "...",
  "poster_url": "https://...",
  "created_at": "2026-02-09T...",
  "genres": ["액션", "코미디", "범죄"],
  "tags": ["reunion", "amused"]
}
```

---

### 3. 영화별 리뷰 목록 (MW-API-003)
```http
GET /api/movies/{movieId}/reviews?page=1&page_size=20
```

**Response:**
```json
{
  "reviews": [
    {
      "id": 1,
      "user_id": "user001",
      "movie_id": 1168190,
      "rating": 4.5,
      "content": "정말 재미있었습니다!",
      "created_at": "2026-02-09T...",
      "likes_count": 5,
      "comments_count": 2
    }
  ],
  "total": 10
}
```

---

### 4. 리뷰 작성 (MW-API-004)
```http
POST /api/movies/{movieId}/reviews?user_id=user001
```

**Request Body:**
```json
{
  "rating": 4.5,
  "content": "정말 재미있었습니다!"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": "user001",
  "movie_id": 1168190,
  "rating": 4.5,
  "content": "정말 재미있었습니다!",
  "created_at": "2026-02-09T...",
  "likes_count": 0,
  "comments_count": 0
}
```

---

## Reviews API

### 5. 리뷰 상세 조회 (MW-API-006)
```http
GET /api/reviews/{reviewId}
```

**Response:**
```json
{
  "id": 1,
  "user_id": "user001",
  "movie_id": 1168190,
  "rating": 4.5,
  "content": "정말 재미있었습니다!",
  "created_at": "2026-02-09T...",
  "likes_count": 5,
  "comments_count": 2
}
```

---

### 6. 리뷰 수정 (MW-API-005)
```http
PUT /api/reviews/{reviewId}
```

**Request Body:**
```json
{
  "rating": 5.0,
  "content": "다시 봐도 최고입니다!"
}
```

---

### 7. 좋아요 토글 (MW-API-007)
```http
POST /api/reviews/{reviewId}/likes?user_id=user001&is_like=true
```

**Query Parameters:**
- `user_id` (required): 사용자 ID
- `is_like` (optional): true=좋아요, false=싫어요 (기본값: true)

**Response:**
```json
{
  "message": "Review liked successfully"
}
```

---

### 8. 댓글 조회 (MW-API-008)
```http
GET /api/reviews/{reviewId}/comments?skip=0&limit=50
```

**Response:**
```json
[
  {
    "id": 1,
    "review_id": 1,
    "user_id": "user002",
    "content": "저도 같은 생각이에요!",
    "created_at": "2026-02-09T..."
  }
]
```

---

### 9. 댓글 작성 (MW-API-008)
```http
POST /api/reviews/{reviewId}/comments?user_id=user001
```

**Request Body:**
```json
{
  "content": "저도 같은 생각이에요!"
}
```

---

## Users API

### 10. 내 정보 조회 (MW-API-009)
```http
GET /api/users/me?user_id=user001
```

**Response:**
```json
{
  "id": "user001",
  "name": "김영화",
  "avatar_text": "따뜻한 드라마",
  "created_at": "2026-02-09T..."
}
```

---

### 11. 내 리뷰 목록 (MW-API-010)
```http
GET /api/users/me/reviews?user_id=user001&page=1&page_size=20
```

**Response:**
```json
{
  "reviews": [
    {
      "id": 1,
      "user_id": "user001",
      "movie_id": 1168190,
      "rating": 4.5,
      "content": "정말 재미있었습니다!",
      "created_at": "2026-02-09T...",
      "likes_count": 5,
      "comments_count": 2
    }
  ],
  "total": 15
}
```

---

### 12. 취향 분석 조회 (MW-API-011)
```http
GET /api/users/me/taste-analysis?user_id=user001
```

**Response:**
```json
{
  "user_id": "user001",
  "summary_text": "당신은 감성적이고 따뜻한 이야기를 선호하시는군요...",
  "updated_at": "2026-02-09T..."
}
```

---

## Swagger UI

모든 API는 Swagger UI에서 테스트할 수 있습니다:
```
http://localhost:8000/docs
```

---

## 데이터 현황

### 현재 데이터베이스 상태
- **영화**: 1,000개
- **사용자**: 10명
- **리뷰**: 219개
- **취향 분석**: 10개
- **장르**: 2,839개
- **태그**: 17,154개

### 테스트용 사용자 ID
- user001, user002, user003, ..., user010

---

## 에러 응답

### 404 Not Found
```json
{
  "detail": "Movie not found"
}
```

### 400 Bad Request
```json
{
  "detail": "User already reviewed this movie. Use PUT to update."
}
```

---

## 프론트엔드 통합 가이드

### 1. Base URL 설정
```typescript
const API_BASE_URL = "http://localhost:8000";
```

### 2. 영화 목록 가져오기
```typescript
const response = await fetch(
  `${API_BASE_URL}/api/movies?genres=액션&sort=popular&page=1`
);
const data = await response.json();
```

### 3. 리뷰 작성
```typescript
const response = await fetch(
  `${API_BASE_URL}/api/movies/${movieId}/reviews?user_id=${userId}`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rating: 4.5, content: "좋았어요!" })
  }
);
```

### 4. 좋아요 토글
```typescript
const response = await fetch(
  `${API_BASE_URL}/api/reviews/${reviewId}/likes?user_id=${userId}&is_like=true`,
  { method: "POST" }
);
```
