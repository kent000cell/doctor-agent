"""AI Doctor Agent - Logging Configuration"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "doctor-agent", log_level: str = "INFO") -> logging.Logger:
    """로거 설정

    Args:
        name: 로거 이름
        log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        설정된 로거 객체
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # 기존 핸들러 제거 (중복 방지)
    logger.handlers.clear()

    # 포맷 설정
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 파일 핸들러 (logs 디렉토리에 저장)
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"doctor-agent-{today}.log"

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 에러 파일 핸들러 (에러만 별도 저장)
    error_file = log_dir / f"error-{today}.log"
    error_handler = logging.FileHandler(error_file, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    return logger


# 전역 로거 인스턴스
logger = setup_logger()


def get_logger(name: str = None) -> logging.Logger:
    """로거 가져오기

    Args:
        name: 로거 이름 (None이면 기본 로거 반환)

    Returns:
        로거 객체
    """
    if name:
        return logging.getLogger(f"doctor-agent.{name}")
    return logger
