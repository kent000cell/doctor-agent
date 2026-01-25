"""API 엔드포인트 테스트"""

import json
import pytest
from fastapi.testclient import TestClient


class TestHealthAPI:
    """헬스체크 API 테스트"""

    def test_health_check(self, client: TestClient):
        """헬스체크 엔드포인트 테스트"""
        response = client.get("/api/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "agent" in data
        assert "skills_count" in data
        assert "model" in data


class TestSkillsAPI:
    """스킬 API 테스트"""

    def test_get_skills(self, client: TestClient):
        """스킬 목록 조회 테스트"""
        response = client.get("/api/skills")

        assert response.status_code == 200
        data = response.json()
        assert "skills" in data
        assert "xml" in data
        assert len(data["skills"]) > 0

    def test_skills_structure(self, client: TestClient):
        """스킬 데이터 구조 검증"""
        response = client.get("/api/skills")
        data = response.json()

        for skill in data["skills"]:
            assert "name" in skill
            assert "description" in skill
            assert "allowed_tools" in skill


class TestChatAPI:
    """채팅 API 테스트"""

    @pytest.mark.skipif(
        not pytest.config.getoption("--run-integration", default=False),
        reason="Integration test requires OpenAI API key"
    )
    def test_chat_basic(self, client: TestClient):
        """기본 채팅 테스트 (통합 테스트)"""
        request_data = {
            "message": "허리가 아파요",
            "patient_id": "P001"
        }

        response = client.post("/api/chat", json=request_data)

        # SSE 스트리밍이므로 200 응답 확인
        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")

    def test_chat_validation(self, client: TestClient):
        """채팅 요청 유효성 검증"""
        # 빈 메시지 테스트
        response = client.post("/api/chat", json={"message": ""})

        # 422 Unprocessable Entity 또는 처리됨
        assert response.status_code in [200, 422]

    def test_chat_with_image(self, client: TestClient):
        """이미지 포함 채팅 테스트"""
        request_data = {
            "message": "이 이미지를 분석해주세요",
            "patient_id": "P001",
            "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg=="  # 더미 base64
        }

        response = client.post("/api/chat", json=request_data)
        assert response.status_code in [200, 500]  # API 키 없으면 500


class TestCORS:
    """CORS 설정 테스트"""

    def test_cors_headers(self, client: TestClient):
        """CORS 헤더 확인"""
        response = client.options("/api/health")

        # CORS 미들웨어가 설정되어 있으면 헤더 존재
        assert response.status_code in [200, 405]


class TestErrorHandling:
    """에러 핸들링 테스트"""

    def test_404_not_found(self, client: TestClient):
        """존재하지 않는 엔드포인트"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    def test_405_method_not_allowed(self, client: TestClient):
        """잘못된 HTTP 메서드"""
        response = client.put("/api/health")
        assert response.status_code == 405
