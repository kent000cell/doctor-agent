---
name: disease-assessment
description: Assess disease progression stage. Determine mild/moderate/severe, classify urgency, check risk factors.
license: Apache-2.0
metadata:
  author: doctor-agent
  version: "1.0"
  category: diagnosis
allowed-tools: assess_severity, check_risk_factors
---

# Disease Assessment Skill

## Overview
Integrate symptom and imaging analysis results to assess disease severity and progression stage.

## When to Use
- After completing symptom and imaging analysis
- When disease progression needs to be determined
- Before deciding treatment direction for severity assessment

## Available Tools
| Tool | Description |
|------|-------------|
| `assess_severity` | Assess disease severity (mild/moderate/severe) |
| `check_risk_factors` | Check risk factors (age, underlying conditions) |

## Workflow
1. Collect symptom analysis + imaging analysis results
2. Determine severity using `assess_severity`
3. Check risk factors with `check_risk_factors`
4. Generate comprehensive assessment report

## Severity Classification Criteria

### Mild
- Daily activities possible
- Improves with medication
- No urgent treatment needed

### Moderate
- Daily activities affected
- Active treatment required
- Consultation with specialist recommended

### Severe
- Daily activities impossible
- Immediate treatment required
- Surgery or hospitalization considered

## Risk Factors Checklist
- [ ] Elderly (65+)
- [ ] Diabetes
- [ ] Hypertension
- [ ] Cardiovascular disease
- [ ] Immunocompromised
- [ ] Smoking
- [ ] Obesity

## Response Format
- Suspected diagnosis
- Severity grade
- List of risk factors
- Urgency classification (emergency/urgent/non-urgent)
