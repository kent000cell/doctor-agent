---
name: symptom-analysis
description: Analyze patient pain, discomfort, and symptoms. Identify pain location, intensity, duration, and characteristics.
license: Apache-2.0
metadata:
  author: doctor-agent
  version: "1.0"
  category: diagnosis
allowed-tools: analyze_symptoms, get_patient_history
---

# Symptom Analysis Skill

## Overview
Systematically analyze patient symptoms to gather diagnostic information.

## When to Use
- When patient describes pain/discomfort
- For requests like "My back hurts", "I have a headache", "My knee aches"
- When initial symptom assessment is needed

## Available Tools
| Tool | Description |
|------|-------------|
| `analyze_symptoms` | Symptom analysis - identify location, intensity, characteristics |
| `get_patient_history` | Retrieve patient medical history |

## Workflow
1. Extract key information from patient symptom text
2. Classify and analyze symptoms using `analyze_symptoms`
3. Check medical history with `get_patient_history` if needed
4. Identify related symptoms and red flags

## Symptom Classification

### Pain Intensity (Pain Scale)
| Score | Description |
|-------|-------------|
| 1-3 | Mild - Daily activities possible |
| 4-6 | Moderate - Daily activities affected |
| 7-10 | Severe - Immediate treatment needed |

### Pain Characteristics
- **Dull pain**: Heavy, persistent pain
- **Sharp pain**: Acute, localized pain
- **Radiating pain**: Pain spreading to other areas
- **Throbbing pain**: Pulsating pain

## Response Format
- Summary of main symptoms
- Pain location and intensity
- List of associated symptoms
- Red flag presence
