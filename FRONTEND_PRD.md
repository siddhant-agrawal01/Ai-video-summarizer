# Frontend PRD — AI Video Summarizer & Meeting Assistant

## 1. Product Overview

Build a **Streamlit-based web frontend** that wraps the existing Python backend pipeline into an intuitive, single-page application. The user should be able to submit a video/audio source, watch the processing pipeline progress in real-time, view all generated insights in organized tabs/sections, and chat with the meeting transcript through a built-in RAG-powered chatbot — all without touching a terminal.

---

## 2. Target Users

| Persona | Description |
|---|---|
| **Working Professional** | Attends meetings daily, needs quick automated minutes with action items and decisions |
| **Student / Researcher** | Wants to summarize long lectures or YouTube videos into key points |
| **Content Creator** | Needs transcripts and summaries from their own video/audio content |
| **Non-English Speaker** | Uses Hinglish in meetings and needs automatic English translation + summarization |

---

## 3. Backend Capabilities (What the frontend must expose)

The backend (`main.py → run_pipeline()`) accepts a source and language, and returns a dictionary with the following keys:

| Backend Output Key | Data Type | Description |
|---|---|---|
| `title` | `str` | Auto-generated professional meeting title (max 8 words) |
| `transcript` | `str` | Full raw transcript of the audio/video |
| `summary` | `str` | Professional bulleted summary of the entire meeting |
| `action_items` | `str` | Extracted tasks with owners and deadlines |
| `key_decisions` | `str` | All major decisions made in the meeting |
| `open_questions` | `str` | Unresolved queries or follow-up topics |
| `rag_chain` | `object` | LangChain RAG chain for interactive Q&A over the transcript |

---

## 4. Functional Requirements

### 4.1 Input Section — Source Submission

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | **YouTube URL Input** — A text input field where the user can paste a YouTube video URL (regular videos, shorts, playlists) | P0 |
| FR-02 | **Local File Upload** — A file uploader that accepts audio/video files (`.mp4`, `.mp3`, `.wav`, `.webm`, `.m4a`, `.ogg`, `.flac`) | P0 |
| FR-03 | **Language Selector** — A dropdown or radio button to choose between `English` and `Hinglish` transcription mode | P0 |
| FR-04 | **Submit / Process Button** — A clearly labeled button that triggers the backend `run_pipeline()` | P0 |
| FR-05 | **Input Validation** — Show inline error if: no source provided, invalid URL format, unsupported file type | P1 |

### 4.2 Processing Status & Progress

| ID | Requirement | Priority |
|---|---|---|
| FR-06 | **Pipeline Progress Indicator** — Show a step-by-step progress tracker as the backend processes. Steps: `Downloading Audio → Chunking → Transcribing → Summarizing → Extracting Insights → Building RAG Index` | P0 |
| FR-07 | **Spinner / Loading State** — Show a loading spinner with descriptive text during each step (e.g., "Transcribing audio with Whisper...") | P0 |
| FR-08 | **Error Handling UI** — Display user-friendly error messages if any pipeline step fails (e.g., invalid URL, API key missing, network timeout) | P1 |
| FR-09 | **Estimated Time Hint** — Display a rough estimate like "This may take 2-5 minutes depending on video length" | P2 |

### 4.3 Results Dashboard — Post-Processing Views

Once `run_pipeline()` returns, display all results in an organized, tabbed dashboard layout:

#### 4.3.1 Meeting Title Header

| ID | Requirement | Priority |
|---|---|---|
| FR-10 | Display the auto-generated `title` as a large heading at the top of the results section | P0 |

#### 4.3.2 Summary Tab

| ID | Requirement | Priority |
|---|---|---|
| FR-11 | Display the full `summary` in a formatted markdown/bullet-point view | P0 |
| FR-12 | **Copy to Clipboard** — Button to copy the entire summary text | P1 |

#### 4.3.3 Full Transcript Tab

| ID | Requirement | Priority |
|---|---|---|
| FR-13 | Display the full raw `transcript` in a scrollable text area | P0 |
| FR-14 | **Copy to Clipboard** — Button to copy the full transcript | P1 |
| FR-15 | **Search in Transcript** — A search/filter input to highlight or jump to specific keywords within the transcript | P2 |

#### 4.3.4 Action Items Tab

| ID | Requirement | Priority |
|---|---|---|
| FR-16 | Display extracted `action_items` as a structured list (task, owner, deadline columns) | P0 |
| FR-17 | **Copy to Clipboard** — Button to copy action items | P1 |

