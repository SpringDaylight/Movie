# 🔥 네트워크 연결 문제 해결

## 현재 상황

모든 AWS 설정은 정상이지만 로컬에서 RDS로 연결이 안 되는 상황입니다.

### 확인된 정상 설정:
- ✓ 보안 그룹: PostgreSQL 포트 5432 허용 (118.218.200.33/32)
- ✓ RDS Public Accessibility: Yes
- ✓ Network ACL: 모든 트래픽 허용
- ✓ DNS 해석: 정상 (43.203.9.28)

### 문제:
- ❌ 로컬에서 RDS 포트 5432로 연결 시도 시 타임아웃 발생

## 해결 방법

### 방법 1: Windows 방화벽 확인 및 해제 (가장 가능성 높음)

#### 1-1. 방화벽 상태 확인
```powershell
# PowerShell에서 실행
Get-NetFirewallProfile | Select-Object Name, Enabled
```

#### 1-2. 방화벽 임시 비활성화 (테스트용)
```powershell
# PowerShell을 관리자 권한으로 실행 후
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# 테스트 후 다시 활성화
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

#### 1-3. Python에 대한 방화벽 규칙 추가
```powershell
# PowerShell을 관리자 권한으로 실행
New-NetFirewallRule -DisplayName "Python PostgreSQL" -Direction Outbound -Program "C:\Users\DS18\AppData\Local\Programs\Python\Python312\python.exe" -Action Allow -Protocol TCP -RemotePort 5432
```

### 방법 2: 다른 네트워크에서 테스트

#### 2-1. 모바일 핫스팟 사용
1. 휴대폰의 모바일 핫스팟 활성화
2. PC를 핫스팟에 연결
3. 다시 연결 테스트:
   ```powershell
   python backend/scripts/direct_psycopg2_test.py
   ```

#### 2-2. 다른 Wi-Fi 네트워크
- 카페, 도서관 등 다른 Wi-Fi에서 테스트

### 방법 3: 안티바이러스 소프트웨어 확인

안티바이러스가 Python의 네트워크 연결을 차단할 수 있습니다.

1. 안티바이러스 임시 비활성화
2. 연결 테스트
3. 성공하면 Python을 예외 목록에 추가

### 방법 4: 회사 네트워크 정책 확인

회사 네트워크에서 작업 중이라면:
- IT 부서에 문의하여 포트 5432 아웃바운드 연결 허용 요청
- VPN 사용이 필요한지 확인

### 방법 5: Telnet으로 포트 연결 테스트

```powershell
# Telnet 클라이언트 설치 (Windows 기능)
dism /online /Enable-Feature /FeatureName:TelnetClient

# 포트 연결 테스트
telnet movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com 5432
```

- 연결되면: 화면이 깜빡이거나 빈 화면 (정상)
- 연결 안 되면: "연결할 수 없습니다" 메시지

### 방법 6: AWS Systems Manager Session Manager (고급)

VPN 없이 AWS 리소스에 접근하는 방법:

1. EC2 인스턴스 생성 (같은 VPC에)
2. Session Manager로 EC2에 접속
3. EC2에서 RDS로 포트 포워딩:
   ```bash
   ssh -L 5432:movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com:5432 ec2-user@localhost
   ```
4. 로컬에서 localhost:5432로 연결

## 테스트 스크립트

### 1. 포트 연결 테스트
```powershell
python backend/scripts/test_port_connection.py
```

### 2. 직접 psycopg2 연결 테스트
```powershell
python backend/scripts/direct_psycopg2_test.py
```

### 3. 전체 DB 연결 테스트
```powershell
python backend/tests/db_connection_check.py
```

## 성공 후 다음 단계

연결이 성공하면:

```powershell
# 1. 마이그레이션 상태 확인
cd backend
alembic current

# 2. 마이그레이션 실행
alembic upgrade head

# 3. 테이블 확인
python tests/db_connection_check.py

# 4. API 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 추가 도움

위 방법으로 해결되지 않으면:
1. 네트워크 관리자에게 문의
2. ISP(인터넷 서비스 제공자)에 문의
3. AWS Support에 문의

## 참고

- 현재 IP: 118.218.200.33
- RDS 엔드포인트: movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com
- RDS IP: 43.203.9.28
- 포트: 5432
