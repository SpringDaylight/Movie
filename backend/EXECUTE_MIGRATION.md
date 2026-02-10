# 마이그레이션 실행 가이드

## ⚠️ 중요: 실행 전 준비사항

### 1. AWS 자격증명 설정

다음 중 **하나**를 선택하세요:

#### 옵션 A: AWS CLI 설치 및 설정 (권장)

```bash
# AWS CLI 설치 확인
aws --version

# 없다면 설치: https://aws.amazon.com/cli/

# AWS 자격증명 설정
aws configure
```

입력 정보:
- AWS Access Key ID: [팀에서 제공]
- AWS Secret Access Key: [팀에서 제공]
- Default region: `ap-northeast-2`
- Default output format: `json`

#### 옵션 B: 환경 변수로 설정

`backend/.env` 파일 생성:

```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=ap-northeast-2
```

#### 옵션 C: DATABASE_URL 직접 설정 (가장 간단)

팀에서 RDS 비밀번호를 받아서 `backend/.env` 파일에 추가:

```bash
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com:5432/movie
```

### 2. 패키지 설치 확인

```bash
cd backend
pip install -r requirements.txt
```

### 3. SSL 인증서 다운로드

```bash
python scripts/download_rds_cert.py
```

## 🚀 마이그레이션 실행

### Step 1: DB 연결 테스트

```bash
cd backend
python tests/db_connection_check.py
```

**예상 출력:**
```
============================================================
Testing AWS RDS PostgreSQL Connection
============================================================

[1] Getting database URL...
✓ Database URL: postgresql://***@movie-dev-db...

[2] Creating SQLAlchemy engine...
✓ Engine created: Engine(postgresql://postgres:***@...)

[3] Testing database connection...
✓ Connected successfully!
  PostgreSQL version: PostgreSQL 16.4...

[4] Testing session creation...
✓ Session created successfully!
  Database: movie
  User: postgres

[5] Checking existing tables...
✓ Found X tables:
  - users
  - movies
  - ...

============================================================
✓ All tests passed!
============================================================
```

### Step 2: 현재 마이그레이션 상태 확인

```bash
cd backend
alembic current
```

**예상 출력:**
```
20260206_000001 (head)
```

### Step 3: 새 마이그레이션 적용

```bash
cd backend
alembic upgrade head
```

**예상 출력:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 20260206_000001 -> 20260209_000002, Update schema with new ERD structure
```

### Step 4: 마이그레이션 확인

```bash
# 현재 버전 확인
alembic current

# 테이블 확인
python tests/db_connection_check.py
```

**예상 테이블 목록:**
- users
- movies
- movie_genres
- movie_tags
- reviews
- comments
- review_likes
- taste_analysis
- group_decisions
- group_members
- user_preferences
- movie_vectors

## ✅ 성공 확인

모든 단계가 성공하면:

1. ✅ DB 연결 성공
2. ✅ 마이그레이션 적용 완료
3. ✅ 12개 테이블 생성 확인

## 🔧 트러블슈팅

### 문제 1: "Unable to locate credentials"

**원인**: AWS 자격증명이 설정되지 않음

**해결책**: 위의 "옵션 C"를 사용하여 DATABASE_URL을 직접 설정

```bash
# backend/.env
DATABASE_URL=postgresql://postgres:PASSWORD@movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com:5432/movie
```

### 문제 2: "Connection timeout"

**원인**: 네트워크 또는 VPC 보안 그룹 문제

**해결책**:
1. VPN 연결 확인
2. 보안 그룹에서 5432 포트 허용 확인
3. 네트워크 연결 확인

### 문제 3: "Target database is not up to date"

**원인**: 마이그레이션 버전 불일치

**해결책**:
```bash
# 현재 버전 확인
alembic current

# 강제로 특정 버전으로 표시
alembic stamp 20260206_000001

# 다시 업그레이드
alembic upgrade head
```

### 문제 4: "relation already exists"

**원인**: 테이블이 이미 존재함

**해결책**:
```bash
# 마이그레이션 히스토리 확인
alembic history

# 현재 상태를 최신으로 표시 (테이블이 이미 있는 경우)
alembic stamp head
```

### 문제 5: 마이그레이션 롤백 필요

```bash
# 1단계 롤백
alembic downgrade -1

# 특정 버전으로 롤백
alembic downgrade 20260206_000001

# 모든 마이그레이션 롤백 (주의!)
alembic downgrade base
```

## 📝 다음 단계

마이그레이션 성공 후:

### 1. 더미 데이터 생성

```bash
python scripts/seed_data.py
```

### 2. API 서버 실행

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. API 문서 확인

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 4. API 테스트

```bash
# Health check
curl http://localhost:8000/health

# 영화 목록
curl http://localhost:8000/api/movies

# 사용자 생성
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"id": "user001", "name": "테스트 사용자"}'
```

## 🎉 완료!

마이그레이션이 성공적으로 완료되었습니다!

이제 다음 작업을 진행할 수 있습니다:
- 더미 데이터 생성
- API 서버 실행 및 테스트
- ML 로직 통합 (model_sample → backend/domain)
