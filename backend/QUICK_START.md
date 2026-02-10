# 빠른 시작 가이드

## AWS 자격증명 설정

DB에 연결하려면 AWS 자격증명이 필요합니다. 다음 중 하나의 방법을 선택하세요:

### 방법 1: AWS CLI 설정 (권장)

```bash
# AWS CLI 설치 확인
aws --version

# AWS 자격증명 설정
aws configure
```

입력 정보:
- AWS Access Key ID: [팀에서 제공]
- AWS Secret Access Key: [팀에서 제공]
- Default region name: `ap-northeast-2`
- Default output format: `json`

### 방법 2: 환경 변수 설정

`.env` 파일을 `backend/` 디렉토리에 생성:

```bash
# backend/.env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=ap-northeast-2
```

### 방법 3: 로컬 개발용 직접 연결 (Secrets Manager 우회)

`.env` 파일에 DATABASE_URL을 직접 설정:

```bash
# backend/.env
DATABASE_URL=postgresql://postgres:your_password@movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com:5432/movie
```

## 연결 테스트

```bash
# 1. 패키지 설치
pip install -r backend/requirements.txt

# 2. SSL 인증서 다운로드
python backend/scripts/download_rds_cert.py

# 3. DB 연결 테스트
python backend/tests/db_connection_check.py
```

## 성공 시 출력 예시

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
  No tables found (database is empty)

============================================================
✓ All tests passed!
============================================================
```

## 다음 단계

연결이 성공하면:

1. **데이터베이스 스키마 생성**
   ```bash
   alembic upgrade head
   ```

2. **더미 데이터 생성**
   ```bash
   python backend/scripts/seed_data.py
   ```

3. **서버 실행**
   ```bash
   uvicorn backend.main:app --reload
   ```

## 트러블슈팅

### "Unable to locate credentials" 오류

AWS 자격증명이 설정되지 않았습니다. 위의 방법 1, 2, 또는 3을 사용하세요.

### "Connection timeout" 오류

- VPC 보안 그룹에서 5432 포트가 열려있는지 확인
- 네트워크 연결 확인

### "SSL certificate verify failed" 오류

SSL 인증서를 다시 다운로드하세요:
```bash
python backend/scripts/download_rds_cert.py
```
