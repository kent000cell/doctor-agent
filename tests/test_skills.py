"""스킬 로더 테스트"""

import pytest
from pathlib import Path
from backend.skill_loader import SkillLoader, SkillMetadata


class TestSkillLoader:
    """SkillLoader 클래스 테스트"""

    def test_skill_loader_initialization(self, skill_loader: SkillLoader):
        """스킬 로더 초기화 테스트"""
        assert skill_loader is not None
        assert isinstance(skill_loader.skills, dict)

    def test_discover_skills(self, skill_loader: SkillLoader):
        """스킬 Discovery 테스트"""
        # 최소 1개 이상의 스킬이 발견되어야 함
        assert len(skill_loader.skills) >= 1

        # 기대되는 스킬들
        expected_skills = [
            "symptom-analysis",
            "imaging-analysis",
            "disease-assessment",
            "treatment-recommendation"
        ]

        for skill_name in expected_skills:
            assert skill_name in skill_loader.skills

    def test_skill_metadata_structure(self, skill_loader: SkillLoader):
        """스킬 메타데이터 구조 검증"""
        for skill_name, skill in skill_loader.skills.items():
            assert skill.metadata is not None
            assert isinstance(skill.metadata, SkillMetadata)
            assert skill.metadata.name == skill_name
            assert skill.metadata.description is not None
            assert skill.metadata.location is not None

    def test_generate_available_skills_xml(self, skill_loader: SkillLoader):
        """스킬 XML 생성 테스트"""
        xml = skill_loader.generate_available_skills_xml()

        assert "<available_skills>" in xml
        assert "</available_skills>" in xml
        assert "<skill>" in xml
        assert "<name>" in xml
        assert "<description>" in xml

    def test_get_skill_content(self, skill_loader: SkillLoader):
        """스킬 컨텐츠 로드 테스트 (Activation)"""
        content = skill_loader.get_skill_content("symptom-analysis")

        assert content is not None
        assert len(content) > 0
        assert "---" in content  # YAML frontmatter
        assert "symptom-analysis" in content

    def test_get_nonexistent_skill(self, skill_loader: SkillLoader):
        """존재하지 않는 스킬 조회"""
        content = skill_loader.get_skill_content("nonexistent-skill")
        assert content is None

    def test_list_skills(self, skill_loader: SkillLoader):
        """스킬 목록 반환 테스트"""
        skills_list = skill_loader.list_skills()

        assert isinstance(skills_list, list)
        assert len(skills_list) > 0

        for skill in skills_list:
            assert "name" in skill
            assert "description" in skill


class TestSkillContent:
    """스킬 컨텐츠 검증"""

    def test_symptom_analysis_skill(self, skill_loader: SkillLoader):
        """증상 분석 스킬 내용 검증"""
        content = skill_loader.get_skill_content("symptom-analysis")

        assert content is not None
        assert "analyze_symptoms" in content
        assert "통증" in content

    def test_imaging_analysis_skill(self, skill_loader: SkillLoader):
        """영상 분석 스킬 내용 검증"""
        content = skill_loader.get_skill_content("imaging-analysis")

        assert content is not None
        assert any(keyword in content for keyword in ["X-ray", "MRI", "CT"])

    def test_disease_assessment_skill(self, skill_loader: SkillLoader):
        """질병 평가 스킬 내용 검증"""
        content = skill_loader.get_skill_content("disease-assessment")

        assert content is not None
        assert "assess_severity" in content
        assert any(keyword in content for keyword in ["경증", "중등증", "중증"])

    def test_treatment_recommendation_skill(self, skill_loader: SkillLoader):
        """치료 추천 스킬 내용 검증"""
        content = skill_loader.get_skill_content("treatment-recommendation")

        assert content is not None
        assert "recommend_treatment" in content
        assert "치료" in content


class TestSkillIntegrity:
    """스킬 무결성 테스트"""

    def test_all_skills_have_markdown_files(self, skill_loader: SkillLoader):
        """모든 스킬이 SKILL.md 파일을 가지고 있는지 확인"""
        for skill_name, skill in skill_loader.skills.items():
            skill_md = skill.path / "SKILL.md"
            assert skill_md.exists(), f"{skill_name} SKILL.md not found"

    def test_skill_allowed_tools(self, skill_loader: SkillLoader):
        """스킬의 allowed-tools 필드 확인"""
        for skill_name, skill in skill_loader.skills.items():
            # allowed-tools는 선택사항이므로 None이어도 됨
            if skill.metadata.allowed_tools:
                assert isinstance(skill.metadata.allowed_tools, str)
