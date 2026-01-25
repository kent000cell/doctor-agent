"""AI Doctor Agent - Configuration"""

import os
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Config:
    """애플리케이션 설정"""

    # 경로
    base_dir: Path = Path(__file__).parent.parent
    skills_dir: Path = None
    prompts_dir: Path = None
    data_dir: Path = None

    # 서버
    host: str = "0.0.0.0"
    port: int = 8000

    # OpenAI
    openai_api_key: str = None
    openai_model: str = "gpt-4o"

    def __post_init__(self):
        self.skills_dir = self.base_dir / "skills"
        self.prompts_dir = self.base_dir / "prompts"
        self.data_dir = self.base_dir / "data"
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")


config = Config()
