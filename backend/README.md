# Movie Recommendation Backend

정서·서사 기반 영화 취향 시뮬레이션 & 감성 검색 서비스 백엔드

## 🚀 빠른 시작

### 1. 패키지 설치

```bash
cd backend
pip install -r requirements.txt
```

### 2. AWS 자격증명 설정

```bash
aws configure
```

또는 `.env` 파일 생성:

```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=ap-northeast-2
```

### 3. SSL 인증서 다운로드

```bash
python scripts/download_rds_cert.py
```

### 4. DB 연결 테스트

```bash
python tests/db_connection_check.py
```

### 5. 마이그레이션 실행

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "Initial schema"

# 마이그레이션 적용
alembic upgrade head
```

### 6. 서버 실행

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API 문서: http://localhost:8000/docs

## 📁 프로젝트 구조

```
backend/
├── api/                    # API 라우터
│   ├── movies.py          # 영화 API
│   ├── reviews.py         # 리뷰 API
│   └── users.py           # 사용자 API
├── repositories/          # 데이터 접근 계층
│   ├── base.py           # 기본 CRUD
│   ├── movie.py          # 영화 레포지토리
│   ├── review.py         # 리뷰 레포지토리
│   └── user.py           # 사용자 레포지토리
├── domain/               # ML 도메인 로직
│   ├── a1_preference.py  # 취향 분석
│   ├── a2_movie_vector.py # 영화 벡터
│   ├── a3_prediction.py  # 만족 확률
│   ├── a4_explanation.py # 설명 생성
│   ├── a5_emotional_search.py # 감성 검색
│   ├── a6_group_simulation.py # 그룹 시뮬레이션
│   └── a7_taste_map.py   # 취향 지도
├── services/             # 외부 서비스
│   ├── llm_client.py    # LLM 클라이언트
│   ├── embedding_client.py # 임베딩
│   ├── vector_store.py  # 벡터 저장소
│   ├── cache.py         # 캐시
│   ├── storage.py       # S3 저장소
│   └── scheduler.py     # 스케줄러
├── utils/               # 유틸리티
│   ├── helpers.py
│   ├── logger.py
│   ├── errors.py
│   ├── response.py
│   └── validator.py
├── tests/               # 테스트
│   ├── db_connection_check.py
├── scripts/             # 스크립트
│   ├── download_rds_cert.py
│   ├── migrate.py
│   └── seed_data.py
├── alembic/             # 마이그레이션
│   ├── versions/
│   └── env.py
├── models.py            # SQLAlchemy 모델
├── schemas.py           # Pydantic 스키마
├── db.py                # 데이터베이스 설정
├── config.py            # 설정
├── main.py              # FastAPI 앱
└── requirements.txt     # 의존성
```

## 🗄️ 데이터베이스 스키마

### 핵심 테이블

- **users** - 사용자
- **movies** - 영화 메타데이터
- **movie_genres** - 영화 장르
- **movie_tags** - 영화 태그 (정서/서사/여운)
- **reviews** - 리뷰
- **comments** - 댓글
- **review_likes** - 좋아요
- **taste_analysis** - 취향 분석
- **group_decisions** - 그룹 결정
- **group_members** - 그룹 멤버

### ML 테이블

- **user_preferences** - 사용자 취향 벡터
- **movie_vectors** - 영화 특성 벡터

## 🔌 API 엔드포인트

### 영화 (Movies)

- `GET /api/movies` - 영화 목록 (검색/필터)
- `GET /api/movies/{id}` - 영화 상세
- `POST /api/movies` - 영화 생성
- `PUT /api/movies/{id}` - 영화 수정
- `DELETE /api/movies/{id}` - 영화 삭제
- `GET /api/movies/genre/{genre}` - 장르별 영화
- `GET /api/movies/popular/list` - 인기 영화

### 리뷰 (Reviews)

- `GET /api/reviews/{id}` - 리뷰 상세
- `POST /api/reviews` - 리뷰 작성
- `PUT /api/reviews/{id}` - 리뷰 수정
- `DELETE /api/reviews/{id}` - 리뷰 삭제
- `POST /api/reviews/{id}/likes` - 좋아요 토글
- `GET /api/reviews/{id}/comments` - 댓글 목록
- `POST /api/reviews/{id}/comments` - 댓글 작성

### 사용자 (Users)

- `GET /api/users/me` - 내 정보
- `POST /api/users` - 사용자 생성
- `PUT /api/users/me` - 내 정보 수정
- `GET /api/users/me/reviews` - 내 리뷰 목록
- `GET /api/users/me/taste-analysis` - 취향 분석
- `GET /api/users/{id}` - 사용자 정보

## 🧪 테스트

```bash
# DB 연결 테스트
python tests/db_connection_check.py

# 로컬 스모크 테스트
```

## 📚 문서

- [RDS 설정 가이드](RDS_SETUP.md)
- [빠른 시작 가이드](QUICK_START.md)
- [마이그레이션 가이드](MIGRATION_GUIDE.md)

## 🛠️ 개발 도구

### 마이그레이션

```bash
# 생성
python scripts/migrate.py create -m "Add new table"

# 적용
python scripts/migrate.py apply

# 현재 버전
python scripts/migrate.py current
```

### 더미 데이터

```bash
python scripts/seed_data.py
```

## 🚢 배포

### Docker

```bash
docker build -t movie-backend .
docker run -p 8000:8000 movie-backend
```


## 🔧 환경 변수

```bash
# AWS
AWS_REGION=ap-northeast-2
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

# RDS
RDS_HOST=movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com
RDS_PORT=5432
RDS_DATABASE=movie
RDS_USER=postgres
RDS_SECRET_ARN=arn:aws:secretsmanager:...

# SSL
SSL_CERT_PATH=/certs/global-bundle.pem

# 로컬 개발 (Secrets Manager 우회)
DATABASE_URL=postgresql://postgres:password@localhost:5432/movie

# 기타
ENV=development
SQL_ECHO=false
```

## 📝 라이선스

MIT

## 👥 팀

납득이 - 정서·서사 기반 영화 추천 시스템
