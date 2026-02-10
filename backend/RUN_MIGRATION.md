# 🚀 마이그레이션 실행 - 간단 가이드

## 1️⃣ 비밀번호 설정 (필수!)

`backend/.env` 파일을 열고 DATABASE_URL의 YOUR_PASSWORD를 실제 비밀번호로 변경하세요:

```bash
# backend/.env 파일에서 아래 줄의 주석(#)을 제거하고 비밀번호 입력
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com:5432/movie
```

## 2️⃣ 마이그레이션 실행

### Windows (PowerShell/CMD)

```powershell
# 1. backend 디렉토리로 이동
cd backend

# 2. DB 연결 테스트
python tests/db_connection_check.py

# 3. 현재 마이그레이션 상태 확인
alembic current

# 4. 마이그레이션 적용
alembic upgrade head

# 5. 확인
python tests/db_connection_check.py
```

### 예상 출력

#### Step 2: DB 연결 테스트
```
============================================================
Testing AWS RDS PostgreSQL Connection
============================================================

[1] Getting database URL...
✓ Database URL: postgresql://***@movie-dev-db...

[3] Testing database connection...
✓ Connected successfully!
  PostgreSQL version: PostgreSQL 16.4...

[5] Checking existing tables...
✓ Found 10 tables:
  - users
  - movies
  - movie_genres
  ...

============================================================
✓ All tests passed!
============================================================
```

#### Step 3: 현재 상태
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
20260206_000001 (head)
```

#### Step 4: 마이그레이션 적용
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 20260206_000001 -> 20260209_000002, Update schema with new ERD structure
```

#### Step 5: 최종 확인
```
[5] Checking existing tables...
✓ Found 12 tables:
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

============================================================
✓ All tests passed!
============================================================
```

## 3️⃣ 서버 실행

```powershell
# backend 디렉토리에서
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

브라우저에서 확인:
- API 문서: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## ⚠️ 문제 해결

### "Unable to locate credentials" 오류

`.env` 파일에서 DATABASE_URL의 주석(#)을 제거했는지 확인하세요.

### "Connection refused" 오류

1. VPN 연결 확인
2. 비밀번호가 정확한지 확인
3. 네트워크 연결 확인

### "relation already exists" 오류

테이블이 이미 존재하는 경우:

```powershell
# 현재 상태를 최신으로 표시
alembic stamp head
```

### 마이그레이션 롤백

```powershell
# 1단계 롤백
alembic downgrade -1

# 처음으로 롤백
alembic downgrade base
```

## ✅ 성공 체크리스트

- [ ] `.env` 파일에 DATABASE_URL 설정 완료
- [ ] DB 연결 테스트 성공
- [ ] 마이그레이션 적용 완료
- [ ] 12개 테이블 생성 확인
- [ ] 서버 실행 성공
- [ ] API 문서 접속 가능

## 🎉 다음 단계

1. **더미 데이터 생성** (다음 작업)
   ```powershell
   python scripts/seed_data.py
   ```

2. **API 테스트**
   - Swagger UI에서 직접 테스트
   - 또는 curl/Postman 사용

3. **ML 로직 통합**
   - model_sample의 A-1~A-8을 backend/domain/에 통합

---

**도움이 필요하면 EXECUTE_MIGRATION.md를 참고하세요!**
