# Database Connection Information

## AWS RDS PostgreSQL 접속 정보

### 기본 정보
- **Host**: `movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com`
- **Port**: `5432`
- **Database**: `movie`
- **Username**: `postgres`
- **Password**: `peB63j)hVMvtor8*wPXwK9J[VmEJ`
- **Region**: `ap-northeast-2` (서울)

### SSL 설정
- **SSL Mode**: `require` (권장) 또는 `prefer`
- **SSL Certificate**: 필요시 AWS RDS CA 인증서 사용

---

## DBeaver 연결 설정

### 1. 새 연결 생성
1. DBeaver 실행
2. `Database` → `New Database Connection` 클릭
3. `PostgreSQL` 선택

### 2. 연결 정보 입력

**Main 탭:**
```
Host: movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com
Port: 5432
Database: movie  ⚠️ 반드시 입력! (비어있으면 에러 발생)
Username: postgres
Password: peB63j)hVMvtor8*wPXwK9J[VmEJ
```

**중요**: Database 필드가 비어있으면 "Invalid JDBC URL" 에러가 발생합니다. 
반드시 `movie`를 입력하세요!

**SSL 탭 (선택사항):**
```
SSL Mode: require
```

### 3. 연결 테스트
- `Test Connection` 버튼 클릭하여 연결 확인
- 드라이버가 없으면 자동으로 다운로드됩니다

### 4. 문제 해결

**"Invalid JDBC URL" 에러:**
- Database 필드에 `movie` 입력 확인
- Host에 포트 번호가 포함되지 않았는지 확인 (Host와 Port는 별도 필드)

**연결 타임아웃:**
- 방화벽 설정 확인
- 현재 IP가 보안 그룹에 허용되어 있는지 확인 (118.218.200.33/32)

**인증 실패:**
- Username: `postgres` (소문자)
- Password 복사 시 공백이 포함되지 않았는지 확인

---

## 다른 PostgreSQL 클라이언트

### pgAdmin
```
Host: movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com
Port: 5432
Maintenance database: movie
Username: postgres
Password: peB63j)hVMvtor8*wPXwK9J[VmEJ
```

### psql (Command Line)
```bash
psql -h movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com -p 5432 -U postgres -d movie
```

### DataGrip (JetBrains)
```
Host: movie-dev-db.cfyyuse8wwfa.ap-northeast-2.rds.amazonaws.com
Port: 5432
Database: movie
User: postgres
Password: peB63j)hVMvtor8*wPXwK9J[VmEJ
```

---

## 유용한 SQL 쿼리

### 테이블 목록 확인
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

### 영화 데이터 확인
```sql
-- 전체 영화 수
SELECT COUNT(*) FROM movies;

-- 최근 영화 10개
SELECT id, title, release, runtime 
FROM movies 
ORDER BY release DESC 
LIMIT 10;

-- 장르별 영화 수
SELECT genre, COUNT(*) as count 
FROM movie_genres 
GROUP BY genre 
ORDER BY count DESC;

-- 특정 영화의 상세 정보 (장르, 태그 포함)
SELECT 
    m.id,
    m.title,
    m.release,
    m.runtime,
    m.synopsis,
    ARRAY_AGG(DISTINCT mg.genre) as genres,
    ARRAY_AGG(DISTINCT mt.tag) as tags
FROM movies m
LEFT JOIN movie_genres mg ON m.id = mg.movie_id
LEFT JOIN movie_tags mt ON m.id = mt.movie_id
WHERE m.title LIKE '%주토피아%'
GROUP BY m.id, m.title, m.release, m.runtime, m.synopsis;
```

### 영화 검색 예제
```sql
-- 제목으로 검색
SELECT id, title, release, runtime 
FROM movies 
WHERE title LIKE '%아바타%'
ORDER BY release DESC;

-- 장르로 검색 (액션 영화)
SELECT DISTINCT m.id, m.title, m.release 
FROM movies m
JOIN movie_genres mg ON m.id = mg.movie_id
WHERE mg.genre = '액션'
ORDER BY m.release DESC
LIMIT 20;

-- 태그로 검색
SELECT DISTINCT m.id, m.title 
FROM movies m
JOIN movie_tags mt ON m.id = mt.movie_id
WHERE mt.tag IN ('sequel', 'buddy cop')
LIMIT 20;
```

### 통계 쿼리
```sql
-- 데이터베이스 통계
SELECT 
    (SELECT COUNT(*) FROM movies) as total_movies,
    (SELECT COUNT(*) FROM movie_genres) as total_genres,
    (SELECT COUNT(*) FROM movie_tags) as total_tags,
    (SELECT COUNT(*) FROM movie_vectors) as total_vectors;

-- 연도별 영화 수
SELECT 
    EXTRACT(YEAR FROM release) as year,
    COUNT(*) as count
FROM movies
WHERE release IS NOT NULL
GROUP BY year
ORDER BY year DESC;

-- 평균 러닝타임
SELECT 
    AVG(runtime) as avg_runtime,
    MIN(runtime) as min_runtime,
    MAX(runtime) as max_runtime
FROM movies
WHERE runtime IS NOT NULL;
```

---

## 보안 주의사항

⚠️ **중요**: 이 접속 정보는 개발 환경용입니다.
- 프로덕션 환경에서는 더 강력한 비밀번호 사용
- AWS Secrets Manager 사용 권장
- IP 화이트리스트 설정 (현재: 118.218.200.33/32)
- 정기적인 비밀번호 변경

---

## 현재 데이터베이스 상태

### 테이블 목록 (13개)
1. `alembic_version` - 마이그레이션 버전 관리
2. `users` - 사용자 정보
3. `movies` - 영화 메타데이터 (1,000개)
4. `movie_genres` - 영화 장르 (2,839개)
5. `movie_tags` - 영화 태그 (17,154개)
6. `movie_vectors` - 영화 벡터 데이터 (1,000개)
7. `reviews` - 리뷰
8. `comments` - 댓글
9. `review_likes` - 리뷰 좋아요
10. `taste_analysis` - 취향 분석
11. `group_decisions` - 그룹 결정
12. `group_members` - 그룹 멤버
13. `user_preferences` - 사용자 선호도

### 현재 데이터
- 영화: 1,000개
- 영화 장르: 2,839개
- 영화 태그: 17,154개
- 영화 벡터: 1,000개