#### 4.3.5 Key Decisions Tab

| ID | Requirement | Priority |
|---|---|---|
| FR-18 | Display extracted `key_decisions` as a numbered list | P0 |
| FR-19 | **Copy to Clipboard** — Button to copy key decisions | P1 |

#### 4.3.6 Open Questions Tab

| ID | Requirement | Priority |
|---|---|---|
| FR-20 | Display extracted `open_questions` as a numbered list | P0 |
| FR-21 | **Copy to Clipboard** — Button to copy open questions | P1 |

### 4.4 RAG Chat Interface — "Chat with Your Meeting"

| ID | Requirement | Priority |
|---|---|---|
| FR-22 | **Chat Panel** — A dedicated chat interface (either in a sidebar or a separate tab) where users can type questions about the meeting | P0 |
| FR-23 | **Message Bubbles** — Display user messages and assistant responses in a conversational chat-bubble format | P0 |
| FR-24 | **Chat History** — Maintain the conversation history within the current session (scrollable) | P0 |
| FR-25 | **Loading Indicator** — Show a typing indicator while the RAG chain is processing a question | P1 |
| FR-26 | **Suggested Questions** — Display 3-4 auto-generated starter questions based on the transcript (e.g., "What were the main topics discussed?", "Who is responsible for the next steps?") | P2 |
| FR-27 | **Clear Chat** — Button to reset the chat conversation | P2 |

### 4.5 Export & Download

| ID | Requirement | Priority |
|---|---|---|
| FR-28 | **Download as PDF** — Generate and download a PDF report containing: Title, Summary, Action Items, Key Decisions, Open Questions, and Full Transcript | P1 |
| FR-29 | **Download as TXT** — Download the full transcript as a plain `.txt` file | P1 |
| FR-30 | **Download Summary Only** — Option to download just the summary section as a standalone file | P2 |

---

## 5. Non-Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| NFR-01 | **Responsive Layout** — The UI must work well on desktop browsers (min 1024px). Mobile is nice-to-have. | P1 |
| NFR-02 | **Session State Management** — Use Streamlit's `st.session_state` to persist results and chat history without re-running the pipeline on page interaction | P0 |
| NFR-03 | **Environment Variable Validation** — On app startup, check if `MISTRAL_API_KEY` is set. Show a clear warning/setup guide if missing. | P1 |
| NFR-04 | **Performance** — The UI must not block or freeze during long-running pipeline operations. Use `st.spinner()` and status containers. | P0 |
| NFR-05 | **Theming** — Apply a clean, professional dark/light theme using Streamlit's theming config (`.streamlit/config.toml`) | P2 |

---

## 6. Page Layout Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    🎬 AI Video Summarizer                   │
│                   & Meeting Assistant                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  📎 Paste YouTube URL   OR   📁 Upload Audio/Video  │    │
│  │  🌐 Language: [English ▼ | Hinglish]                │    │
│  │              [ 🚀 Process Video ]                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  ⏳ Pipeline Progress                                │    │
│  │  ✅ Downloading → ✅ Chunking → 🔄 Transcribing     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  📌 Title: "Quarterly Product Review Meeting"       │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │ [Summary] [Transcript] [Actions] [Decisions] [Q&A]  │    │
│  │                                                     │    │
│  │  • The team discussed Q3 performance metrics...     │    │
│  │  • Revenue targets were reviewed and...             │    │
│  │  • Next sprint planning is scheduled for...         │    │
│  │                                                     │    │
│  │  [📋 Copy] [📄 Download PDF] [📝 Download TXT]      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  💬 Chat with Your Meeting                          │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │ 🧑 You: What action items came out of this? │    │    │
│  │  │ 🤖 AI: Based on the meeting, the key        │    │    │
│  │  │        action items are: 1) ...              │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │  [Type your question here...           ] [Send]     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Tech Stack (Frontend)

| Layer | Technology | Purpose |
|---|---|---|
| **UI Framework** | Streamlit `>=1.35.0` | Rapid Python-native web UI |
| **UI Extras** | `streamlit-extras >=0.4.0` | Additional widgets (e.g., colored headers, metric cards) |
| **PDF Export** | `reportlab >=4.2.0` or `fpdf2 >=2.7.9` | Generate downloadable PDF reports |
| **Hot Reload** | `watchdog >=4.0.0` | Faster Streamlit dev-server reload |
| **State Mgmt** | `st.session_state` (built-in) | Persist pipeline results and chat history |
| **Theming** | `.streamlit/config.toml` | Custom color scheme and font config |

