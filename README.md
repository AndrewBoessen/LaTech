# LaTech

## Architecture (FastAPI)

### Project Structure

```
app/
  main.py              # FastAPI app (serves / and /api/*)
static/
  index.html           # Frontend HTML
  styles.css           # Frontend CSS
  app.js               # Frontend JS
requirements.txt       # Python dependencies
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

### Run (development)

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` in your browser.

### API Endpoints

- `GET /api/health` → `{ "status": "ok" }`
- `POST /api/echo` with JSON `{ "message": "hello" }` → `{ "echo": "hello" }`

### Notes

- Static files are served under `/static` and `index.html` is served at `/`.
- You can also run with `python app/main.py` which launches uvicorn with reload for quick local testing.

