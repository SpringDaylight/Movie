# 데이터베이스 마이그레이션 가이드

## 준비사항

1. AWS 자격증명 설정 완료
2. RDS 연결 테스트 성공
3. 패키지 설치 완료

```bash
pip install -r requirements.txt
```

## 마이그레이션 생성

### 방법 1: Python 스크립트 사용 (권장)

```bash
# 새 마이그레이션 생성
python backend/scripts/migrate.py create -m "Create initial tables"

# 마이그레이션 적용
python backend/scripts/migrate.py apply

# 현재 버전 확인
python backend/scripts/migrate.py current

# 마이그레이션 히스토리 확인
python backend/scripts/migrate.py history
```

### 방법 2: Alembic 직접 사용

```bash
cd backend

# 새 마이그레이션 생성
alembic revision --autogenerate -m "Create initial tables"

# 마이그레이션 적용
alembic upgrade head

# 현재 버전 확인
alembic current

# 마이그레이션 히스토리
alembic history

# 롤백 (1단계)
alembic downgrade -1

# 특정 버전으로 롤백
alembic downgrade <revision_id>
```

## 초기 마이그레이션 실행

```bash
# 1. 마이그레이션 생성
cd backend
alembic revision --autogenerate -m "Initial schema with all tables"

# 2. 생성된 마이그레이션 파일 확인
# backend/alembic/versions/<timestamp>_initial_schema_with_all_tables.py

# 3. 마이그레이션 적용
alembic upgrade head

# 4. 확인
python tests/db_connection_check.py
```

## 생성되는 테이블 목록

### 핵심 도메인 테이블
1. **users** - 사용자
2. **movies** - 영화 메타데이터
3. **movie_genres** - 영화 장르 (다대다)
4. **movie_tags** - 영화 정성 태그
5. **reviews** - 리뷰
6. **comments** - 리뷰 댓글
7. **review_likes** - 리뷰 좋아요
8. **taste_analysis** - 취향 분석 결과
9. **group_decisions** - 그룹 결정
10. **group_members** - 그룹 멤버

### ML/벡터 데이터 테이블
11. **user_preferences** - 사용자 취향 벡터
12. **movie_vectors** - 영화 특성 벡터

## 마이그레이션 파일 구조

```
backend/alembic/
├── versions/
│   ├── 20260206_000001_init.py  (기존)
│   └── <timestamp>_initial_schema_with_all_tables.py  (새로 생성)
├── env.py
└── script.py.mako
```

## 트러블슈팅

### 1. "Target database is not up to date" 오류

```bash
# 현재 버전 확인
alembic current

# 강제로 최신 버전으로 표시 (주의!)
alembic stamp head
```

### 2. "Can't locate revision identified by" 오류

```bash
# 마이그레이션 히스토리 확인
alembic history

# 특정 버전으로 이동
alembic upgrade <revision_id>
```

### 3. 마이그레이션 충돌

```bash
# 마이그레이션 파일 삭제 후 재생성
rm backend/alembic/versions/<problematic_file>.py
alembic revision --autogenerate -m "Recreate schema"
```

### 4. 데이터베이스 초기화 (주의: 모든 데이터 삭제!)

```bash
# 모든 테이블 삭제
alembic downgrade base

# 다시 적용
alembic upgrade head
```

## 마이그레이션 베스트 프랙티스

1. **항상 백업**: 프로덕션 마이그레이션 전 백업
2. **테스트 환경 먼저**: 개발 → 스테이징 → 프로덕션 순서
3. **리뷰**: 생성된 마이그레이션 파일 검토
4. **롤백 계획**: 문제 발생 시 롤백 방법 준비
5. **데이터 마이그레이션**: 스키마 변경 시 데이터 마이그레이션 스크립트 작성

## 다음 단계

마이그레이션 완료 후:

1. **더미 데이터 생성**
   ```bash
   python backend/scripts/seed_data.py
   ```

2. **API 서버 실행**
   ```bash
   uvicorn backend.main:app --reload
   ```

3. **API 문서 확인**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
