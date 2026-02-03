# AI Doctor Agent

> Agent Skills-Based Medical AI Consultation System - Production-Ready Prototype

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

## Overview

AI Doctor Agent is a medical AI consultation system built following **Agent Skills specification**. It analyzes patient symptoms, interprets medical images, and recommends appropriate treatments using AI technology.

**Key Features:**
- 🏥 **Multimodal Diagnosis**: Text symptoms + Image analysis (GPT-4o Vision)
- 🔧 **Agent Skills Compliant**: Progressive Disclosure pattern implementation
- ⚡ **Real-time Streaming**: Live diagnostic process via SSE
- 🛠️ **10 Medical Tools**: Systematic diagnosis via Function Calling
- 📚 **4 Specialized Skills**: Symptom analysis, imaging, assessment, treatment
- 💊 **RxNorm API Integration**: Real FDA-approved drug information from US National Library of Medicine

⚠️ **Disclaimer**: This system is an AI-assisted diagnostic demo and does not replace actual medical diagnosis.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Frontend (Web UI)                     │
│                  Vanilla JS + SSE Streaming                 │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/SSE
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Routes    │  │ Skill Loader │  │ Tool Registry│      │
│  │  /api/chat  │─▶│  Discovery   │─▶│  10 Tools    │      │
│  │ /api/skills │  │  Activation  │  │  Execution   │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────┬─────────────────────────────────────┘
                        │ OpenAI API
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    OpenAI GPT-4o                            │
│              Function Calling + Vision                      │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Agent Skills (4 modules)                  │
│  symptom-analysis │ imaging-analysis │ disease-assessment  │
│                   treatment-recommendation                  │
└─────────────────────────────────────────────────────────────┘
```

### Agent Skills Workflow

```
1. Discovery Phase
   └─ Inject skill metadata XML into system prompt

2. Activation Phase
   └─ LLM loads full skill content via read_skill tool

3. Execution Phase
   └─ LLM executes 10 medical tools following skill guidelines
      ├─ analyze_symptoms (symptom analysis)
      ├─ analyze_xray/mri/ct (imaging analysis)
      ├─ assess_severity (severity assessment)
      └─ recommend_treatment (treatment recommendation)
```

---

## Tech Stack

### Backend
- **Framework**: FastAPI 0.100+
- **LLM**: OpenAI GPT-4o (Function Calling + Vision)
- **Streaming**: Server-Sent Events (SSE)
- **Medical Data**: RxNorm API (FDA drug database) + Mock Data Source

### Frontend
- **UI**: Vanilla JavaScript + HTML5
- **Styling**: Pure CSS (Gradient Design)
- **Communication**: Fetch API + EventSource (SSE)

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Testing**: pytest + coverage
- **Logging**: Python logging module

---

## Quick Start

### Prerequisites
- Python 3.10 or higher
- OpenAI API Key
- (Optional) Docker & Docker Compose

### Local Setup

```bash
# 1. Clone repository
git clone https://github.com/kent000cell/doctor-agent.git
cd doctor-agent

# 2. Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# 3. Run entire system (auto-creates venv + installs deps + starts servers)
python run.py
```

Browser automatically opens at `http://localhost:3000`

### Docker Setup

```bash
# Run with Docker Compose
docker-compose up -d

# Access
open http://localhost:3000
```

---

## Project Structure

