# Local Windows Setup

## Prerequisites

- Windows 10/11
- Python 3.11+
- Node.js 24+
- Git
- VS Code

Docker is not required for the local demo.

## 1. Clone

```powershell
git clone https://github.com/varunpothu/clinicflow-ai.git
cd clinicflow-ai
```

## 2. Backend

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
cd ..
```

Create a local environment file by copying .env.example to .env.

## 3. Start FastAPI

```powershell
cd backend
uvicorn app.main:app --reload
```

Open the interactive API documentation at the local FastAPI docs route.

## 4. Frontend

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

The frontend will call the backend using VITE_API_BASE_URL when configured. During development the default points to localhost.

## 5. Run tests

Backend:

```powershell
cd backend
pytest -q
ruff check . --select E4,E7,E9,F
mypy app
```

Frontend:

```powershell
cd frontend
npm run build
```

## 6. Run the patient demo

Open the Staff Console and select Patient demo. Submit a natural-language request. The backend returns the extracted intent and current workflow state.

## 7. Optional AWS mode

Set:

- AI_PROVIDER=bedrock
- AWS_REGION=eu-west-2
- BEDROCK_MODEL_ID=<approved model identifier>

For Guardrails, also set the Bedrock guardrail identifier/version.

The local mock provider remains the default so AWS access is never required for normal development.
