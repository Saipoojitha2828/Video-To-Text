**🎬 Textify - Video to Text Transcriber**

Convert any video into text! Upload a video file or paste a YouTube link to get instant transcription in 100+ languages with optional similarity comparison.

---

## 📋 Overview

Textify is an AI-powered application that:
- Extracts audio from videos (file upload or YouTube links)
- Converts speech to text using Whisper (supports 100+ languages)
- Auto-detects language from audio
- Optionally compares transcripts with reference answers
- Provides similarity scores, concept coverage analysis, and detailed feedback
- Detects objects in video frames using YOLO

---

## ✨ Features

- 📹 **Multi-Format Video Support** — MP4, MOV, MKV, AVI, WebM, audio files
- 🎥 **YouTube URL Support** — Paste any YouTube link directly
- 🌐 **100+ Languages** — Auto-detect and transcribe in any language
- 📊 **Similarity Comparison** — Compare with reference answer
- 📈 **Analytics** — Similarity score, concept coverage, missing concepts
- 🤖 **Object Detection** — YOLO detects objects in video frames
- ⚡ **Fast & Reliable** — Processes videos in minutes
- 💬 **Smart Feedback** — AI-powered suggestions based on comparison

---

## 🛠️ Tech Stack

**Backend:**
- FastAPI — REST API framework
- Python — Core language

**Frontend:**
- Streamlit — Web UI

**Speech & Audio:**
- OpenAI Whisper — Speech-to-text (100+ languages)
- FFmpeg — Audio extraction from video
- Librosa — Audio processing

**Computer Vision:**
- OpenCV — Video frame extraction
- YOLO v8 — Object detection

**NLP & Similarity:**
- Scikit-learn — TF-IDF similarity
- Sentence Transformers — Semantic similarity
- LangDetect — Language detection

**Video:**
- yt-dlp — YouTube video download

**Translation:**
- LibreTranslate API — Multi-language translation

---

**🏗️ System Architecture**

<img width="1472" height="1608" alt="image" src="https://github.com/user-attachments/assets/e48fbd6e-9895-48d7-a3d7-397bada44822" />

---

## 🚀 How to Run

### Prerequisites

# Install FFmpeg (required for audio extraction)
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg


### Step 1: Install Dependencies

pip install -r requirements.txt
pip install yt-dlp

### Step 2: Run Backend

**Terminal 1:**

uvicorn app:app --reload


You should see:

INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.

### Step 3: Run Frontend

**Terminal 2:**

streamlit run StreamliApp.py

Browser opens at: `http://localhost:8501`

---

## 📤 How to Use

1. **Upload Video** — Choose file upload OR paste YouTube/video URL
2. **Select Language** (optional) — Leave blank for auto-detection
3. **Add Reference** (optional) — Paste reference answer for comparison
4. **Click "Analyze Video"** — Wait for processing
5. **View Results** — See transcript, stats, and comparison metrics

---

## 📊 Output

### Transcript Mode (No Reference)

📝 Transcript
🌐 English

[Full transcript of video speech]

Video Statistics:
- Duration: 2:45
- Words: 342
- Speaking Rate: 124 WPM
- Detected Objects: person, whiteboard, marker
- 

### Comparison Mode (With Reference)

📝 Transcript
[Transcript shown]

📊 Comparison Analysis
Similarity Score: 78%
Concept Coverage: 85%

💡 Feedback: Good answer but some details are missing.

Missing Concepts: algorithm, optimization
Extra Concepts: example, practice

---

## 📝 Example Workflow

**Input:**
- YouTube video: https://youtu.be/1B5ppTif5ZY
- Reference: "Machine learning is a subset of AI..."

**Output:**

Transcript: "Machine learning is a branch of artificial intelligence..."
Language: English
Duration: 3:22
Words: 456
Speaking Rate: 130 WPM

Similarity Score: 82%
Concept Coverage: 90%
Feedback: Excellent explanation. You covered most key points.

---

## 🎯 Key Technologies Used

| Component | Technology |
|-----------|-----------|
| Speech-to-Text | Whisper (OpenAI) |
| Video Processing | FFmpeg, OpenCV |
| Object Detection | YOLO v8 |
| Similarity Analysis | TF-IDF + Sentence Transformers |
| Language Detection | LangDetect |
| Translation | LibreTranslate |
| Web Framework | FastAPI + Streamlit |

---

## ✅ What's Included

✓ Multi-format video support (MP4, MOV, MKV, WebM, etc.)  
✓ YouTube video download & processing  
✓ 100+ language transcription  
✓ Auto language detection  
✓ Similarity scoring with reference text  
✓ Concept coverage analysis  
✓ Object detection from video frames  
✓ Speaking rate calculation  
✓ AI-powered feedback  
✓ Beautiful Streamlit UI  
✓ RESTful API backend  

