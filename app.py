from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import shutil
import os
import time
import cv2
import requests
from urllib.parse import urlparse

from AudioExtractor import extract_audio
from FrameExtractor import extract_frames
from CleanUp import clear_folder
from SpeechToText import transcribe_audio, get_supported_languages, detect_language_from_audio
from VisualAnalysis import detect_objects
from ContextFusion import fuse_context
from Similarity import calculate_similarity, extract_concepts, calculate_concept_coverage
from Translate import translate_text, translate_transcript, get_language_name

# Try to import yt-dlp, but don't fail if not installed
try:
    import yt_dlp
    YOUTUBE_SUPPORT = True
except ImportError:
    YOUTUBE_SUPPORT = False

app = FastAPI()

UPLOAD_FOLDER = "uploads"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("frames", exist_ok=True)
os.makedirs("audio", exist_ok=True)


def is_youtube_url(url):
    """Check if URL is a YouTube URL"""
    return "youtube.com" in url or "youtu.be" in url


def download_youtube_video(youtube_url):
    """
    Download video from YouTube using yt-dlp.
    
    Args:
        youtube_url: YouTube URL
    
    Returns:
        str: Path to downloaded video, or None if download fails
    """
    if not YOUTUBE_SUPPORT:
        return None
    
    try:
        video_path = f"{UPLOAD_FOLDER}/youtube_video.mp4"
        
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': video_path.replace('.mp4', ''),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            
            # Find the downloaded file
            downloaded_file = ydl.prepare_filename(info)
            
            if os.path.exists(downloaded_file):
                return downloaded_file
            
        return None
    
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        return None


