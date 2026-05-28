# AI Video & Meeting Assistant

A full-stack AI-powered application that transforms YouTube videos and local meeting recordings into actionable intelligence. This tool automatically transcribes audio, generates concise summaries, extracts key decisions and action items, and features a built-in **RAG (Retrieval-Augmented Generation) Chat** so you can talk directly to your transcript.

## Features
* **Dual-Engine Transcription**: 
  * Uses local **OpenAI Whisper** for English audio.
  * Integrates **Sarvam AI** for native "Hinglish" speech-to-text and translation.
* **Smart Summarization**: Uses **Mistral AI** via LangChain to map-reduce large transcripts into bulleted, professional summaries and titles.
* **Information Extraction**: Automatically identifies and isolates Action Items, Key Decisions, and Open Questions.
* **Interactive RAG Chat**: Powered by **ChromaDB** and HuggingFace embeddings, allowing you to ask questions and get precise answers based *only* on the context of your meeting.
* **Beautiful Streamlit UI**: A sleek, dark-mode interface with animated status tracking and a native chat window.
* **Flexible Input**: Accepts both direct YouTube URLs (via `yt-dlp`) and local audio/video files.

## Tech Stack
* **Frontend**: Streamlit
* **Core Processing**: Python, `pydub`, `yt-dlp`, FFmpeg
* **AI & NLP Pipeline**: LangChain (LCEL)
* **Language Models**: Mistral AI (`mistral-small-latest`)
* **Speech-to-Text**: Whisper (Local), Sarvam AI API
* **Vector Database & Embeddings**: ChromaDB, HuggingFace (`all-MiniLM-L6-v2`)

## Project Structure
├── app.py                      # Streamlit frontend web application
├── main.py                     # CLI entry point for terminal usage
├── test.py                     # Testing script for core modules
├── utils/
│   └── audio_processor.py      # Handles YouTube downloads, file conversion, and audio chunking
├── core/
│   ├── transcriber.py          # Whisper & Sarvam AI transcription routing
│   ├── summarizer.py           # Mistral LLM title and summary generation
│   ├── extractor.py            # Extracts action items, decisions, and questions
│   ├── vector_store.py         # ChromaDB and HuggingFace embeddings setup
│   └── rag_engine.py           # LangChain RAG pipeline for the chat feature
└── requirements.txt            # Project dependencies

## Getting Started

### 1. Prerequisites
* Python 3.8+
* **FFmpeg**: You must have FFmpeg installed on your system for audio extraction and conversion to work.
  * *Mac*: `brew install ffmpeg`
  * *Linux*: `sudo apt install ffmpeg`
  * *Windows*: Download from the official site and add to PATH.

### 2. Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

### 3. Install Dependencies
Set up a virtual environment and install the required Python packages.
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

pip install streamlit langchain langchain-mistralai langchain-chroma langchain-huggingface pydub yt-dlp openai-whisper requests python-dotenv

### 4. Environment Variables
Create a `.env` file in the root directory and add your API keys:

# Required for Summarization, Extraction, and RAG
MISTRAL_API_KEY=your_mistral_api_key_here

# Required for Hinglish Transcription
SARVAM_API_KEY=your_sarvam_api_key_here

# Optional Configurations
WHISPER_MODEL=small
SARVAM_STT_MODEL=saaras:v2.5

### 5. Run the Application

**Option A: Web Interface (Recommended)**
Launch the modern Streamlit interface:
streamlit run app.py

*The UI will open automatically in your browser at `http://localhost:8501`.*

**Option B: Command Line Interface**
Run the pipeline directly in your terminal:
python main.py

*You will be prompted to enter a YouTube URL or file path, and the language preference.*

## How the Pipeline Works
1. **Audio Ingestion**: `yt-dlp` fetches YouTube audio, or `pydub` converts local video to WAV format. The audio is split into manageable chunks.
2. **Transcription**: Chunks are sent to Whisper (English) or Sarvam AI (Hinglish/<=30s sliced chunks).
3. **Analysis**: LangChain uses Mistral AI to split the transcript, summarize the segments, generate a title, and extract key metrics.
4. **Vectorization**: The transcript is chunked and embedded into a local ChromaDB instance using HuggingFace embeddings.
5. **Retrieval**: When a user asks a question in the chat, the RAG engine queries ChromaDB for the most relevant transcript segments and uses Mistral to formulate a precise answer.
