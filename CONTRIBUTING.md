# Contributing Guide

AI Doctor Agent 프로젝트에 기여해주셔서 감사합니다!

## 개발 환경 설정

```bash
# 1. 저장소 클론
git clone https://github.com/yourusername/doctor-agent.git
cd doctor-agent

# 2. 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 개발 의존성 설치
pip install -r backend/requirements.txt

# 4. 환경 변수 설정
cp .env.example .env
# .env 파일에서 OPENAI_API_KEY 설정
```

## 코드 스타일

- Python: PEP 8 준수
- 들여쓰기: 4 spaces
- 최대 줄 길이: 100자
- Docstring: Google Style

## 테스트

모든 PR은 테스트를 포함해야 합니다.

```bash
# 테스트 실행
pytest

# 커버리지 확인
pytest --cov=backend --cov-report=html
```

## 커밋 메시지

```
<type>: <subject>

<body>

<footer>
```

**Type:**
- feat: 새 기능
- fix: 버그 수정
- docs: 문서 변경
- test: 테스트 추가/수정
- refactor: 리팩토링
- style: 코드 스타일 변경
- chore: 빌드/설정 변경

**예시:**
```
feat: Add patient authentication

- JWT 토큰 기반 인증 추가
- 환자 데이터 보안 강화

Closes #123
```

## Pull Request 프로세스

1. Feature 브랜치 생성: `git checkout -b feat/your-feature`
2. 변경사항 커밋
3. 테스트 통과 확인
4. PR 생성
5. 코드 리뷰 대기
6. Merge

## 새 스킬 추가하기

```bash
# 1. 스킬 디렉토리 생성
mkdir skills/your-skill-name

# 2. SKILL.md 작성
cat > skills/your-skill-name/SKILL.md << EOF
---
name: your-skill-name
description: 스킬 설명
allowed-tools: tool1, tool2
---

# 스킬 제목

## 개요
...
EOF

# 3. 필요한 도구를 backend/tools/definitions.py에 추가
# 4. 도구 구현을 backend/tools/registry.py에 추가
# 5. 테스트 작성
```

## 라이선스

Apache License 2.0
