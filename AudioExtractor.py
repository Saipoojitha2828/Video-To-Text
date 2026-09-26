import subprocess
import os

def extract_audio(video_path):
    """
    Extract audio from video using FFmpeg.
    Handles all video formats: mp4, mov, avi, mkv, webm, etc.
    """
    filename = os.path.basename(video_path)
    name = filename.split(".")[0]
    
    # Create audio directory if it doesn't exist
    os.makedirs("audio", exist_ok=True)
    
    audio_path = f"audio/{name}.wav"
    
    # FFmpeg command to extract audio
    command = [
        'ffmpeg',
        '-i', video_path,
        '-q:a', '9',  # Quality (9 is highest quality)
        '-n',  # Don't overwrite existing files
        audio_path
    ]
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            print(f"FFmpeg Error: {result.stderr}")
            return None
            
        return audio_path
    except subprocess.TimeoutExpired:
        print("Audio extraction timed out")
        return None
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None