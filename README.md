# LaTech

![LaTech Logo](./assets/logo.png)

A modern web application for converting images to LaTeX and compiling them to PDF. LaTech provides an intuitive interface for uploading images, preprocessing them, converting mathematical expressions to LaTeX format, and generating PDF documents.

https://github.com/user-attachments/assets/a1416ead-f950-4023-abcf-6180fd8e137c

## Features

- **Image Upload**: Upload images containing mathematical expressions
- **Image Preprocessing**: Enhance image quality for better OCR accuracy
- **OCR to LaTeX**: Convert mathematical expressions to LaTeX format using AI
- **PDF Compilation**: Compile LaTeX source to PDF documents
- **Job Management**: Track and manage conversion jobs with status monitoring
- **Modern UI**: Responsive web interface built with SvelteKit and Tailwind CSS

## Prerequisites

### System Requirements

- **Python**: 3.9 or higher
- **Node.js**: 18 or higher
- **npm**: 9 or higher

### External Dependencies

- **LaTeX Distribution**: Required for PDF compilation (e.g., TeX Live, MiKTeX, or MacTeX)
- **Google Generative AI API Key**: Required for OCR to LaTeX conversion (set via environment variables)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AndrewBoessen/LaTech.git
cd LaTech
```

### 2. Set Up Python Environment

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- OpenCV (image processing)
- Google Generative AI (OCR conversion)
- Honcho (process manager)
- And other required dependencies

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

This installs:
- SvelteKit (frontend framework)
- Tailwind CSS (styling)
- CodeMirror (code editor)
- And other frontend dependencies

### 5. Configure Environment Variables (Optional)

Create a `.env` file in the project root or `frontend/.env` for frontend-specific variables:

```bash
# Backend (required)
GEMINI_API_KEY=your_api_key_here

# Frontend (optional)
PUBLIC_API_BASE=http://127.0.0.1:8000
```

## Usage

### Running the Application

The recommended way to run LaTech is using Honcho, which starts both the backend and frontend services simultaneously:

```bash
# Ensure your virtual environment is activated
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Start both backend and frontend
honcho start
```

This command:
- Starts the FastAPI backend on `http://127.0.0.1:8000`
- Starts the SvelteKit frontend on `http://localhost:5173`
- Automatically installs frontend dependencies if needed

### Accessing the Application

Once running, open your browser and navigate to:
- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs (Swagger UI)

### Development Mode

The application runs in development mode by default with:
- Hot reload enabled for both backend and frontend
- Automatic dependency installation for frontend
- Detailed error messages and logging

## Project Structure

```
LaTech/
├── app/                    # FastAPI backend application
│   ├── main.py            # FastAPI app entry point
│   ├── models/            # Data models and schemas
│   │   ├── schemas.py     # Pydantic models
│   │   └── storage.py     # Storage helpers
│   ├── routers/           # API route handlers
│   │   ├── uploads.py     # Image upload endpoints
│   │   ├── preprocess.py  # Preprocessing endpoints
│   │   ├── convert.py     # OCR to LaTeX conversion
│   │   ├── compile.py     # LaTeX compilation
│   │   └── status.py      # Job status tracking
│   └── services/          # Business logic
│       ├── image_preprocess.py
│       ├── ocr_to_latex.py
│       └── latex_compile.py
├── frontend/              # SvelteKit frontend
│   └── src/
│       ├── routes/        # Application pages
│       └── lib/           # Shared components and utilities
├── data/                  # Data storage directories
│   ├── uploads/           # Uploaded images
│   ├── processed/         # Processed images
│   ├── latex/             # LaTeX source files
│   └── pdf/               # Compiled PDF files
├── requirements.txt       # Python dependencies
├── Procfile              # Honcho process definitions
└── README.md             # This file
```

## API Endpoints

The backend provides the following REST API endpoints:

- `POST /api/uploads` - Upload an image file
- `POST /api/preprocess/{jobId}` - Apply preprocessing to an image
- `POST /api/convert/{jobId}` - Convert image to LaTeX
- `POST /api/compile/{jobId}` - Compile LaTeX to PDF
- `GET /api/latex/{jobId}` - Retrieve LaTeX source
- `GET /api/pdf/{jobId}` - Retrieve compiled PDF
- `GET /api/status/{jobId}` - Get job status
- `GET /api/jobs` - List all jobs
- `DELETE /api/jobs/{jobId}` - Delete a job
