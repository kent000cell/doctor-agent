---
name: imaging-analysis
description: Analyze medical imaging such as X-ray, CT, MRI. Detect abnormalities like fractures, disc issues, tumors.
license: Apache-2.0
metadata:
  author: doctor-agent
  version: "1.0"
  category: diagnosis
allowed-tools: analyze_xray, analyze_mri, analyze_ct
---

# Medical Imaging Analysis Skill

## Overview
Analyze X-ray, CT, MRI and other medical images to detect abnormalities and assist in diagnosis.

## When to Use
- When patient provides X-ray, CT, or MRI images
- When image-based diagnosis is required
- To check for structural abnormalities like fractures, disc issues, tumors

## Available Tools
| Tool | Description |
|------|-------------|
| `analyze_xray` | X-ray analysis - fractures, joints, lungs |
| `analyze_mri` | MRI analysis - soft tissues, discs, brain |
| `analyze_ct` | CT analysis - abdomen, chest, brain hemorrhage |

## Workflow
1. Identify imaging type (X-ray/CT/MRI)
2. Determine scan location
3. Call appropriate analysis tool
4. Generate abnormality report

## Application by Imaging Type

### X-ray
| Region | Key Assessments |
|--------|-----------------|
| Spine | Disc spacing, osteophytes, alignment |
| Chest | Pneumonia, tumors, cardiomegaly |
| Joints | Fractures, arthritis, dislocation |
| Extremities | Fractures, bone density |

### MRI
| Region | Key Assessments |
|--------|-----------------|
| Spine | Disc herniation, nerve compression |
| Brain | Tumors, infarction, hemorrhage |
| Joints | Ligament, cartilage damage |

### CT
| Region | Key Assessments |
|--------|-----------------|
| Brain | Hemorrhage, infarction, tumors |
| Abdomen | Organ abnormalities, stones |
| Chest | Pulmonary embolism, aorta |

## Response Format
- Imaging type and scan location
- Normal/abnormal findings differentiation
- Detailed explanation of abnormalities
- Additional testing recommendations (if needed)
