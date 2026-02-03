"""AI Doctor Agent - Tool Registry

도구 실행 관리자. 각 도구의 실제 구현을 담당.
"""

import json
from typing import Any
from pathlib import Path


class ToolRegistry:
    """도구 레지스트리 - 도구 실행 관리"""

    def __init__(self, data_source, skill_loader):
        self.data_source = data_source
        self.skill_loader = skill_loader

        # 도구 매핑
        self._tools = {
            "analyze_symptoms": self._analyze_symptoms,
            "get_patient_history": self._get_patient_history,
            "analyze_xray": self._analyze_xray,
            "analyze_mri": self._analyze_mri,
            "analyze_ct": self._analyze_ct,
            "assess_severity": self._assess_severity,
            "check_risk_factors": self._check_risk_factors,
            "recommend_treatment": self._recommend_treatment,
            "get_medication_options": self._get_medication_options,
            "get_surgery_options": self._get_surgery_options,
            "read_skill": self._read_skill,
        }

    def execute(self, tool_name: str, args: dict) -> str:
        """도구 실행"""
        if tool_name not in self._tools:
            return json.dumps({"error": f"알 수 없는 도구: {tool_name}"}, ensure_ascii=False)

        try:
            result = self._tools[tool_name](**args)
            return result
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)

    # === 증상 분석 ===
    def _analyze_symptoms(self, symptoms: str, pain_scale: int = None,
                          duration: str = None, pain_type: str = None) -> str:
        """증상 분석"""
        analysis = self.data_source.analyze_symptoms(symptoms, pain_scale, duration, pain_type)

        result = f"""## 증상 분석 결과

**주요 증상**: {symptoms}
**통증 강도**: {pain_scale or '미입력'}/10
**지속 기간**: {duration or '미입력'}
**통증 유형**: {self._translate_pain_type(pain_type)}

### 분석 결과
{analysis['analysis']}

### 연관 증상
{', '.join(analysis['related_symptoms'])}

### 위험 신호 (Red Flags)
{self._format_red_flags(analysis['red_flags'])}

### 예상 진단
{', '.join(analysis['possible_diagnoses'])}
"""
        return result

    def _translate_pain_type(self, pain_type: str) -> str:
        """통증 유형 번역"""
        translations = {
            "dull": "둔통 (묵직함)",
            "sharp": "찌르는 통증",
            "radiating": "방사통 (퍼지는 통증)",
            "throbbing": "박동성 통증",
            "burning": "화끈거리는 통증"
        }
        return translations.get(pain_type, "미입력")

    def _format_red_flags(self, red_flags: list) -> str:
        """위험 신호 포맷"""
        if not red_flags:
            return "- 없음"
        return '\n'.join([f"⚠️ {flag}" for flag in red_flags])

    # === 환자 병력 ===
    def _get_patient_history(self, patient_id: str) -> str:
        """환자 병력 조회"""
        history = self.data_source.get_patient_history(patient_id)

        result = f"""## 환자 병력 조회

**환자 ID**: {patient_id}
**나이**: {history['age']}세
**성별**: {history['gender']}

### 과거 병력
{self._format_list(history['medical_history'])}

### 수술 이력
{self._format_list(history['surgeries'])}

### 알레르기
{self._format_list(history['allergies'])}

### 현재 복용 약물
{self._format_list(history['current_medications'])}
"""
        return result

    def _format_list(self, items: list) -> str:
        """리스트 포맷"""
        if not items:
            return "- 없음"
        return '\n'.join([f"- {item}" for item in items])

    # === 영상 분석 ===
    def _analyze_xray(self, body_part: str, image_data: str = None) -> str:
        """X-ray 분석"""
        analysis = self.data_source.analyze_xray(body_part)

        result = f"""## X-ray 분석 결과

**촬영 부위**: {self._translate_body_part(body_part)}
**영상 품질**: 양호

### 분석 소견
{analysis['findings']}

### 이상 소견
{self._format_list(analysis['abnormalities'])}

### 정상 소견
{self._format_list(analysis['normal_findings'])}

### 추가 검사 권고
{analysis['recommendation']}
"""
        return result

    def _analyze_mri(self, body_part: str, image_data: str = None) -> str:
        """MRI 분석"""
        analysis = self.data_source.analyze_mri(body_part)

        result = f"""## MRI 분석 결과

**촬영 부위**: {self._translate_body_part(body_part)}
**영상 품질**: 양호

### 분석 소견
{analysis['findings']}

### 이상 소견
{self._format_list(analysis['abnormalities'])}

### 상세 분석
{analysis['detailed_analysis']}

### 결론
{analysis['conclusion']}
"""
        return result

    def _analyze_ct(self, body_part: str, image_data: str = None) -> str:
        """CT 분석"""
        analysis = self.data_source.analyze_ct(body_part)

        result = f"""## CT 분석 결과

**촬영 부위**: {self._translate_body_part(body_part)}
**영상 품질**: 양호

### 분석 소견
{analysis['findings']}

### 이상 소견
{self._format_list(analysis['abnormalities'])}

### 결론
{analysis['conclusion']}
"""
        return result

    def _translate_body_part(self, body_part: str) -> str:
        """부위명 번역"""
        translations = {
            "spine": "척추",
            "chest": "흉부",
            "knee": "무릎",
            "shoulder": "어깨",
            "hip": "고관절",
            "ankle": "발목",
            "wrist": "손목",
            "pelvis": "골반",
            "brain": "뇌",
            "abdomen": "복부"
        }
        return translations.get(body_part, body_part)

    # === 심각도 평가 ===
    def _assess_severity(self, diagnosis: str, symptoms_summary: str = None,
                         imaging_summary: str = None) -> str:
        """심각도 평가"""
        assessment = self.data_source.assess_severity(diagnosis, symptoms_summary, imaging_summary)

        severity_emoji = {"mild": "🟢", "moderate": "🟡", "severe": "🔴"}
        severity_kr = {"mild": "경증", "moderate": "중등증", "severe": "중증"}

        result = f"""## 심각도 평가 결과

**진단명**: {diagnosis}
**심각도**: {severity_emoji[assessment['severity']]} {severity_kr[assessment['severity']]}
**긴급도**: {assessment['urgency']}

### 평가 근거
{assessment['rationale']}

### 주요 소견
{self._format_list(assessment['key_findings'])}

### 권고사항
{assessment['recommendation']}
"""
        return result

    # === 위험 요소 체크 ===
    def _check_risk_factors(self, patient_id: str = None, age: int = None,
                            conditions: list = None) -> str:
        """위험 요소 체크"""
        risk = self.data_source.check_risk_factors(age, conditions or [])

        result = f"""## 위험 요소 평가

**전체 위험도**: {risk['overall_risk']}

### 확인된 위험 요소
{self._format_list(risk['identified_risks'])}

### 주의사항
{self._format_list(risk['precautions'])}

### 권고사항
{risk['recommendation']}
"""
        return result

    # === 치료 추천 ===
    def _recommend_treatment(self, diagnosis: str, severity: str,
                             patient_age: int = None, contraindications: list = None) -> str:
        """치료 추천"""
        treatment = self.data_source.recommend_treatment(
            diagnosis, severity, patient_age, contraindications or []
        )

        result = f"""## 치료 추천

**진단명**: {diagnosis}
**심각도**: {severity}
**치료 방향**: {treatment['treatment_direction']}

### 1차 권장 치료
{treatment['primary_treatment']}

### 대안 치료
{treatment['alternative_treatment']}

### 생활습관 권고
{self._format_list(treatment['lifestyle_recommendations'])}

### 추적 관찰
{treatment['follow_up']}

---
⚠️ **주의**: 본 내용은 AI 보조 진단입니다. 최종 치료 결정은 반드시 전문의와 상담하세요.
"""
        return result

    # === Medication Options (RxNorm API) ===
    def _get_medication_options(self, diagnosis: str, allergies: list = None) -> str:
        """Get medication options using RxNorm API"""
        from backend.services.rxnorm_api import rxnorm_client
        from backend.logger import get_logger

        logger = get_logger("tools.medication")
        allergies = allergies or []

        # Map diagnosis to common drug queries
        drug_queries = self._get_drug_queries_for_diagnosis(diagnosis)

        if not drug_queries:
            logger.warning(f"No drug queries found for diagnosis: {diagnosis}")
            # Fallback to mock data
            medications = self.data_source.get_medication_options(diagnosis, allergies)
            return self._format_mock_medications(diagnosis, medications)

        result = f"""## Medication Treatment Options (via RxNorm API)

**Diagnosis**: {diagnosis}

### Primary Medications (FDA-approved)
"""

        found_any = False
        for query in drug_queries[:3]:  # Top 3 drug types
            logger.info(f"Searching RxNorm for: {query}")
            drugs = rxnorm_client.search_drugs(query)

            if drugs:
                found_any = True
                for drug in drugs[:2]:  # Top 2 per category
                    drug_name = drug.get('name', 'Unknown')
                    rxcui = drug.get('rxcui', 'N/A')

                    # Check for allergies
                    if any(allergy.lower() in drug_name.lower() for allergy in allergies):
                        continue

                    # Get drug details
                    drug_info = rxnorm_client.get_drug_info(rxcui)

                    result += f"""
**{drug_name}**
- RxCUI: {rxcui}
- Type: {drug_info.get('tty', 'N/A') if drug_info else 'N/A'}
- Note: Consult healthcare provider for dosage and usage
"""

                    # Get interactions if available
                    interactions = rxnorm_client.get_drug_interactions(rxcui)
                    if interactions:
                        result += f"- ⚠️ Known interactions: {len(interactions)} found\n"

        if not found_any:
            logger.warning(f"No drugs found via RxNorm API, using fallback")
            # Fallback to mock data
            medications = self.data_source.get_medication_options(diagnosis, allergies)
            return self._format_mock_medications(diagnosis, medications)

        result += """

---
⚠️ **Disclaimer**: This information is from the FDA RxNorm database. Always consult with a healthcare professional before taking any medication.
"""

        return result

    def _get_drug_queries_for_diagnosis(self, diagnosis: str) -> list:
        """Map diagnosis to drug search queries"""
        diagnosis_lower = diagnosis.lower()

        # Common diagnosis to drug mapping
        drug_map = {
            "disc herniation": ["ibuprofen", "naproxen", "celecoxib"],
            "herniated disc": ["ibuprofen", "naproxen", "celecoxib"],
            "back pain": ["ibuprofen", "acetaminophen", "naproxen"],
            "arthritis": ["ibuprofen", "naproxen", "celecoxib"],
            "headache": ["acetaminophen", "ibuprofen", "aspirin"],
            "migraine": ["sumatriptan", "ibuprofen", "acetaminophen"],
            "knee pain": ["ibuprofen", "naproxen", "acetaminophen"],
        }

        for key, drugs in drug_map.items():
            if key in diagnosis_lower:
                return drugs

        # Default pain medications
        return ["ibuprofen", "acetaminophen"]

    def _format_mock_medications(self, diagnosis: str, medications: dict) -> str:
        """Format mock medication data (fallback)"""
        result = f"""## Medication Treatment Options (Fallback Data)

**Diagnosis**: {diagnosis}

### Primary Medications
"""
        for med in medications['primary']:
            result += f"""
**{med['name']}**
- Ingredient: {med['ingredient']}
- Dosage: {med['dosage']}
- Effect: {med['effect']}
- Warning: {med['warning']}
"""

        result += "\n### Secondary Medications\n"
        for med in medications['secondary']:
            result += f"- {med['name']}: {med['effect']}\n"

        result += "\n⚠️ **Note**: This is demo data. Real data unavailable.\n"

        return result

    # === 수술 옵션 ===
    def _get_surgery_options(self, diagnosis: str, severity: str = None) -> str:
        """수술 옵션 조회"""
        surgeries = self.data_source.get_surgery_options(diagnosis)

        result = f"""## 수술 치료 옵션

**진단명**: {diagnosis}

"""
        for surgery in surgeries:
            result += f"""### {surgery['name']}
- **방법**: {surgery['method']}
- **장점**: {surgery['pros']}
- **단점**: {surgery['cons']}
- **회복기간**: {surgery['recovery_time']}
- **성공률**: {surgery['success_rate']}

"""

        result += "---\n⚠️ 수술 결정은 반드시 전문의와 충분한 상담 후 결정하세요."
        return result

    # === 스킬 읽기 ===
    def _read_skill(self, skill_name: str) -> str:
        """스킬 문서 읽기"""
        content = self.skill_loader.get_skill_content(skill_name)
        if content:
            return content
        return f"스킬을 찾을 수 없습니다: {skill_name}"
