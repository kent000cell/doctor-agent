"""AI Doctor Agent - Mock Data Source

실제 의료 데이터베이스 대신 사용하는 목업 데이터.
프로토타입 및 데모용.
"""

from typing import Optional


class MockDataSource:
    """목업 데이터 소스"""

    def __init__(self):
        # 환자 데이터
        self.patients = {
            "P001": {
                "age": 45,
                "gender": "남성",
                "medical_history": ["고혈압 (2018~)", "당뇨병 전단계"],
                "surgeries": ["충수절제술 (2010)"],
                "allergies": ["페니실린"],
                "current_medications": ["혈압약 (아모디핀 5mg)"]
            },
            "P002": {
                "age": 32,
                "gender": "여성",
                "medical_history": ["편두통"],
                "surgeries": [],
                "allergies": [],
                "current_medications": []
            },
            "default": {
                "age": 40,
                "gender": "미상",
                "medical_history": [],
                "surgeries": [],
                "allergies": [],
                "current_medications": []
            }
        }

        # 증상별 분석 데이터
        self.symptom_analysis = {
            "허리": {
                "analysis": "요추부 통증으로 추정됩니다. 디스크 질환, 근육통, 척추관 협착증 등이 의심됩니다.",
                "related_symptoms": ["다리 저림", "보행 장애", "앉기 힘듦", "기침/재채기 시 악화"],
                "red_flags": [],
                "possible_diagnoses": ["요추 추간판 탈출증", "요추 염좌", "척추관 협착증"]
            },
            "두통": {
                "analysis": "두통의 양상과 동반 증상에 따라 긴장성 두통, 편두통, 군발두통 등이 의심됩니다.",
                "related_symptoms": ["메스꺼움", "빛 과민", "소리 과민", "시야 이상"],
                "red_flags": ["갑작스러운 극심한 두통", "발열 동반", "의식 저하"],
                "possible_diagnoses": ["긴장성 두통", "편두통", "경추성 두통"]
            },
            "무릎": {
                "analysis": "무릎 통증으로 관절염, 인대 손상, 반월판 파열 등이 의심됩니다.",
                "related_symptoms": ["붓기", "열감", "삐걱거림", "무릎 잠김"],
                "red_flags": ["외상 후 급성 부종", "무릎 변형"],
                "possible_diagnoses": ["퇴행성 관절염", "반월판 파열", "전방십자인대 손상"]
            },
            "default": {
                "analysis": "증상에 대한 추가 정보가 필요합니다.",
                "related_symptoms": ["피로", "불편감"],
                "red_flags": [],
                "possible_diagnoses": ["추가 검사 필요"]
            }
        }

        # 영상 분석 데이터
        self.imaging_data = {
            "xray": {
                "spine": {
                    "findings": "요추 4-5번 디스크 간격 감소 소견. 골극 형성 관찰.",
                    "abnormalities": ["L4-L5 디스크 간격 협소", "경미한 골극 형성", "요추 전만 감소"],
                    "normal_findings": ["골절 소견 없음", "척추 정렬 양호"],
                    "recommendation": "증상 지속 시 MRI 검사 권장"
                },
                "chest": {
                    "findings": "폐야 청명. 심비대 소견 없음.",
                    "abnormalities": [],
                    "normal_findings": ["폐야 청명", "심장 크기 정상", "횡격막 정상"],
                    "recommendation": "특이 소견 없음"
                },
                "knee": {
                    "findings": "내측 관절 간격 경미한 협소. 퇴행성 변화 의심.",
                    "abnormalities": ["내측 관절 간격 협소", "경미한 골극"],
                    "normal_findings": ["골절 소견 없음", "외측 관절 정상"],
                    "recommendation": "증상에 따라 MRI 검사 고려"
                }
            },
            "mri": {
                "spine": {
                    "findings": "L4-L5 추간판 탈출 소견. 좌측 신경근 압박 관찰.",
                    "abnormalities": ["L4-L5 추간판 탈출 (후방 중심성)", "좌측 L5 신경근 압박", "경미한 척추관 협착"],
                    "detailed_analysis": "L4-L5 레벨에서 추간판이 후방으로 약 5mm 탈출되어 좌측 L5 신경근을 압박하고 있습니다. 척수 압박 소견은 없습니다.",
                    "conclusion": "L4-L5 추간판 탈출증 (좌측 신경근병증 동반)"
                },
                "knee": {
                    "findings": "내측 반월판 후각부 파열 소견.",
                    "abnormalities": ["내측 반월판 수평 파열", "관절 삼출액 소량"],
                    "detailed_analysis": "내측 반월판 후각부에 수평 파열이 관찰됩니다. Grade 3 파열로 관절면까지 연장됨.",
                    "conclusion": "내측 반월판 파열 (Grade 3)"
                }
            },
            "ct": {
                "brain": {
                    "findings": "급성 뇌출혈 소견 없음. 뇌실질 정상.",
                    "abnormalities": [],
                    "conclusion": "정상 소견"
                },
                "abdomen": {
                    "findings": "간, 담낭, 췌장, 비장 정상. 신장 결석 의심 소견.",
                    "abnormalities": ["우측 신장 하극에 3mm 결석 의심"],
                    "conclusion": "우측 신결석 의심, 비뇨기과 상담 권장"
                }
            }
        }

        # 치료 데이터
        self.treatment_data = {
            "요추 추간판 탈출증": {
                "mild": {
                    "treatment_direction": "비수술적 보존 치료",
                    "primary_treatment": """
**약물 치료**
- 소염진통제 (이부프로펜 400mg, 1일 3회, 식후)
- 근이완제 (에페리손 50mg, 1일 3회)

**물리치료**
- 온열치료 + 견인치료 (주 3회, 4주)
- 코어 근력 강화 운동

**생활 관리**
- 급성기 2-3일 안정 후 점진적 활동 증가
- 올바른 자세 유지
""",
                    "alternative_treatment": "도수치료, 침치료 고려 가능",
                    "lifestyle_recommendations": ["장시간 앉는 자세 피하기", "무거운 물건 들지 않기", "수영, 걷기 등 저강도 운동"],
                    "follow_up": "4주 후 재평가, 호전 없으면 주사 치료 고려"
                },
                "moderate": {
                    "treatment_direction": "적극적 보존 치료 + 주사 치료",
                    "primary_treatment": """
**약물 치료**
- 소염진통제 (셀레콕시브 200mg, 1일 1회)
- 신경통 약물 (프레가발린 75mg, 1일 2회)
- 근이완제

**주사 치료**
- 경막외 스테로이드 주사 (1-3회, 2주 간격)
- 신경차단술 고려

**물리치료**
- 집중 재활치료 (주 5회, 6주)
""",
                    "alternative_treatment": "6주 보존 치료 실패 시 수술 고려",
                    "lifestyle_recommendations": ["절대 안정 1주", "보조기 착용", "체중 관리"],
                    "follow_up": "2주마다 재평가, 신경 증상 악화 시 즉시 내원"
                },
                "severe": {
                    "treatment_direction": "수술 치료 권장",
                    "primary_treatment": """
**수술 치료**
- 미세현미경 디스크제거술 권장
- 내시경 디스크제거술 대안

**수술 전 준비**
- 수술 전 검사 (혈액, 심전도, 흉부 X-ray)
- 마취과 상담
""",
                    "alternative_treatment": "수술 거부 시 집중 보존 치료 시도 가능하나 효과 제한적",
                    "lifestyle_recommendations": ["수술 후 6주 허리 보호", "점진적 재활"],
                    "follow_up": "수술 후 2주, 6주, 3개월, 6개월 추적"
                }
            },
            "default": {
                "treatment_direction": "증상에 맞는 대증 치료",
                "primary_treatment": "전문의 상담 후 치료 계획 수립 필요",
                "alternative_treatment": "추가 검사 필요",
                "lifestyle_recommendations": ["충분한 휴식", "수분 섭취"],
                "follow_up": "1-2주 내 재평가"
            }
        }

        # 약물 데이터
        self.medication_data = {
            "요추 추간판 탈출증": {
                "primary": [
                    {
                        "name": "셀레콕시브 (세레브렉스)",
                        "ingredient": "Celecoxib 200mg",
                        "dosage": "1일 1회, 식후 복용",
                        "effect": "염증 및 통증 완화 (COX-2 선택적 억제)",
                        "warning": "위장관 출혈 위험, 심혈관 질환자 주의"
                    },
                    {
                        "name": "프레가발린 (리리카)",
                        "ingredient": "Pregabalin 75mg",
                        "dosage": "1일 2회, 아침/저녁",
                        "effect": "신경통 완화",
                        "warning": "졸음, 어지러움 가능, 운전 주의"
                    }
                ],
                "secondary": [
                    {"name": "에페리손 (뮤렉스)", "effect": "근육 이완"},
                    {"name": "트라마돌 (트리돌)", "effect": "중등도 통증 완화"},
                    {"name": "가바펜틴 (뉴론틴)", "effect": "신경통 대체약"}
                ]
            },
            "default": {
                "primary": [
                    {
                        "name": "아세트아미노펜 (타이레놀)",
                        "ingredient": "Acetaminophen 500mg",
                        "dosage": "1회 1-2정, 1일 3회, 식후",
                        "effect": "해열, 진통",
                        "warning": "간 질환자 주의, 1일 4g 초과 금지"
                    }
                ],
                "secondary": []
            }
        }

        # 수술 데이터
        self.surgery_data = {
            "요추 추간판 탈출증": [
                {
                    "name": "미세현미경 디스크제거술",
                    "method": "현미경 확대 하에 2-3cm 절개로 탈출된 디스크 제거",
                    "pros": "성공률 높음(90-95%), 표준 술식, 보험 적용",
                    "cons": "전신마취 필요, 입원 3-5일",
                    "recovery_time": "4-6주",
                    "success_rate": "90-95%"
                },
                {
                    "name": "내시경 디스크제거술",
                    "method": "8mm 내시경으로 디스크 제거, 최소 침습",
                    "pros": "절개 작음, 회복 빠름, 당일/익일 퇴원 가능",
                    "cons": "기술적 난이도 높음, 일부 경우 적용 제한",
                    "recovery_time": "2-4주",
                    "success_rate": "85-90%"
                },
                {
                    "name": "인공디스크 치환술",
                    "method": "손상된 디스크를 인공 디스크로 교체",
                    "pros": "운동성 보존, 인접 분절 퇴행 예방",
                    "cons": "고비용, 제한적 적응증",
                    "recovery_time": "6-8주",
                    "success_rate": "85-90%"
                }
            ],
            "default": [
                {
                    "name": "수술 옵션 없음",
                    "method": "해당 진단에 대한 수술 정보가 없습니다.",
                    "pros": "-",
                    "cons": "-",
                    "recovery_time": "-",
                    "success_rate": "-"
                }
            ]
        }

    # === 데이터 조회 메서드 ===

    def analyze_symptoms(self, symptoms: str, pain_scale: int = None,
                         duration: str = None, pain_type: str = None) -> dict:
        """증상 분석"""
        # 키워드 기반 매칭
        for keyword, data in self.symptom_analysis.items():
            if keyword in symptoms:
                result = data.copy()
                # 심각도에 따른 red flags 추가
                if pain_scale and pain_scale >= 8:
                    result["red_flags"].append("심한 통증 (8/10 이상)")
                if duration and ("개월" in duration or "년" in duration):
                    result["red_flags"].append("만성 통증")
                return result

        return self.symptom_analysis["default"]

    def get_patient_history(self, patient_id: str) -> dict:
        """환자 병력 조회"""
        return self.patients.get(patient_id, self.patients["default"])

    def analyze_xray(self, body_part: str) -> dict:
        """X-ray 분석"""
        xray_data = self.imaging_data["xray"]
        return xray_data.get(body_part, {
            "findings": "해당 부위 분석 데이터 없음",
            "abnormalities": [],
            "normal_findings": [],
            "recommendation": "전문의 상담 필요"
        })

    def analyze_mri(self, body_part: str) -> dict:
        """MRI 분석"""
        mri_data = self.imaging_data["mri"]
        return mri_data.get(body_part, {
            "findings": "해당 부위 분석 데이터 없음",
            "abnormalities": [],
            "detailed_analysis": "",
            "conclusion": "전문의 상담 필요"
        })

    def analyze_ct(self, body_part: str) -> dict:
        """CT 분석"""
        ct_data = self.imaging_data["ct"]
        return ct_data.get(body_part, {
            "findings": "해당 부위 분석 데이터 없음",
            "abnormalities": [],
            "conclusion": "전문의 상담 필요"
        })

    def assess_severity(self, diagnosis: str, symptoms_summary: str = None,
                        imaging_summary: str = None) -> dict:
        """심각도 평가"""
        # 키워드 기반 심각도 판단 (실제로는 더 복잡한 로직 필요)
        severity = "moderate"  # 기본값
        urgency = "준응급"

        if imaging_summary:
            if "탈출" in imaging_summary or "파열" in imaging_summary:
                severity = "moderate"
                urgency = "준응급 - 1-2주 내 치료 권장"
            if "신경 압박" in imaging_summary or "마비" in imaging_summary:
                severity = "severe"
                urgency = "응급 - 즉시 전문의 상담"

        if symptoms_summary:
            if "심한" in symptoms_summary or "극심" in symptoms_summary:
                severity = "severe" if severity == "moderate" else severity

        return {
            "severity": severity,
            "urgency": urgency,
            "rationale": f"{diagnosis}에 대한 증상 및 영상 소견을 종합한 결과입니다.",
            "key_findings": [
                imaging_summary or "영상 소견 없음",
                symptoms_summary or "증상 요약 없음"
            ],
            "recommendation": "전문의 상담을 통한 치료 계획 수립을 권장합니다."
        }

    def check_risk_factors(self, age: int = None, conditions: list = None) -> dict:
        """위험 요소 체크"""
        risks = []
        precautions = []

        if age and age >= 65:
            risks.append("고령 (65세 이상)")
            precautions.append("수술 시 마취 위험도 평가 필요")

        if conditions:
            if "당뇨" in str(conditions):
                risks.append("당뇨병")
                precautions.append("상처 회복 지연 가능성")
            if "고혈압" in str(conditions):
                risks.append("고혈압")
                precautions.append("수술 중 혈압 모니터링 필요")

        overall = "높음" if len(risks) >= 2 else ("중간" if risks else "낮음")

        return {
            "overall_risk": overall,
            "identified_risks": risks if risks else ["특이 위험 요소 없음"],
            "precautions": precautions if precautions else ["일반적 주의사항 준수"],
            "recommendation": "위험 요소를 고려한 치료 계획 수립 필요" if risks else "표준 치료 프로토콜 적용 가능"
        }

    def recommend_treatment(self, diagnosis: str, severity: str,
                            patient_age: int = None, contraindications: list = None) -> dict:
        """치료 추천"""
        # 진단명으로 치료 데이터 조회
        treatment = self.treatment_data.get(diagnosis, self.treatment_data["default"])

        if isinstance(treatment, dict) and severity not in treatment:
            return treatment  # default case

        return treatment.get(severity, treatment.get("mild", self.treatment_data["default"]))

    def get_medication_options(self, diagnosis: str, allergies: list = None) -> dict:
        """약물 옵션 조회"""
        meds = self.medication_data.get(diagnosis, self.medication_data["default"])

        # 알레르기 필터링 (간단한 구현)
        if allergies:
            filtered_primary = [m for m in meds["primary"]
                                if not any(a.lower() in m["name"].lower() for a in allergies)]
            meds = {"primary": filtered_primary, "secondary": meds["secondary"]}

        return meds

    def get_surgery_options(self, diagnosis: str) -> list:
        """수술 옵션 조회"""
        return self.surgery_data.get(diagnosis, self.surgery_data["default"])