```
doctor-agent/
├── backend/                 # FastAPI backend
│   ├── main.py             # API server (SSE streaming)
│   ├── config.py           # Configuration management
│   ├── skill_loader.py     # Agent Skills loader
│   └── tools/
│       ├── definitions.py  # OpenAI Function definitions
│       └── registry.py     # Tool execution engine
├── frontend/               # Frontend
│   └── index.html          # Chat UI (Vanilla JS)
├── skills/                 # Agent Skills (4 modules)
│   ├── symptom-analysis/
│   ├── imaging-analysis/
│   ├── disease-assessment/
│   └── treatment-recommendation/
├── data/                   # Mock data
│   └── mock_data.py
├── tests/                  # Test suite
│   ├── test_api.py
│   ├── test_skills.py
│   └── test_tools.py
├── prompts/                # System prompts
│   └── system.md
├── run.py                  # One-click launcher
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Key Features

### 1. Symptom Analysis
- Pain location, intensity (1-10), duration tracking
- Pain type classification (dull/sharp/radiating/throbbing/burning)
- Red flag detection (emergency situations)

### 2. Medical Imaging Analysis
- **X-ray**: Fractures, disc spacing, arthritis
- **MRI**: Disc herniation, ligament damage, nerve compression
- **CT**: Brain hemorrhage, abdominal organs, pulmonary embolism

### 3. Disease Assessment
- Severity classification: Mild / Moderate / Severe
- Urgency determination: Emergency / Urgent / Non-urgent
- Risk factor evaluation (age, underlying conditions)

### 4. Treatment Recommendations
- Medication options via **RxNorm API** (real FDA-approved drugs with RxCUI codes)
- Drug interaction checking and allergy filtering
- Surgical options (methods, pros/cons, recovery time)
- Lifestyle recommendations

---

## RxNorm API Integration

The system integrates with the **RxNorm API** from the U.S. National Library of Medicine to provide real FDA-approved drug information.

**Features:**
- ✅ Drug search by name (returns RxCUI codes)
- ✅ Detailed drug information (type, synonyms, properties)
- ✅ Drug interaction checking
- ✅ Allergy filtering
- ✅ Graceful fallback to mock data if API unavailable

**Example:**
```python
# Search for ibuprofen
drugs = rxnorm_client.search_drugs("ibuprofen")
# Returns: [
#   {"rxcui": "1100070", "name": "ibuprofen 800 MG Oral Tablet", "tty": "SBD"},
#   ...
# ]
```

**API Documentation:** https://lhncbc.nlm.nih.gov/RxNav/APIs/

---

## API Endpoints

### `POST /api/chat`
Send chat message (SSE streaming response)

**Request:**
```json
{
  "message": "I have back pain and leg numbness",
  "patient_id": "P001",
  "image": "data:image/jpeg;base64,..." // optional
}
```

**Response:** (SSE Stream)
```json
{"type": "log", "data": {"step": "discovery", "message": "..."}}
{"type": "log", "data": {"step": "activation", "message": "..."}}
{"type": "log", "data": {"step": "tool_call", "message": "..."}}
{"type": "response", "data": {"content": "Diagnosis result..."}}
```

### `GET /api/skills`
Get available skills list

### `GET /api/health`
Health check endpoint

---

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=backend --cov-report=html

# Specific test
pytest tests/test_api.py -v
```

---

## Environment Variables

```bash
# Required
OPENAI_API_KEY=your-api-key-here

# Optional (defaults available)
OPENAI_MODEL=gpt-4o          # Model to use
HOST=0.0.0.0                  # Server host
PORT=8000                     # Server port
```

---

## Development Roadmap

- [x] Agent Skills specification implementation
- [x] Multimodal support (text + image)
- [x] SSE streaming
- [x] Docker containerization
- [x] Test suite
- [x] Real medical data API integration (RxNorm for medications)
- [ ] PostgreSQL integration (conversation history)
- [ ] User authentication (JWT)
- [ ] Additional medical APIs (imaging, labs)
- [ ] RAG-based medical knowledge base

---

## License

Apache License 2.0

---

## Disclaimer

⚠️ **This system is a prototype for educational and research purposes.**

- Does not replace actual medical diagnosis
- For emergencies, call 911 or visit nearest emergency room immediately
- All medical decisions must be made in consultation with healthcare professionals
- Uses mock data, not actual patient data

---

## Contributing

Contributions are welcome! Feel free to submit issues or PRs.

---

## Contact

Project inquiries: [your.email@example.com](mailto:your.email@example.com)
