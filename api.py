import os
import uuid
import shutil
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

app = FastAPI(title="MeetingAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/process")
async def process_video(
    url: str = Form(None),
    language: str = Form("english"),
    file: UploadFile = File(None),
):
    if file and file.filename:
        ext = os.path.splitext(file.filename)[1]
        save_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        source = save_path
    elif url:
        source = url
    else:
        raise HTTPException(status_code=400, detail="Provide either a YouTube URL or upload a file.")

    try:
        chunks = process_input(source)
        transcript = transcribe_all(chunks, language)
        title = generate_title(transcript)
        summary = summarize(transcript)
        action_items = extract_action_items(transcript)
        key_decisions = extract_key_decisions(transcript)
        open_questions = extract_questions(transcript)
        rag_chain = build_rag_chain(transcript)

        session_id = str(uuid.uuid4())
        sessions[session_id] = rag_chain

        return {
            "session_id": session_id,
            "title": title,
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items,
            "key_decisions": key_decisions,
            "open_questions": open_questions,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ChatRequest(BaseModel):
    session_id: str
    question: str


@app.post("/api/chat")
def chat(req: ChatRequest):
    rag_chain = sessions.get(req.session_id)
    if not rag_chain:
        raise HTTPException(status_code=404, detail="Session not found. Process a video first.")

    try:
        answer = ask_question(rag_chain, req.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("MeetingAI API starting on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
