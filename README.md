# AI Video Summarizer & Meeting Assistant (Backend)

## Overview
The backend of the AI Video Summarizer & Meeting Assistant is a robust Python-based system designed to process audio/video inputs, transcribe them intelligently, extract key insights, generate summaries, and provide a conversational question-answering interface over the meeting context. It leverages state-of-the-art LLMs (Mistral), transcription models (Whisper, Sarvam AI), and RAG pipelines (LangChain, Chroma) to automate meeting minutes and documentation.

## Core Features

### 1. Audio & Video Processing (`utils/audio_processor.py`)
- **YouTube Audio Extraction:** Extracts and downloads the highest quality audio directly from YouTube URLs using `yt-dlp`.
- **Format Normalization:** Converts any incoming local audio or video file to `16kHz`, mono-channel `WAV` format using `pydub` and `ffmpeg` to ensure compatibility with STT models.
- **Smart Chunking:** Automatically splits large audio files into manageable chunks (e.g., 10-minute segments) to optimize memory usage and transcription reliability.

### 2. Intelligent Transcription (`core/transcriber.py`)
- **Dual-Engine Speech-to-Text:**
  - **Local Whisper Model:** Uses OpenAI's Whisper model (runs locally) for highly accurate English transcription.
  - **Sarvam AI Integration:** Specifically designed for "Hinglish" inputs. Routes audio chunks to Sarvam AI's STT-translate API, automatically transcribing and translating Hinglish to English.
- **API Limit Handling:** Seamlessly slices audio into smaller <=25s pieces with safety margins to comply with strict external API constraints, then restitches the final transcript automatically.

### 3. Smart Insight Extraction (`core/extractor.py`)
Utilizing the `ChatMistralAI` model through LangChain's LCEL (LangChain Expression Language), the backend automatically analyzes transcripts to extract structured insights:
- **Action Items:** Identifies exact tasks, responsible owners, and specified deadlines.
- **Key Decisions:** Extracts all major decisions agreed upon during the meeting.
- **Open Questions:** Highlights unresolved queries or topics that require further follow-up.

### 4. Professional Summarization (`core/summarizer.py`)
- **Map-Reduce Architecture:** Handles extremely long transcripts by splitting text into chunks of 3000 characters using `RecursiveCharacterTextSplitter`.
- **Chunk Summarization:** Individually summarizes each chunk and combines them into a cohesive, professional bulleted summary using the Mistral LLM.
- **Auto-Title Generation:** Automatically reads the beginning of the transcript to generate a concise, professional title (max 8 words) for the meeting.

### 5. Retrieval-Augmented Generation (RAG) Engine (`core/rag_engine.py` & `core/vector_store.py`)
- **Semantic Search & Vector DB:** Embeds the meeting transcript using HuggingFace's `all-MiniLM-L6-v2` embeddings and stores them persistently in a local Chroma vector database (`vector_db`).
- **Interactive Q&A:** Allows users to ask specific questions about the meeting. The system retrieves the top 4 most relevant context chunks and uses Mistral to answer the question strictly based on the provided context, preventing hallucinations.

## Technology Stack
- **Audio Processing:** `yt-dlp`, `pydub`, `ffmpeg-python`
- **Speech-to-Text:** `openai-whisper`, `torch`, Sarvam AI API
- **LLM Orchestration:** `langchain`, `langchain-mistralai`, `mistralai`
- **Embeddings & Vector Database:** `chromadb`, `sentence-transformers`, `langchain-community`, `huggingface-hub`

## Environment Configuration
Ensure you have the following environment variables configured in your `.env` file at the root of the project:
```env
# Required for Langchain & LLM features (Summarization, Extraction, RAG)
MISTRAL_API_KEY=your_mistral_api_key_here

# Required for Hinglish translation/transcription
SARVAM_API_KEY=your_sarvam_api_key_here

# Optional overrides
WHISPER_MODEL=small          # default is "small"
SARVAM_STT_MODEL=saaras:v2.5 # default is "saaras:v2.5"
```
