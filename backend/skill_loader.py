"""AI Doctor Agent - Skill Loader

Agent Skills 스펙 준수 스킬 로더
Progressive Disclosure 패턴 구현
"""

from pathlib import Path
from typing import Optional
from dataclasses import dataclass
import yaml


@dataclass
class SkillMetadata:
    """스킬 메타데이터 (Discovery 단계에서 로드)"""
    name: str
    description: str
    location: str
    license: Optional[str] = None
    allowed_tools: Optional[str] = None


@dataclass
class Skill:
    """스킬 전체 정보"""
    metadata: SkillMetadata
    path: Path
    content: Optional[str] = None


class SkillLoader:
    """스킬 로더 - Agent Skills 스펙 준수"""

    def __init__(self, skills_dir: str | Path):
        self.skills_dir = Path(skills_dir)
        self.skills: dict[str, Skill] = {}
        self._discover()

    def _discover(self) -> None:
        """Discovery 단계: 모든 스킬의 메타데이터만 로드"""
        if not self.skills_dir.exists():
            return

        for skill_path in self.skills_dir.iterdir():
            if not skill_path.is_dir():
                continue

            skill_md = skill_path / "SKILL.md"
            if not skill_md.exists():
                continue

            metadata = self._parse_frontmatter(skill_md)
            if metadata:
                self.skills[metadata.name] = Skill(
                    metadata=metadata,
                    path=skill_path,
                    content=None,
                )

    def _parse_frontmatter(self, skill_md: Path) -> Optional[SkillMetadata]:
        """SKILL.md에서 YAML frontmatter 파싱"""
        try:
            content = skill_md.read_text(encoding="utf-8")
        except Exception:
            return None

        if not content.startswith("---"):
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            return None

        try:
            data = yaml.safe_load(parts[1])
        except yaml.YAMLError:
            return None

        if not data or "name" not in data or "description" not in data:
            return None

        return SkillMetadata(
            name=data["name"],
            description=data["description"],
            location=str(skill_md.absolute()),
            license=data.get("license"),
            allowed_tools=data.get("allowed-tools"),
        )

    def generate_available_skills_xml(self) -> str:
        """<available_skills> XML 생성 - 시스템 프롬프트 주입용"""
        lines = ["<available_skills>"]

        for skill in self.skills.values():
            meta = skill.metadata
            lines.append("  <skill>")
            lines.append(f"    <name>{meta.name}</name>")
            lines.append(f"    <description>{meta.description}</description>")
            lines.append(f"    <allowed-tools>{meta.allowed_tools or 'all'}</allowed-tools>")
            lines.append("  </skill>")

        lines.append("</available_skills>")
        return "\n".join(lines)

    def get_skill_content(self, skill_name: str) -> Optional[str]:
        """Activation 단계: 스킬 전체 내용 로드"""
        if skill_name not in self.skills:
            return None

        skill = self.skills[skill_name]

        if skill.content is None:
            skill_md = skill.path / "SKILL.md"
            try:
                skill.content = skill_md.read_text(encoding="utf-8")
            except Exception:
                return None

        return skill.content

    def list_skills(self) -> list[dict]:
        """스킬 목록 반환"""
        return [
            {
                "name": skill.metadata.name,
                "description": skill.metadata.description,
                "allowed_tools": skill.metadata.allowed_tools,
            }
            for skill in self.skills.values()
        ]
