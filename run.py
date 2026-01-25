#!/usr/bin/env python3
"""
AI Doctor Agent - 실행 스크립트
python run.py 하나로 모든 것을 실행
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# 경로 설정
ROOT_DIR = Path(__file__).parent.absolute()
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
VENV_DIR = ROOT_DIR / ".venv"

# Windows/Unix 구분
IS_WINDOWS = sys.platform == "win32"
PYTHON_BIN = VENV_DIR / ("Scripts" if IS_WINDOWS else "bin") / ("python.exe" if IS_WINDOWS else "python")
PIP_BIN = VENV_DIR / ("Scripts" if IS_WINDOWS else "bin") / ("pip.exe" if IS_WINDOWS else "pip")


def run_command(cmd: list, cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
    """명령어 실행"""
    print(f"  > {' '.join(str(c) for c in cmd)}")
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=False)


def setup_venv():
    """가상환경 설정"""
    print("\n[1/4] 가상환경 설정...")

    if not VENV_DIR.exists():
        print("  가상환경 생성 중...")
        run_command([sys.executable, "-m", "venv", str(VENV_DIR)])
        print("  ✓ 가상환경 생성 완료")
    else:
        print("  ✓ 가상환경이 이미 존재합니다")


def install_dependencies():
    """의존성 설치"""
    print("\n[2/4] 의존성 설치...")

    requirements = BACKEND_DIR / "requirements.txt"
    if requirements.exists():
        run_command([str(PIP_BIN), "install", "-r", str(requirements), "-q"])
        print("  ✓ 의존성 설치 완료")
    else:
        print("  ⚠ requirements.txt를 찾을 수 없습니다")


def check_api_key():
    """API 키 확인"""
    print("\n[2.5/4] OpenAI API 키 확인...")

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("  ⚠ OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("  다음 명령어로 설정하세요:")
        if IS_WINDOWS:
            print('    set OPENAI_API_KEY=your-api-key-here')
        else:
            print('    export OPENAI_API_KEY=your-api-key-here')
        print("")
        response = input("  API 키 없이 계속하시겠습니까? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print("  ✓ API 키 확인됨")


def start_backend():
    """백엔드 서버 시작"""
    print("\n[3/4] 백엔드 서버 시작 (port 8000)...")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = str(ROOT_DIR)

    process = subprocess.Popen(
        [
            str(PYTHON_BIN), "-m", "uvicorn",
            "backend.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ],
        cwd=ROOT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    print("  ✓ 백엔드 서버 시작됨")
    return process


def start_frontend():
    """프론트엔드 서버 시작"""
    print("\n[4/4] 프론트엔드 서버 시작 (port 3000)...")

    process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3000"],
        cwd=FRONTEND_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    print("  ✓ 프론트엔드 서버 시작됨")
    return process


def print_banner():
    """배너 출력"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║              🏥 AI Doctor Agent - Demo                       ║
║                  의료 AI 상담 에이전트                         ║
╚══════════════════════════════════════════════════════════════╝
""")


def print_urls():
    """URL 출력"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║  서버가 실행 중입니다!                                        ║
║                                                              ║
║  🌐 Frontend: http://localhost:3000                          ║
║  🔧 Backend:  http://localhost:8000                          ║
║  📚 API Docs: http://localhost:8000/docs                     ║
║                                                              ║
║  ⚠️  주의: 본 시스템은 AI 보조 진단 데모입니다.                 ║
║      실제 의료 진단을 대체하지 않습니다.                        ║
║                                                              ║
║  종료하려면 Ctrl+C를 누르세요                                  ║
╚══════════════════════════════════════════════════════════════╝
""")


def main():
    print_banner()

    try:
        # 1. 가상환경 설정
        setup_venv()

        # 2. 의존성 설치
        install_dependencies()

        # 2.5. API 키 확인
        check_api_key()

        # 3. 백엔드 시작
        backend_process = start_backend()

        # 4. 프론트엔드 시작
        frontend_process = start_frontend()

        # 서버 시작 대기
        time.sleep(2)

        print_urls()

        # 브라우저 열기
        print("  브라우저를 열고 있습니다...")
        webbrowser.open("http://localhost:3000")

        # 백엔드 로그 출력
        print("\n[Backend Logs]")
        print("-" * 60)

        while True:
            line = backend_process.stdout.readline()
            if line:
                print(line.rstrip())
            elif backend_process.poll() is not None:
                break

    except KeyboardInterrupt:
        print("\n\n종료 중...")

    finally:
        # 프로세스 종료
        try:
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except:
            pass

        print("서버가 종료되었습니다.")


if __name__ == "__main__":
    main()
