"""AI Doctor Agent - Tool Definitions

OpenAI Function Calling 스키마 정의
"""

TOOL_DEFINITIONS = [
    # === 증상 분석 도구 ===
    {
        "type": "function",
        "function": {
            "name": "analyze_symptoms",
            "description": "환자 증상 분석. 통증 위치, 강도, 특성, 지속기간을 파악하여 진단에 필요한 정보 추출.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symptoms": {
                        "type": "string",
                        "description": "환자가 호소하는 증상 (예: 허리 통증, 두통, 무릎 통증)"
                    },
                    "pain_scale": {
                        "type": "integer",
                        "description": "통증 강도 1-10 (1: 경미, 10: 극심)"
                    },
                    "duration": {
                        "type": "string",
                        "description": "증상 지속 기간 (예: 3일, 2주, 1개월)"
                    },
                    "pain_type": {
                        "type": "string",
                        "enum": ["dull", "sharp", "radiating", "throbbing", "burning"],
                        "description": "통증 유형 (둔통/찌르는/방사통/박동성/화끈거림)"
                    }
                },
                "required": ["symptoms"]
            }
        }
    },

    # === 환자 병력 조회 ===
    {
        "type": "function",
        "function": {
            "name": "get_patient_history",
            "description": "환자 과거 병력, 수술 이력, 알레르기, 복용 약물 조회.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "환자 ID"
                    }
                },
                "required": ["patient_id"]
            }
        }
    },

    # === X-ray 분석 ===
    {
        "type": "function",
        "function": {
            "name": "analyze_xray",
            "description": "X-ray 영상 분석. 골절, 디스크 간격, 관절 이상, 폐 병변 등 탐지.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_data": {
                        "type": "string",
                        "description": "X-ray 이미지 (base64 또는 URL)"
                    },
                    "body_part": {
                        "type": "string",
                        "enum": ["spine", "chest", "knee", "shoulder", "hip", "ankle", "wrist", "pelvis"],
                        "description": "촬영 부위"
                    }
                },
                "required": ["body_part"]
            }
        }
    },

    # === MRI 분석 ===
    {
        "type": "function",
        "function": {
            "name": "analyze_mri",
            "description": "MRI 영상 분석. 디스크 탈출, 인대 손상, 연골 파열, 뇌 병변 등 탐지.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_data": {
                        "type": "string",
                        "description": "MRI 이미지 (base64 또는 URL)"
                    },
                    "body_part": {
                        "type": "string",
                        "enum": ["spine", "brain", "knee", "shoulder", "hip"],
                        "description": "촬영 부위"
                    }
                },
                "required": ["body_part"]
            }
        }
    },

    # === CT 분석 ===
    {
        "type": "function",
        "function": {
            "name": "analyze_ct",
            "description": "CT 영상 분석. 뇌출혈, 복부 장기 이상, 폐색전 등 탐지.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_data": {
                        "type": "string",
                        "description": "CT 이미지 (base64 또는 URL)"
                    },
                    "body_part": {
                        "type": "string",
                        "enum": ["brain", "chest", "abdomen", "pelvis"],
                        "description": "촬영 부위"
                    }
                },
                "required": ["body_part"]
            }
        }
    },

    # === 심각도 평가 ===
    {
        "type": "function",
        "function": {
            "name": "assess_severity",
            "description": "질병 심각도 평가. 경증/중등증/중증 분류 및 긴급도 판단.",
            "parameters": {
                "type": "object",
                "properties": {
                    "diagnosis": {
                        "type": "string",
                        "description": "예상 진단명 (예: 요추 추간판 탈출증, 골절)"
                    },
                    "symptoms_summary": {
                        "type": "string",
                        "description": "증상 분석 결과 요약"
                    },
                    "imaging_summary": {
                        "type": "string",
                        "description": "영상 분석 결과 요약 (있는 경우)"
                    }
                },
                "required": ["diagnosis"]
            }
        }
    },

    # === 위험 요소 체크 ===
    {
        "type": "function",
        "function": {
            "name": "check_risk_factors",
            "description": "환자 위험 요소 체크. 나이, 기저질환, 생활습관 등 평가.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "환자 ID"
                    },
                    "age": {
                        "type": "integer",
                        "description": "환자 나이"
                    },
                    "conditions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "기저질환 목록 (당뇨, 고혈압 등)"
                    }
                },
                "required": []
            }
        }
    },

    # === 치료 추천 ===
    {
        "type": "function",
        "function": {
            "name": "recommend_treatment",
            "description": "종합 치료법 추천. 수술/비수술 판단, 치료 옵션 제시.",
            "parameters": {
                "type": "object",
                "properties": {
                    "diagnosis": {
                        "type": "string",
                        "description": "진단명"
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["mild", "moderate", "severe"],
                        "description": "심각도"
                    },
                    "patient_age": {
                        "type": "integer",
                        "description": "환자 나이"
                    },
                    "contraindications": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "금기사항 (알레르기, 기저질환 등)"
                    }
                },
                "required": ["diagnosis", "severity"]
            }
        }
    },

    # === 약물 옵션 조회 ===
    {
        "type": "function",
        "function": {
            "name": "get_medication_options",
            "description": "약물 치료 옵션 조회. 진단에 맞는 약물 목록 및 용법 제공.",
            "parameters": {
                "type": "object",
                "properties": {
                    "diagnosis": {
                        "type": "string",
                        "description": "진단명"
                    },
                    "allergies": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "알레르기 목록"
                    }
                },
                "required": ["diagnosis"]
            }
        }
    },

    # === 수술 옵션 조회 ===
    {
        "type": "function",
        "function": {
            "name": "get_surgery_options",
            "description": "수술 옵션 조회. 진단에 맞는 수술 방법, 장단점, 회복기간 제공.",
            "parameters": {
                "type": "object",
                "properties": {
                    "diagnosis": {
                        "type": "string",
                        "description": "진단명"
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["moderate", "severe"],
                        "description": "심각도"
                    }
                },
                "required": ["diagnosis"]
            }
        }
    },

    # === 스킬 읽기 ===
    {
        "type": "function",
        "function": {
            "name": "read_skill",
            "description": "스킬 문서(SKILL.md)를 읽어 작업 수행 방법을 확인.",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_name": {
                        "type": "string",
                        "description": "스킬 이름 (symptom-analysis, imaging-analysis, disease-assessment, treatment-recommendation)"
                    }
                },
                "required": ["skill_name"]
            }
        }
    }
]
