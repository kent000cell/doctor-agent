"""도구 레지스트리 테스트"""

import pytest
from backend.tools.registry import ToolRegistry
from backend.skill_loader import SkillLoader
from data.mock_data import MockDataSource


class TestToolRegistry:
    """ToolRegistry 클래스 테스트"""

    @pytest.fixture
    def tool_registry(self, skill_loader, mock_data):
        """ToolRegistry fixture"""
        return ToolRegistry(mock_data, skill_loader)

    def test_tool_registry_initialization(self, tool_registry):
        """도구 레지스트리 초기화 테스트"""
        assert tool_registry is not None
        assert hasattr(tool_registry, '_tools')
        assert len(tool_registry._tools) > 0

    def test_analyze_symptoms(self, tool_registry):
        """증상 분석 도구 테스트"""
        result = tool_registry.execute("analyze_symptoms", {
            "symptoms": "허리가 아파요",
            "pain_scale": 7,
            "duration": "2주",
            "pain_type": "radiating"
        })

        assert result is not None
        assert "증상 분석 결과" in result
        assert "허리" in result or "통증" in result

    def test_get_patient_history(self, tool_registry):
        """환자 병력 조회 도구 테스트"""
        result = tool_registry.execute("get_patient_history", {
            "patient_id": "P001"
        })

        assert result is not None
        assert "환자 병력 조회" in result
        assert "P001" in result

    def test_analyze_xray(self, tool_registry):
        """X-ray 분석 도구 테스트"""
        result = tool_registry.execute("analyze_xray", {
            "body_part": "spine"
        })

        assert result is not None
        assert "X-ray 분석 결과" in result
        assert "척추" in result

    def test_analyze_mri(self, tool_registry):
        """MRI 분석 도구 테스트"""
        result = tool_registry.execute("analyze_mri", {
            "body_part": "spine"
        })

        assert result is not None
        assert "MRI 분석 결과" in result
        assert "척추" in result

    def test_analyze_ct(self, tool_registry):
        """CT 분석 도구 테스트"""
        result = tool_registry.execute("analyze_ct", {
            "body_part": "brain"
        })

        assert result is not None
        assert "CT 분석 결과" in result
        assert "뇌" in result

    def test_assess_severity(self, tool_registry):
        """심각도 평가 도구 테스트"""
        result = tool_registry.execute("assess_severity", {
            "diagnosis": "요추 추간판 탈출증",
            "symptoms_summary": "심한 통증",
            "imaging_summary": "L4-L5 디스크 탈출, 신경 압박"
        })

        assert result is not None
        assert "심각도 평가 결과" in result
        assert any(severity in result for severity in ["경증", "중등증", "중증"])

    def test_check_risk_factors(self, tool_registry):
        """위험 요소 체크 도구 테스트"""
        result = tool_registry.execute("check_risk_factors", {
            "age": 70,
            "conditions": ["당뇨", "고혈압"]
        })

        assert result is not None
        assert "위험 요소 평가" in result

    def test_recommend_treatment(self, tool_registry):
        """치료 추천 도구 테스트"""
        result = tool_registry.execute("recommend_treatment", {
            "diagnosis": "요추 추간판 탈출증",
            "severity": "moderate",
            "patient_age": 45
        })

        assert result is not None
        assert "치료 추천" in result
        assert "치료" in result

    def test_get_medication_options(self, tool_registry):
        """약물 옵션 조회 도구 테스트"""
        result = tool_registry.execute("get_medication_options", {
            "diagnosis": "요추 추간판 탈출증",
            "allergies": []
        })

        assert result is not None
        assert "약물 치료 옵션" in result

    def test_get_surgery_options(self, tool_registry):
        """수술 옵션 조회 도구 테스트"""
        result = tool_registry.execute("get_surgery_options", {
            "diagnosis": "요추 추간판 탈출증",
            "severity": "severe"
        })

        assert result is not None
        assert "수술 치료 옵션" in result

    def test_read_skill(self, tool_registry):
        """스킬 읽기 도구 테스트"""
        result = tool_registry.execute("read_skill", {
            "skill_name": "symptom-analysis"
        })

        assert result is not None
        assert "symptom-analysis" in result

    def test_nonexistent_tool(self, tool_registry):
        """존재하지 않는 도구 테스트"""
        result = tool_registry.execute("nonexistent_tool", {})

        assert "error" in result.lower() or "알 수 없는" in result

    def test_tool_with_invalid_args(self, tool_registry):
        """잘못된 인자로 도구 실행"""
        result = tool_registry.execute("analyze_symptoms", {
            # required 필드 누락
        })

        # 에러를 반환하거나 기본값으로 처리
        assert result is not None


class TestMockDataSource:
    """MockDataSource 테스트"""

    def test_analyze_symptoms_data(self, mock_data):
        """증상 분석 데이터 테스트"""
        result = mock_data.analyze_symptoms("허리", pain_scale=8, duration="2주")

        assert "analysis" in result
        assert "related_symptoms" in result
        assert "red_flags" in result
        assert "possible_diagnoses" in result

    def test_get_patient_history_data(self, mock_data):
        """환자 병력 데이터 테스트"""
        result = mock_data.get_patient_history("P001")

        assert "age" in result
        assert "gender" in result
        assert "medical_history" in result

    def test_analyze_xray_data(self, mock_data):
        """X-ray 분석 데이터 테스트"""
        result = mock_data.analyze_xray("spine")

        assert "findings" in result
        assert "abnormalities" in result
        assert "recommendation" in result

    def test_assess_severity_data(self, mock_data):
        """심각도 평가 데이터 테스트"""
        result = mock_data.assess_severity(
            "요추 추간판 탈출증",
            symptoms_summary="심한 통증",
            imaging_summary="디스크 탈출"
        )

        assert "severity" in result
        assert result["severity"] in ["mild", "moderate", "severe"]
        assert "urgency" in result
