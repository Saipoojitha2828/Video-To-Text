import whisper
from langdetect import detect, LangDetectException
import librosa

# Load Whisper model once
model = whisper.load_model("base")

# Language codes supported by Whisper
LANGUAGE_CODES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'zh': 'Chinese',
    'hi': 'Hindi',
    'te': 'Telugu',
    'ta': 'Tamil',
    'ml': 'Malayalam',
    'ar': 'Arabic',
    'ko': 'Korean',
    'pl': 'Polish',
    'nl': 'Dutch',
    'tr': 'Turkish',
    'vi': 'Vietnamese',
    'th': 'Thai',
}

def get_supported_languages():
    """Return list of supported languages"""
    return LANGUAGE_CODES

def detect_language_from_audio(audio_path):
    """
    Auto-detect language from audio file.
    Uses Whisper's automatic language detection.
    """
    try:
        # Run Whisper with no language specified for auto-detection
        result = model.transcribe(audio_path, language=None, verbose=False)
        detected_lang = result.get("language", "en")
        return detected_lang
    except Exception as e:
        print(f"Error detecting language: {e}")
        return "en"  # Default to English

def transcribe_audio(audio_path, language=None):
    """
    Transcribe audio to text.
    
    Args:
        audio_path: Path to audio file
        language: Language code (e.g., 'en', 'es', 'hi'). 
                 If None, auto-detects language.
    
    Returns:
        tuple: (transcript_text, detected_language)
    """
    try:
        if language is None:
            language = detect_language_from_audio(audio_path)
        
        # Transcribe with specified language
        result = model.transcribe(audio_path, language=language, verbose=False)
        transcript = result["text"]
        
        return transcript, language
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return "", "en"

def get_confidence_scores(audio_path, language=None):
    """
    Get word-level confidence scores from transcription.
    Useful for identifying low-confidence words.
    """
    try:
        if language is None:
            language = detect_language_from_audio(audio_path)
        
        result = model.transcribe(audio_path, language=language, verbose=False)
        
        # Extract segments with timing and confidence
        segments = result.get("segments", [])
        confidence_data = []
        
        for segment in segments:
            confidence_data.append({
                'text': segment.get('text', ''),
                'start': segment.get('start', 0),
                'end': segment.get('end', 0),
            })
        
        return confidence_data
    except Exception as e:
        print(f"Error getting confidence scores: {e}")
        return []

def get_audio_duration(audio_path):
    """Get duration of audio file in seconds"""
    try:
        duration = librosa.get_duration(filename=audio_path)
        return duration
    except Exception as e:
        print(f"Error getting audio duration: {e}")
        return 0