---

## 8. Streamlit Session State Schema

```python
st.session_state = {
    # Pipeline results (populated after run_pipeline completes)
    "title": str | None,
    "transcript": str | None,
    "summary": str | None,
    "action_items": str | None,
    "key_decisions": str | None,
    "open_questions": str | None,
    "rag_chain": object | None,

    # UI state
    "pipeline_running": bool,       # True while pipeline is executing
    "pipeline_complete": bool,      # True after successful completion
    "pipeline_error": str | None,   # Error message if pipeline fails

    # Chat state
    "chat_history": list[dict],     # [{"role": "user"|"assistant", "content": str}, ...]
}
```

---

## 9. Backend Integration Points

The frontend communicates with the backend via **direct Python function calls** (no REST API needed since Streamlit runs in the same Python process):

| Frontend Action | Backend Function Call | Returns |
|---|---|---|
| User clicks "Process Video" | `run_pipeline(source, language)` | `dict` with all results |
| User sends chat message | `ask_question(rag_chain, question)` | `str` (answer) |

### Granular Pipeline Steps (for progress tracking)

If the frontend needs step-by-step progress (instead of one big `run_pipeline` call), it should call the backend modules individually:

```python
# Step 1: Download & chunk audio
from utils.audio_processor import process_input
chunks = process_input(source)   # → list of WAV chunk paths

# Step 2: Transcribe all chunks
from core.transcriber import transcribe_all
transcript = transcribe_all(chunks, language)   # → str

# Step 3: Generate title
from core.summarizer import generate_title
title = generate_title(transcript)   # → str

# Step 4: Summarize transcript
from core.summarizer import summarize
summary = summarize(transcript)   # → str

# Step 5: Extract insights
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
action_items = extract_action_items(transcript)    # → str
decisions = extract_key_decisions(transcript)       # → str
questions = extract_questions(transcript)           # → str

# Step 6: Build RAG index
from core.rag_engine import build_rag_chain
rag_chain = build_rag_chain(transcript)   # → LangChain Runnable

# Step 7 (on-demand): Chat Q&A
from core.rag_engine import ask_question
answer = ask_question(rag_chain, user_question)   # → str
```

---

## 10. File Structure (Proposed)

```
Ai-video/
├── main.py                   # CLI entry point (existing)
├── app.py                    # 🆕 Streamlit frontend entry point
├── .streamlit/
│   └── config.toml           # 🆕 Streamlit theme configuration
├── core/
│   ├── extractor.py          # Action items, decisions, questions extraction
│   ├── rag_engine.py         # RAG chain builder + Q&A
│   ├── summarizer.py         # Map-reduce summarizer + title generator
│   ├── transcriber.py        # Whisper + Sarvam AI transcription
│   └── vector_store.py       # Chroma vector DB management
├── utils/
│   ├── audio_processor.py    # YouTube download, WAV conversion, chunking
│   └── pdf_exporter.py       # 🆕 PDF report generation utility
├── downloades/               # Downloaded audio files (auto-created)
├── vector_db/                # Chroma DB persistence (auto-created)
├── .env                      # API keys
├── Requirements.txt          # Python dependencies
└── README.md                 # Backend documentation
```

---

## 11. Feature Roadmap

### Phase 1 — MVP (Must Have)
- [ ] Source input (YouTube URL + file upload)
- [ ] Language selection (English / Hinglish)
- [ ] Pipeline execution with spinner/progress
- [ ] Results display with tabs (Summary, Transcript, Actions, Decisions, Questions)
- [ ] RAG chat interface
- [ ] Session state management

### Phase 2 — Enhanced UX
- [ ] Copy-to-clipboard for all sections
- [ ] PDF & TXT export/download
- [ ] Error handling with user-friendly messages
- [ ] Environment variable validation on startup
- [ ] Suggested starter questions in chat

### Phase 3 — Polish
- [ ] Custom Streamlit theme (dark mode)
- [ ] Transcript search/keyword highlighting
- [ ] Estimated processing time hints
- [ ] Chat history clear button
- [ ] Mobile-responsive improvements

---

## 12. Running the Frontend

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the Streamlit app
streamlit run app.py
```

The app will be available at `http://localhost:8501`.
