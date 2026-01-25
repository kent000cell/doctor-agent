"""Pytest configuration and fixtures"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# 프로젝트 루트를 Python 경로에 추가
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.main import app
from backend.skill_loader import SkillLoader
from backend.config import config
from data.mock_data import MockDataSource


@pytest.fixture
def client():
    """FastAPI TestClient fixture"""
    return TestClient(app)


@pytest.fixture
def skill_loader():
    """SkillLoader fixture"""
    return SkillLoader(config.skills_dir)


@pytest.fixture
def mock_data():
    """MockDataSource fixture"""
    return MockDataSource()


@pytest.fixture
def sample_symptoms():
    """샘플 증상 데이터"""
    return {
        "symptoms": "허리가 아파요",
        "pain_scale": 7,
        "duration": "2주",
        "pain_type": "radiating"
    }


@pytest.fixture
def sample_patient_id():
    """샘플 환자 ID"""
    return "P001"
