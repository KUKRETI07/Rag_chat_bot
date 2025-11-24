# Full Stack RAG Chatbot

This is a production-quality full stack chatbot application using FastAPI (Backend) and React + Tailwind (Frontend). It features a ChatGPT-style UI and integrates with a RAG pipeline.

## Project Structure

- `backend/`: FastAPI application, RAG logic, and PDF document.
- `frontend/`: React application with Tailwind CSS.

## Setup & Running

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```

**Important:**
- Ensure `combined_handbook.pdf` is in the `backend/` directory (it should be there already).
- Open `backend/.env` and add your `MISTRAL_API_KEY`.

Run the server:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Run the development server:
```bash
npm run dev
```
The application will be available at `http://localhost:5173`.

## Features

- **RAG Integration**: Uploads and queries `combined_handbook.pdf`.
- **Chat History**: Saves chat sessions to `backend/chat_history.json`.
- **Modern UI**: Dark mode, message bubbles, sidebar history.
- **Responsive**: Works on mobile and desktop.

## Notes

- The RAG pipeline initializes on server startup. If the PDF is missing or the API key is invalid, it will print a warning but the server will still start.
- Chat history is stored locally in a JSON file.
