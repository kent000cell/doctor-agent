---
name: treatment-recommendation
description: 수술/비수술 판단, 약물 치료, 물리치료 등 치료법 추천. 치료 옵션 비교.
license: Apache-2.0
metadata:
  author: doctor-agent
  version: "1.0"
  category: treatment
allowed-tools: recommend_treatment, get_medication_options, get_surgery_options
---

# 치료 추천 스킬

## 개요
진단 결과와 심각도 평가를 바탕으로 최적의 치료법을 추천합니다.

## 사용 시점
- 진단 및 심각도 평가 완료 후
- 치료 방향 결정이 필요할 때
- 환자에게 치료 옵션 설명 시

## 사용 도구
| 도구 | 설명 |
|------|------|
| `recommend_treatment` | 종합 치료법 추천 |
| `get_medication_options` | 약물 치료 옵션 조회 |
| `get_surgery_options` | 수술 옵션 조회 |

## 작업 흐름
1. 진단명 + 심각도 확인
2. `recommend_treatment`로 치료 방향 결정
3. 필요시 `get_medication_options` 또는 `get_surgery_options` 호출
4. 치료 옵션 비교 및 추천

## 치료 결정 기준

### 비수술 치료 우선
| 심각도 | 치료법 |
|--------|--------|
| 경증 | 약물치료 + 생활습관 개선 |
| 중등증 | 약물치료 + 물리치료 + 주사치료 |

### 수술 치료 고려
| 조건 | 수술 고려 |
|------|----------|
| 보존적 치료 6주 이상 실패 | O |
| 신경 손상 진행 | O |
| 마비 증상 | O (긴급) |
| 통증 조절 불가 | O |

## 치료 옵션 분류

### 약물 치료
- 소염진통제 (NSAIDs)
- 근이완제
- 신경통 약물
- 스테로이드

### 비약물 치료
- 물리치료
- 도수치료
- 운동치료
- 침/한방치료

### 주사 치료
- 경막외 스테로이드 주사
- 신경차단술
- 프롤로치료

### 수술 치료
- 최소침습 수술
- 내시경 수술
- 개방성 수술

## 응답 형식
- 추천 치료 방향 (수술/비수술)
- 1차 치료 옵션 (상세)
- 2차 치료 옵션 (대안)
- 예상 치료 기간
- 주의사항 및 금기사항

## 필수 안내 문구
⚠️ 본 내용은 AI 보조 진단으로, 최종 치료 결정은 반드시 전문의와 상담하세요.
