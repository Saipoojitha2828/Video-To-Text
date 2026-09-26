import cv2
import os

def extract_frames(video_path, sample_rate=60):
    """
    Extract frames from video for object detection.
    
    Args:
        video_path: Path to video file
        sample_rate: Extract 1 frame every N frames (default: every 60 frames ~2 seconds at 30fps)
    
    Returns:
        list: List of paths to extracted frame files
    """
    
    cap = cv2.VideoCapture(video_path)
    
    # Create frames directory if it doesn't exist
    os.makedirs("frames", exist_ok=True)
    
    frame_paths = []
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Save frame at specified interval
            if frame_count % sample_rate == 0:
                frame_path = f"frames/frame_{frame_count}.jpg"
                cv2.imwrite(frame_path, frame)
                frame_paths.append(frame_path)
            
            frame_count += 1
    
    finally:
        cap.release()
    
    return frame_paths


def extract_frames_adaptive(video_path, max_frames=20):
    """
    Adaptively extract a maximum number of frames from video.
    Useful for handling videos of different lengths.
    
    Args:
        video_path: Path to video file
        max_frames: Maximum number of frames to extract (default: 20)
    
    Returns:
        list: List of paths to extracted frame files
    """
    
    cap = cv2.VideoCapture(video_path)
    
    os.makedirs("frames", exist_ok=True)
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    sample_rate = max(1, total_frames // max_frames)
    
    frame_paths = []
    frame_count = 0
    frames_saved = 0
    
    try:
        while frames_saved < max_frames:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            if frame_count % sample_rate == 0:
                frame_path = f"frames/frame_{frame_count}.jpg"
                cv2.imwrite(frame_path, frame)
                frame_paths.append(frame_path)
                frames_saved += 1
            
            frame_count += 1
    
    finally:
        cap.release()
    
    return frame_paths


def get_video_info(video_path):
    """
    Get information about video file.
    
    Args:
        video_path: Path to video file
    
    Returns:
        dict: Video information (fps, frame count, duration, resolution)
    """
    
    cap = cv2.VideoCapture(video_path)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    duration = frame_count / fps if fps > 0 else 0
    
    cap.release()
    
    return {
        "fps": fps,
        "frame_count": frame_count,
        "duration_seconds": duration,
        "width": width,
        "height": height,
        "resolution": f"{width}x{height}"
    }