# LaTech

## Architecture (FastAPI)

### Project Structure

```
app/
  main.py              # FastAPI app (API only)
frontend/              # SvelteKit + Tailwind frontend (multipage)
requirements.txt       # Python dependencies
Procfile               # honcho process definitions (backend + frontend)
```

### Prerequisites

- Python 3.9+
- Recommended: a virtual environment (e.g., `python -m venv .venv`)

### Setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run (API development)

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` in your browser.

### Run both (honcho + Procfile)

Assumes your conda environment is already activated.

```bash
# Install Python deps (includes honcho)
pip install -r requirements.txt

# Start backend and frontend together
honcho start
```

This uses `Procfile` to run:

```
backend: uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
frontend: cd frontend && npm install && npm run dev
```

## Frontend (SvelteKit + Tailwind)

A multipage UI is available under `frontend/` using SvelteKit with Tailwind CSS. It proxies `/api/*` to the FastAPI backend during development.

### Prerequisites

- Node.js 18+
- npm 9+

### Setup & Run (frontend-only)

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`. Ensure the backend is running (see "Run (development)" above).

### Environment

- `PUBLIC_API_BASE` (optional): override API base URL. Example `frontend/.env`:

```
PUBLIC_API_BASE=http://127.0.0.1:8000
```

### Planned: Image → LaTeX → PDF workflow

High-level: Upload image → Preprocess → Convert to LaTeX → Compile to PDF → Preview.

#### Planned project structure additions

```
app/
  routers/
    uploads.py            # image uploads & retrieval
    preprocess.py         # preprocessing operations
    convert.py            # OCR → LaTeX conversion
    compile.py            # LaTeX compile → PDF
  services/
    image_preprocess.py   # preprocessing logic
    ocr_to_latex.py       # OCR and parsing
    latex_compile.py      # compilation to PDF
  models/
    schemas.py            # Pydantic models
    storage.py            # storage helpers/paths
data/
  uploads/ processed/ latex/ pdf/
```

#### API routes

- POST `/api/uploads`: upload an image → `{ jobId }`
- POST `/api/preprocess/{jobId}`: apply preprocessing → `{ jobId }`
- POST `/api/convert/{jobId}`: OCR/convert → `{ jobId }`
- POST `/api/compile/{jobId}`: compile → `{ jobId }`
- GET `/api/latex/{jobId}`: return LaTeX source
- GET `/api/pdf/{jobId}`: return compiled PDF
- GET `/api/status/{jobId}`: get job status
- GET `/api/jobs`: get all jobs
- DELETE `/api/jobs/{jobId}`: delete a job

Notes:

- Endpoints may return `{ jobId }` for async processing with polling on `/api/status/{jobId}`.
- Storage can be local under `data/` with short-lived cleanup.
