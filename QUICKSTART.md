# Quick Start Guide

AI Doctor Agent를 빠르게 시작하는 방법

## 방법 1: 원클릭 실행 (권장)

```bash
# 1. OpenAI API 키 설정
export OPENAI_API_KEY="your-api-key-here"

# 2. 실행 (가상환경 자동 생성 + 의존성 설치 + 서버 시작)
python run.py
```

자동으로 브라우저에서 `http://localhost:3000` 열림

---

## 방법 2: 수동 설정

```bash
# 1. 가상환경 생성
python -m venv .venv

# 2. 가상환경 활성화
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3. 의존성 설치
pip install -r backend/requirements.txt

# 4. 환경 변수 설정
export OPENAI_API_KEY="your-api-key-here"

# 5. 백엔드 실행
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 6. 프론트엔드 실행 (새 터미널)
cd frontend
python -m http.server 3000
```

접속: http://localhost:3000

---

## 방법 3: Docker 실행

```bash
# 1. .env 파일 생성
cp .env.example .env
# .env 파일에서 OPENAI_API_KEY 설정

# 2. Docker Compose 실행
docker-compose up -d

# 3. 로그 확인
docker-compose logs -f

# 4. 중지
docker-compose down
```

접속: http://localhost:3000

---

## 테스트 실행

```bash
# 전체 테스트
pytest

# 커버리지 포함
pytest --cov=backend --cov-report=html

# 통합 테스트 포함 (OpenAI API 필요)
pytest --run-integration

# 특정 테스트만
pytest tests/test_api.py -v
```

---

## 사용 예시

### 1. 기본 증상 상담
```
허리가 아프고 다리가 저려요. 2주 정도 됐어요.
```

### 2. 이미지 + 증상
```
이 X-ray 사진을 분석해주세요. 허리가 많이 아픕니다.
[사진 첨부]
```

### 3. 빠른 증상 선택
UI에서 "허리 통증", "무릎 통증" 등 버튼 클릭

---

## API 직접 사용

### 헬스체크
```bash
curl http://localhost:8000/api/health
```

### 채팅 (SSE 스트리밍)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "허리가 아파요",
    "patient_id": "P001"
  }'
```

### 스킬 목록
```bash
curl http://localhost:8000/api/skills
```

---

## 문제 해결

### OpenAI API 키 오류
```
⚠ OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.
```
→ `export OPENAI_API_KEY="sk-..."` 실행

### 포트 충돌
```
ERROR: Address already in use
```
→ 다른 포트 사용: `uvicorn backend.main:app --port 8001`

### 의존성 오류
```
ModuleNotFoundError: No module named 'fastapi'
```
→ `pip install -r backend/requirements.txt` 재실행

---

## 다음 단계

- [README.md](README.md) - 전체 문서 읽기
- [API 문서](http://localhost:8000/docs) - FastAPI 자동 생성 문서
- [tests/](tests/) - 테스트 코드 살펴보기
- [skills/](skills/) - 스킬 커스터마이징
