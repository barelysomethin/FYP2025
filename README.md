# Hybrid News Summarizer

A web-based application that uses AI to generate extractive, abstractive, and hybrid summaries of news articles.

## Features

- **Extractive Summary**: Uses TextRank algorithm to identify key sentences.
- **Abstractive Summary**: Uses Facebook's BART Large CNN model via Hugging Face API to generate human-like summaries.
- **Hybrid Summary**: Combines both approaches for optimized results.
- **Modern UI**: Clean, responsive interface built with React and Vanilla CSS (Premium Design).

## Tech Stack

- **Frontend**: React, Vite
- **Backend**: FastAPI, Python, NLTK, Newspaper3k
- **AI/ML**: Hugging Face Inference API, Scikit-learn, NetworkX

## Prerequisites

- Python 3.10+
- Node.js 16+
- Hugging Face API Key (Free)

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/barelysomethin/FYP2025.git
cd FYP2025
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment and install dependencies:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:

```bash
# backend/.env
HF_API_KEY=your_hugging_face_api_key_here
```

start the backend server:

```bash
uvicorn main:app --reload
```

The backend will run at `http://127.0.0.1:8000`.

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend server:

```bash
npm run dev
```

The frontend will run at `http://localhost:5173` (or similar).

## Usage

1.  Open the frontend URL in your browser.
2.  Paste a link to a news article (e.g., from BBC, CNN, TechCrunch).
3.  Click **Summarize Article**.
4.  View the generated summaries.
