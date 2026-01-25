"""AI Doctor Agent - Main API Server

Agent Skills 스펙 기반 의료 AI 에이전트
"""

import json
import asyncio
import sys
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from openai import OpenAI, OpenAIError

# 경로 설정
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.config import config
from backend.skill_loader import SkillLoader
from backend.tools.registry import ToolRegistry
from backend.tools.definitions import TOOL_DEFINITIONS
from backend.logger import get_logger
from data import MockDataSource

# 로거 설정
logger = get_logger("main")


# === 초기화 ===

app = FastAPI(
    title="AI Doctor Agent API",
    description="Agent Skills 기반 AI 의료 보조 에이전트",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === 에러 핸들러 ===

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP 예외 핸들러"""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail} | Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """일반 예외 핸들러"""
    logger.error(f"Unhandled exception: {str(exc)} | Path: {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


# 컴포넌트 초기화
try:
    logger.info("Initializing AI Doctor Agent...")
    skill_loader = SkillLoader(config.skills_dir)
    logger.info(f"Loaded {len(skill_loader.skills)} skills")

    data_source = MockDataSource()
    logger.info("Mock data source initialized")

    tool_registry = ToolRegistry(data_source, skill_loader)
    logger.info("Tool registry initialized")

    openai_client = OpenAI(api_key=config.openai_api_key)
    logger.info(f"OpenAI client initialized (model: {config.openai_model})")
except Exception as e:
    logger.critical(f"Failed to initialize application: {str(e)}", exc_info=True)
    raise


# === 프롬프트 관리 ===

def load_prompt_template(name: str) -> str:
    """프롬프트 템플릿 로드"""
    prompt_path = config.prompts_dir / f"{name}.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"프롬프트를 찾을 수 없습니다: {name}")


def create_system_prompt() -> str:
    """시스템 프롬프트 생성 (템플릿 + 스킬 XML 주입)"""
    template = load_prompt_template("system")
    available_skills_xml = skill_loader.generate_available_skills_xml()
    return template.replace("{{available_skills}}", available_skills_xml)


# === 요청/응답 모델 ===

class ChatRequest(BaseModel):
    message: str
    patient_id: str = "P001"
    image: str | None = None  # Base64 인코딩된 이미지 (data:image/...;base64,...)


# === 채팅 처리 ===

def build_user_content(message: str, patient_id: str, image: str | None = None) -> list | str:
    """사용자 메시지 컨텐츠 생성 (텍스트 또는 멀티모달)"""
    user_text = f"[환자 ID: {patient_id}]\n\n{message}"

    if not image:
        return user_text

    # 멀티모달 컨텐츠 (텍스트 + 이미지)
    content = [
        {"type": "text", "text": user_text + "\n\n[첨부된 이미지를 분석해주세요. 피부 상태, 상처, 발진 등 의료적으로 관찰되는 소견을 설명해주세요.]"}
    ]

    # Base64 이미지 추가
    if image.startswith("data:"):
        content.append({
            "type": "image_url",
            "image_url": {"url": image}
        })
    else:
        # data: 프리픽스가 없으면 추가
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image}"}
        })

    return content


async def process_chat(message: str, patient_id: str = "P001", image: str | None = None) -> AsyncGenerator[str, None]:
    """채팅 처리 - SSE 스트리밍

    Agent Skills 스펙에 따른 동작:
    1. Discovery: 시작 시 스킬 메타데이터가 시스템 프롬프트에 포함됨
    2. Activation: LLM이 read_skill 도구로 필요한 스킬의 전체 내용을 로드
    3. Execution: LLM이 스킬 지침에 따라 도구들을 실행
    """

    # 사용자 메시지 생성 (이미지 포함 가능)
    user_content = build_user_content(message, patient_id, image)

    messages = [
        {"role": "system", "content": create_system_prompt()},
        {"role": "user", "content": user_content}
    ]

    # === 1단계: Discovery ===
    yield _log_event(
        "discovery",
        "🏥 AI Doctor Agent 시작",
        description="스킬 메타데이터 로드 완료"
    )
    await asyncio.sleep(0.1)

    skill_names = [s["name"] for s in skill_loader.list_skills()]
    yield _log_event(
        "skills_loaded",
        f"사용 가능한 스킬: {skill_names}",
        description="진단 및 치료 스킬 준비됨"
    )
    await asyncio.sleep(0.1)

    # 이미지 첨부 여부에 따른 로그
    if image:
        yield _log_event(
            "start",
            f"📷 이미지 첨부됨 - {message[:30]}...",
            description="이미지 + 증상 분석 시작"
        )
    else:
        yield _log_event(
            "start",
            f"환자 증상 접수: {message[:50]}...",
            description="증상 분석 시작"
        )
    await asyncio.sleep(0.1)

    # === 2단계: 에이전트 루프 ===
    max_iterations = 10
    for iteration in range(1, max_iterations + 1):
        yield _log_event(
            "llm_thinking",
            f"[진단 단계 #{iteration}] 분석 중...",
            description="AI가 증상을 분석하고 있습니다"
        )
        await asyncio.sleep(0.1)

        # OpenAI API 호출
        try:
            response = openai_client.chat.completions.create(
                model=config.openai_model,
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )
            logger.debug(f"OpenAI API response received (iteration {iteration})")
        except OpenAIError as e:
            error_msg = f"OpenAI API 오류: {str(e)}"
            logger.error(error_msg, exc_info=True)
            yield _log_event("error", error_msg)
            yield _response_event(f"죄송합니다. AI 서비스 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
            break
        except Exception as e:
            error_msg = f"예상치 못한 오류: {str(e)}"
            logger.error(error_msg, exc_info=True)
            yield _log_event("error", error_msg)
            yield _response_event(f"죄송합니다. 시스템 오류가 발생했습니다: {str(e)}")
            break

        choice = response.choices[0]
        assistant_message = choice.message

        # 도구 호출 처리
        if assistant_message.tool_calls:
            messages.append(assistant_message)

            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # 도구 유형에 따른 로그
                if tool_name == "read_skill":
                    yield _log_event(
                        "activation",
                        f"📚 스킬 로드: {tool_args.get('skill_name')}",
                        description="진단/치료 가이드라인 확인 중",
                        tool=tool_name,
                        args=tool_args
                    )
                elif tool_name.startswith("analyze"):
                    emoji = "🔬" if "xray" in tool_name or "mri" in tool_name or "ct" in tool_name else "🩺"
                    yield _log_event(
                        "tool_call",
                        f"{emoji} 분석 도구 실행: {tool_name}",
                        description="의료 데이터 분석 중",
                        tool=tool_name,
                        args=tool_args
                    )
                elif tool_name == "assess_severity":
                    yield _log_event(
                        "tool_call",
                        f"⚖️ 심각도 평가 중",
                        description="질병 진행 단계 판단",
                        tool=tool_name,
                        args=tool_args
                    )
                elif tool_name == "recommend_treatment":
                    yield _log_event(
                        "tool_call",
                        f"💊 치료법 검색 중",
                        description="최적의 치료 옵션 탐색",
                        tool=tool_name,
                        args=tool_args
                    )
                else:
                    yield _log_event(
                        "tool_call",
                        f"🔧 도구 실행: {tool_name}",
                        tool=tool_name,
                        args=tool_args
                    )
                await asyncio.sleep(0.1)

                # 도구 실행
                try:
                    logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
                    tool_result = tool_registry.execute(tool_name, tool_args)
                    logger.debug(f"Tool {tool_name} executed successfully")

                    yield _log_event(
                        "tool_result",
                        f"✅ {tool_name} 완료",
                        tool=tool_name,
                        result=tool_result[:300] if len(tool_result) > 300 else tool_result
                    )
                except Exception as e:
                    error_msg = f"도구 실행 오류 ({tool_name}): {str(e)}"
                    logger.error(error_msg, exc_info=True)
                    tool_result = json.dumps({"error": error_msg}, ensure_ascii=False)
                    yield _log_event("error", error_msg)

                await asyncio.sleep(0.1)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })

        # 최종 응답
        else:
            yield _log_event(
                "complete",
                "📋 진단 및 치료 추천 완료",
                description="AI 분석이 완료되었습니다"
            )
            yield _response_event(assistant_message.content)
            break


def _log_event(step: str, message: str, **extra) -> str:
    """로그 이벤트 생성"""
    data = {"step": step, "message": message, **extra}
    return json.dumps({"type": "log", "data": data}, ensure_ascii=False) + "\n"


def _response_event(content: str) -> str:
    """응답 이벤트 생성"""
    return json.dumps({"type": "response", "data": {"content": content}}, ensure_ascii=False) + "\n"


# === API 엔드포인트 ===

@app.get("/api/skills")
async def get_skills():
    """스킬 목록 반환"""
    try:
        logger.info("Fetching skills list")
        return {
            "skills": skill_loader.list_skills(),
            "xml": skill_loader.generate_available_skills_xml(),
        }
    except Exception as e:
        logger.error(f"Failed to fetch skills: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch skills")


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """채팅 API - SSE 스트리밍 (이미지 첨부 지원)"""
    try:
        logger.info(f"Chat request received | patient_id: {request.patient_id} | message: {request.message[:50]}...")
        if request.image:
            logger.info("Image attached to request")

        return StreamingResponse(
            process_chat(request.message, request.patient_id, request.image),
            media_type="text/event-stream"
        )
    except Exception as e:
        logger.error(f"Chat processing failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Chat processing failed")


@app.get("/api/health")
async def health():
    """헬스체크"""
    try:
        return {
            "status": "ok",
            "agent": "AI Doctor Agent",
            "skills_count": len(skill_loader.skills),
            "model": config.openai_model,
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        }


# === 직접 실행 ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.host, port=config.port)
