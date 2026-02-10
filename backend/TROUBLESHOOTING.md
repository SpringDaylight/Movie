# 🔧 데이터베이스 연결 문제 해결 가이드

## 현재 상황

데이터베이스 연결 시도 시 다음 오류 발생:
```
Connection timed out (0x0000274C/10060)
Is the server running on that host and accepting TCP/IP connections?
```

## 원인 분석

이 오류는 **네트워크 연결 문제**를 나타냅니다. RDS 인스턴스에 도달할 수 없는 상태입니다.

## 해결 방법

### 1️⃣ VPN 연결 확인 (가장 가능성 높음)

AWS RDS가 프라이빗 서브넷에 있는 경우, VPN을 통해서만 접근 가능합니다.

**확인 방법:**
```powershell
# RDS 엔드포인트에 ping 테스트
ping movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com

# 포트 연결 테스트
Test-NetConnection -ComputerName movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com -Port 5432
```

**해결:**
- 회사/프로젝트 VPN에 연결
- VPN 연결 후 다시 테스트

### 2️⃣ RDS 보안 그룹 확인

RDS 보안 그룹이 현재 IP 주소를 허용하지 않을 수 있습니다.

**AWS Console에서 확인:**
1. AWS Console → RDS → Databases → movie-dev-db
2. "Connectivity & security" 탭 클릭
3. "Security" 섹션에서 Security groups 클릭
4. Inbound rules 확인:
   - Type: PostgreSQL
   - Port: 5432
   - Source: 현재 IP 주소 또는 0.0.0.0/0 (개발용)

**현재 IP 확인:**
```powershell
# 현재 공인 IP 확인
Invoke-RestMethod -Uri "https://api.ipify.org?format=json"
```

### 3️⃣ RDS 퍼블릭 액세스 확인

RDS가 퍼블릭 액세스를 허용하지 않을 수 있습니다.

**AWS Console에서 확인:**
1. AWS Console → RDS → Databases → movie-dev-db
2. "Connectivity & security" 탭
3. "Public accessibility" 확인
   - Yes: 인터넷에서 접근 가능
   - No: VPC 내부에서만 접근 가능 (VPN 필요)

### 4️⃣ 네트워크 ACL 확인

VPC의 Network ACL이 트래픽을 차단할 수 있습니다.

**AWS Console에서 확인:**
1. AWS Console → VPC → Network ACLs
2. RDS 서브넷과 연결된 ACL 확인
3. Inbound/Outbound rules에서 포트 5432 허용 확인

### 5️⃣ 로컬 방화벽 확인

Windows 방화벽이 아웃바운드 연결을 차단할 수 있습니다.

```powershell
# 방화벽 상태 확인
Get-NetFirewallProfile | Select-Object Name, Enabled

# PostgreSQL 포트 테스트
Test-NetConnection -ComputerName movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com -Port 5432
```

## 임시 해결 방법

### Option A: 로컬 PostgreSQL 사용

개발 중에는 로컬 PostgreSQL을 사용할 수 있습니다:

1. **PostgreSQL 설치:**
   ```powershell
   # Chocolatey 사용
   choco install postgresql
   
   # 또는 공식 사이트에서 다운로드
   # https://www.postgresql.org/download/windows/
   ```

2. **로컬 데이터베이스 생성:**
   ```powershell
   # PostgreSQL 서비스 시작
   Start-Service postgresql-x64-16
   
   # 데이터베이스 생성
   psql -U postgres -c "CREATE DATABASE movie;"
   ```

3. **`.env` 파일 수정:**
   ```bash
   # 로컬 PostgreSQL 사용
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/movie
   ```

### Option B: AWS Systems Manager Session Manager

VPN 없이 AWS 리소스에 접근하는 방법:

```powershell
# AWS CLI로 포트 포워딩
aws ssm start-session --target <EC2-instance-id> `
  --document-name AWS-StartPortForwardingSessionToRemoteHost `
  --parameters '{\"host\":[\"movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com\"],\"portNumber\":[\"5432\"],\"localPortNumber\":[\"5432\"]}'
```

그 후 localhost:5432로 연결

## 연결 성공 후 다음 단계

연결이 성공하면:

```powershell
# 1. DB 연결 테스트
python backend/tests/db_connection_check.py

# 2. 마이그레이션 상태 확인
cd backend
alembic current

# 3. 마이그레이션 실행
alembic upgrade head

# 4. 테이블 확인
python tests/db_connection_check.py
```

## 도움 요청

위 방법으로 해결되지 않으면:

1. **네트워크 관리자에게 문의:**
   - RDS 엔드포인트: `movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com`
   - 포트: `5432`
   - 현재 IP 주소 제공

2. **AWS 관리자에게 문의:**
   - RDS 보안 그룹 설정 확인 요청
   - VPN 접근 권한 확인 요청

## 참고 자료

- [AWS RDS 연결 문제 해결](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Troubleshooting.html#CHAP_Troubleshooting.Connecting)
- [PostgreSQL 연결 문제](https://www.postgresql.org/docs/current/libpq-connect.html)
