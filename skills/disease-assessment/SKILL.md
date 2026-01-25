---
name: disease-assessment
description: 질병 진행 단계 평가. 경증/중등증/중증 판단, 긴급도 분류, 위험 요소 체크.
license: Apache-2.0
metadata:
  author: doctor-agent
  version: "1.0"
  category: diagnosis
allowed-tools: assess_severity, check_risk_factors
---

# 질병 평가 스킬

## 개요
증상 분석과 영상 분석 결과를 종합하여 질병의 심각도와 진행 단계를 평가합니다.

## 사용 시점
- 증상 분석 + 영상 분석 완료 후
- 질병 진행 단계 파악이 필요할 때
- 치료 방향 결정 전 심각도 평가 시

## 사용 도구
| 도구 | 설명 |
|------|------|
| `assess_severity` | 질병 심각도 평가 (경증/중등증/중증) |
| `check_risk_factors` | 위험 요소 체크 (나이, 기저질환 등) |

## 작업 흐름
1. 증상 분석 결과 + 영상 분석 결과 수집
2. `assess_severity`로 심각도 판단
3. `check_risk_factors`로 위험 요소 확인
4. 종합 평가 리포트 생성

## 심각도 분류 기준

### 경증 (Mild)
- 일상생활 가능
- 약물치료로 호전 가능
- 긴급 치료 불필요

### 중등증 (Moderate)
- 일상생활 지장
- 적극적 치료 필요
- 전문의 상담 권장

### 중증 (Severe)
- 일상생활 불가
- 즉각적 치료 필요
- 수술 또는 입원 고려

## 위험 요소 체크리스트
- [ ] 고령 (65세 이상)
- [ ] 당뇨병
- [ ] 고혈압
- [ ] 심혈관 질환
- [ ] 면역 저하
- [ ] 흡연
- [ ] 비만

## 응답 형식
- 예상 진단명
- 심각도 등급
- 위험 요소 목록
- 긴급도 분류 (응급/준응급/비응급)
