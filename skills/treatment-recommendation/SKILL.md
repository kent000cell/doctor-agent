---
name: treatment-recommendation
description: Determine surgical/non-surgical approach, recommend medication, physical therapy. Compare treatment options.
license: Apache-2.0
metadata:
  author: doctor-agent
  version: "1.0"
  category: treatment
allowed-tools: recommend_treatment, get_medication_options, get_surgery_options
---

# Treatment Recommendation Skill

## Overview
Recommend optimal treatment based on diagnosis results and severity assessment.

## When to Use
- After completing diagnosis and severity assessment
- When treatment direction needs to be decided
- When explaining treatment options to patient

## Available Tools
| Tool | Description |
|------|-------------|
| `recommend_treatment` | Comprehensive treatment recommendation |
| `get_medication_options` | Retrieve medication treatment options |
| `get_surgery_options` | Retrieve surgical options |

## Workflow
1. Confirm diagnosis + severity
2. Decide treatment direction with `recommend_treatment`
3. Call `get_medication_options` or `get_surgery_options` if needed
4. Compare and recommend treatment options

## Treatment Decision Criteria

### Non-Surgical Treatment Priority
| Severity | Treatment |
|----------|-----------|
| Mild | Medication + lifestyle modification |
| Moderate | Medication + physical therapy + injections |

### Surgical Treatment Consideration
| Condition | Surgery Considered |
|-----------|-------------------|
| Conservative treatment failure (6+ weeks) | Yes |
| Progressive nerve damage | Yes |
| Paralysis symptoms | Yes (urgent) |
| Uncontrollable pain | Yes |

## Treatment Option Categories

### Medication Treatment
- Anti-inflammatory drugs (NSAIDs)
- Muscle relaxants
- Neuropathic pain medications
- Steroids

### Non-Medication Treatment
- Physical therapy
- Manual therapy
- Exercise therapy
- Acupuncture

### Injection Treatment
- Epidural steroid injection
- Nerve block
- Prolotherapy

### Surgical Treatment
- Minimally invasive surgery
- Endoscopic surgery
- Open surgery

## Response Format
- Recommended treatment direction (surgical/non-surgical)
- Primary treatment option (detailed)
- Secondary treatment option (alternative)
- Expected treatment duration
- Precautions and contraindications

## Required Disclaimer
⚠️ This is AI-assisted diagnosis. Final treatment decisions must be made in consultation with a healthcare professional.