def download_video_from_url(video_url):
    """
    Download video from URL and save locally.
    Supports both direct links and YouTube URLs.
    
    Args:
        video_url: URL to video file
    
    Returns:
        str: Path to downloaded video, or None if download fails
    """
    # Check if it's a YouTube URL
    if is_youtube_url(video_url):
        if YOUTUBE_SUPPORT:
            return download_youtube_video(video_url)
        else:
            raise Exception("YouTube support not available. Install yt-dlp: pip install yt-dlp")
    
    # Handle direct video links
    try:
        parsed_url = urlparse(video_url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename or '.' not in filename:
            filename = "video_from_url.mp4"
        
        video_path = f"{UPLOAD_FOLDER}/{filename}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(video_url, headers=headers, timeout=300, stream=True)
        
        if response.status_code != 200:
            print(f"Error downloading video: Status {response.status_code}")
            return None
        
        with open(video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return video_path
    
    except Exception as e:
        print(f"Error downloading video from URL: {e}")
        return None


def get_video_duration(video_path):
    """Convert video duration to mm:ss format"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    if fps == 0:
        cap.release()
        return "0:00"

    duration_seconds = frame_count / fps
    cap.release()

    minutes = int(duration_seconds // 60)
    seconds = int(duration_seconds % 60)

    return f"{minutes}:{seconds:02d}"


def generate_feedback(score):
    """Generate feedback based on similarity score"""
    if score >= 85:
        return "Excellent explanation. You covered most key points."
    elif score >= 70:
        return "Good answer but some details are missing."
    elif score >= 50:
        return "Partial understanding. Try to explain more key concepts."
    elif score >= 30:
        return "Your explanation is limited. Review the topic and add more relevant points."
    else:
        return "Answer is mostly incorrect or incomplete. Please study the concept again."


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "youtube_support": YOUTUBE_SUPPORT}


@app.get("/languages")
async def get_languages():
    """Get list of supported languages"""
    return {"languages": get_supported_languages()}


@app.post("/transcript-only")
async def transcript_only(
    file: UploadFile = File(None),
    video_url: str = Form(None),
    language: str = Form(None)
):
    """
    Extract transcript from video (file or URL) without comparing to reference.
    """
    start_time = time.time()

    try:
        # Clear previous files
        clear_folder("frames")
        clear_folder("audio")
        clear_folder(UPLOAD_FOLDER)

        # Handle file or URL
        if file:
            video_path = f"{UPLOAD_FOLDER}/{file.filename}"
            with open(video_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        elif video_url:
            video_path = download_video_from_url(video_url)
            if not video_path:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Failed to download video from URL. Make sure the link is valid."}
                )
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Please provide either a video file or URL"}
            )

        # Get video duration
        video_duration = get_video_duration(video_path)

        # Extract audio
        audio_path = extract_audio(video_path)
        if not audio_path:
            return JSONResponse(
                status_code=400,
                content={"error": "Failed to extract audio from video"}
            )

        # Auto-detect language if not specified
        if language is None:
            language = detect_language_from_audio(audio_path)

        # Speech to text
        speech_text, detected_language = transcribe_audio(audio_path, language)

        # Word count
        word_count = len(speech_text.split())

        # Extract frames and detect objects (optional)
        frames = extract_frames(video_path)
        objects = detect_objects(frames) if frames else []

        # Context fusion
        context = fuse_context(speech_text, objects)

        # Processing time
        end_time = time.time()
        processing_time = round(end_time - start_time, 2)

        # Speaking rate
        duration_seconds = int(video_duration.split(":")[0]) * 60 + int(video_duration.split(":")[1])
        speaking_rate = round(word_count / (duration_seconds / 60), 2) if duration_seconds > 0 else 0

        return {
            "speech_text": speech_text,
            "detected_language": detected_language,
            "language_name": get_language_name(detected_language),
            "objects": objects,
            "context": context,
            "video_duration": video_duration,
            "word_count": word_count,
            "processing_time": processing_time,
            "speaking_rate": speaking_rate
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/upload")
async def upload_video(
    file: UploadFile = File(None),
    video_url: str = Form(None),
    reference_text: str = Form(None),
    language: str = Form(None)
):
    """
    Upload video (file or URL) and optionally compare with reference text.
    Supports YouTube URLs, direct links, and file uploads.
    """
    start_time = time.time()

    try:
        # Clear previous files
        clear_folder("frames")
        clear_folder("audio")
        clear_folder(UPLOAD_FOLDER)

        # Handle file or URL
        if file:
            video_path = f"{UPLOAD_FOLDER}/{file.filename}"
            with open(video_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        elif video_url:
            video_path = download_video_from_url(video_url)
            if not video_path:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Failed to download video from URL. Make sure the link is valid and accessible."}
                )
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Please provide either a video file or URL"}
            )

        # Get video duration (mm:ss)
        video_duration = get_video_duration(video_path)

        # Extract audio
        audio_path = extract_audio(video_path)
        if not audio_path:
            return JSONResponse(
                status_code=400,
                content={"error": "Failed to extract audio from video"}
            )

        # Auto-detect language if not specified
        if language is None:
            language = detect_language_from_audio(audio_path)

        # Speech to text
        speech_text, detected_language = transcribe_audio(audio_path, language)

        # Word count
        word_count = len(speech_text.split())

        # Extract frames
        frames = extract_frames(video_path)

        # Object detection
        objects = detect_objects(frames) if frames else []

        # Context fusion
        context = fuse_context(speech_text, objects)

        # Calculate duration in seconds for speaking rate
        duration_parts = video_duration.split(":")
        duration_seconds = int(duration_parts[0]) * 60 + int(duration_parts[1])
        speaking_rate = round(word_count / (duration_seconds / 60), 2) if duration_seconds > 0 else 0

        # Processing time
        end_time = time.time()
        processing_time = round(end_time - start_time, 2)

        result = {
            "speech_text": speech_text,
            "detected_language": detected_language,
            "language_name": get_language_name(detected_language),
            "objects": objects,
            "context": context,
            "video_duration": video_duration,
            "word_count": word_count,
            "processing_time": processing_time,
            "speaking_rate": speaking_rate
        }

        # Only do comparison if reference text is provided
        if reference_text and reference_text.strip():
            # Similarity
            similarity_score = calculate_similarity(reference_text, context)
            score_percentage = round(similarity_score * 100, 2)

            # Concept coverage
            reference_concepts = extract_concepts(reference_text)
            speech_concepts = extract_concepts(speech_text)
            concept_coverage = calculate_concept_coverage(speech_concepts, reference_concepts)

            # Feedback
            feedback = generate_feedback(score_percentage)

            result.update({
                "similarity_score": similarity_score,
                "score_percentage": score_percentage,
                "feedback": feedback,
                "reference_concepts": reference_concepts,
                "speech_concepts": speech_concepts,
                "concept_coverage": concept_coverage,
                "has_comparison": True
            })
        else:
            result["has_comparison"] = False

        return result

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/translate")
async def translate_transcript(
    transcript: str = Form(...),
    source_language: str = Form(...),
    target_languages: str = Form(...)
):
    """
    Translate transcript to multiple languages.
    """
    try:
        targets = [lang.strip() for lang in target_languages.split(",")]
        translations = {}

        for target_lang in targets:
            translated = translate_text(transcript, source_language, target_lang)
            translations[target_lang] = translated

        return {
            "source_language": source_language,
            "translations": translations
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )