# AWS RDS PostgreSQL 연결 설정 가이드

## 개요

이 프로젝트는 AWS RDS PostgreSQL 데이터베이스에 연결하며, AWS Secrets Manager를 통해 비밀번호를 안전하게 관리합니다.

## 연결 정보

- **Host**: `movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com`
- **Port**: `5432`
- **Database**: `movie`
- **User**: `postgres`
- **Secret ARN**: `arn:aws:secretsmanager:ap-northeast-2:416963226971:secret:rds!db-f3aa3685-4bca-4982-bae8-c628e185fdf2-078IVh`

## 설치 단계

### 1. 필수 패키지 설치

```bash
cd backend
pip install -r requirements.txt
```

### 2. SSL 인증서 다운로드

RDS 연결을 위한 SSL 인증서를 다운로드합니다:

```bash
# 방법 1: Python 스크립트 사용
python scripts/download_rds_cert.py

# 방법 2: 수동 다운로드
mkdir -p /certs
curl -o /certs/global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

### 3. AWS 자격증명 설정

AWS CLI가 설정되어 있어야 합니다:

```bash
# AWS CLI 설치 확인
aws --version

# AWS 자격증명 설정 (아직 안 했다면)
aws configure
```

필요한 정보:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `ap-northeast-2`

### 4. 환경 변수 설정 (선택사항)

`.env` 파일을 생성하여 설정을 오버라이드할 수 있습니다:

```bash
# backend/.env
ENV=development

# RDS 설정 (기본값 사용 시 생략 가능)
RDS_HOST=movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com
RDS_PORT=5432
RDS_DATABASE=movie
RDS_USER=postgres
RDS_SECRET_ARN=arn:aws:secretsmanager:ap-northeast-2:416963226971:secret:rds!db-f3aa3685-4bca-4982-bae8-c628e185fdf2-078IVh

# AWS 설정
AWS_REGION=ap-northeast-2

# SSL 인증서 경로
SSL_CERT_PATH=/certs/global-bundle.pem

# 로컬 개발용 직접 DATABASE_URL 설정 (Secrets Manager 우회)
# DATABASE_URL=postgresql://postgres:password@localhost:5432/movie
```

## 연결 테스트

### 기본 연결 테스트

```bash
cd backend
python tests/db_connection_check.py
```

예상 출력:
```
============================================================
Testing AWS RDS PostgreSQL Connection
============================================================

[1] Getting database URL...
✓ Database URL: postgresql://***@movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com:5432/movie

[2] Creating SQLAlchemy engine...
✓ Engine created: Engine(postgresql://postgres:***@movie-dev-db...)

[3] Testing database connection...
✓ Connected successfully!
  PostgreSQL version: PostgreSQL 16.4 on x86_64-pc-linux-gnu...

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

### 직접 psycopg2로 테스트

```python
import psycopg2
import boto3
import json
import subprocess

# Secrets Manager에서 비밀번호 가져오기
secret_arn = 'arn:aws:secretsmanager:ap-northeast-2:416963226971:secret:rds!db-f3aa3685-4bca-4982-bae8-c628e185fdf2-078IVh'
result = subprocess.check_output([
    'bash', '-lc',
    f"aws secretsmanager get-secret-value --secret-id '{secret_arn}' --query SecretString --output text"
]).decode()
password = json.loads(result)['password']

# 연결
conn = psycopg2.connect(
    host='movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com',
    port=5432,
    database='movie',
    user='postgres',
    password=password,
    sslmode='verify-full',
    sslrootcert='/certs/global-bundle.pem'
)

cur = conn.cursor()
cur.execute('SELECT version();')
print(cur.fetchone()[0])
cur.close()
conn.close()
```

## 데이터베이스 마이그레이션

### Alembic 초기화 (이미 완료됨)

```bash
cd backend
alembic init alembic
```

### 마이그레이션 생성

```bash
# 새 마이그레이션 생성
alembic revision --autogenerate -m "Create initial tables"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

## 트러블슈팅

### 1. SSL 인증서 오류

```
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**해결책**: SSL 인증서를 다시 다운로드하거나 경로를 확인하세요.

```bash
python scripts/download_rds_cert.py
```

### 2. Secrets Manager 접근 오류

```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

**해결책**: AWS 자격증명을 설정하세요.

```bash
aws configure
```

### 3. 연결 타임아웃

```
psycopg2.OperationalError: timeout expired
```

**해결책**: 
- VPC 보안 그룹에서 5432 포트가 열려있는지 확인
- RDS 인스턴스가 Public Access 설정되어 있는지 확인
- 네트워크 연결 확인

### 4. 로컬 개발 시 Secrets Manager 우회

로컬에서 개발할 때 Secrets Manager 없이 직접 연결하려면:

```bash
# .env 파일에 추가
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/movie
```

## 코드 구조

### config.py
- `get_rds_password()`: Secrets Manager에서 비밀번호 가져오기
- `get_database_url()`: 데이터베이스 URL 생성

### db.py
- `get_engine()`: SQLAlchemy 엔진 생성
- `get_db()`: FastAPI 의존성 주입용 세션 생성

### 사용 예시

```python
from backend.db import get_db
from sqlalchemy import text

# FastAPI 라우터에서
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT version()"))
    return {"version": result.scalar()}
```

## 보안 주의사항

1. **절대 비밀번호를 코드에 하드코딩하지 마세요**
2. **`.env` 파일을 Git에 커밋하지 마세요** (`.gitignore`에 추가됨)
3. **AWS 자격증명을 공유하지 마세요**
4. **프로덕션에서는 IAM 역할을 사용하세요**

## 참고 자료

- [AWS RDS PostgreSQL 문서](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
- [AWS Secrets Manager 문서](https://docs.aws.amazon.com/secretsmanager/)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [Alembic 문서](https://alembic.sqlalchemy.org/)
