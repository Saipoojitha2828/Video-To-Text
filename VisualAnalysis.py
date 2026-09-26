from ultralytics import YOLO
import cv2
import os

# Load YOLOv8 nano model (lightweight and fast)
model = YOLO("yolov8n.pt")

def detect_objects(frame_paths):
    """
    Detect objects in video frames using YOLOv8.
    
    Args:
        frame_paths: List of paths to frame images
    
    Returns:
        list: List of unique detected object classes
    """
    
    detected_objects = []
    
    try:
        for frame_path in frame_paths:
            if not os.path.exists(frame_path):
                continue
            
            # Run YOLO detection
            results = model(frame_path, verbose=False)
            
            # Extract class names from results
            for result in results:
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        class_id = int(box.cls)
                        label = model.names[class_id]
                        detected_objects.append(label)
    
    except Exception as e:
        print(f"Error in object detection: {e}")
    
    # Return unique objects while preserving order
    seen = set()
    unique_objects = []
    for obj in detected_objects:
        if obj not in seen:
            seen.add(obj)
            unique_objects.append(obj)
    
    return unique_objects


def detect_objects_with_confidence(frame_paths, confidence_threshold=0.5):
    """
    Detect objects with confidence scores and filtering.
    
    Args:
        frame_paths: List of paths to frame images
        confidence_threshold: Only include detections above this confidence (0-1)
    
    Returns:
        dict: Objects with confidence scores
    """
    
    detected_data = {}
    
    try:
        for frame_path in frame_paths:
            if not os.path.exists(frame_path):
                continue
            
            results = model(frame_path, verbose=False)
            
            for result in results:
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        class_id = int(box.cls)
                        confidence = float(box.conf)
                        
                        if confidence >= confidence_threshold:
                            label = model.names[class_id]
                            
                            if label not in detected_data:
                                detected_data[label] = []
                            
                            detected_data[label].append({
                                'confidence': round(confidence, 2),
                                'frame': os.path.basename(frame_path)
                            })
    
    except Exception as e:
        print(f"Error in object detection: {e}")
    
    return detected_data


def get_object_list(frame_paths, confidence_threshold=0.5):
    """
    Get simple list of detected objects.
    
    Args:
        frame_paths: List of paths to frame images
        confidence_threshold: Only include detections above this confidence
    
    Returns:
        list: List of unique detected object labels
    """
    
    detected_data = detect_objects_with_confidence(frame_paths, confidence_threshold)
    return list(detected_data.keys())


def analyze_objects_across_frames(frame_paths):
    """
    Analyze which objects appear in which frames.
    Useful for understanding scene composition.
    
    Args:
        frame_paths: List of paths to frame images
    
    Returns:
        dict: Frame-by-frame object analysis
    """
    
    frame_analysis = {}
    
    try:
        for frame_path in frame_paths:
            if not os.path.exists(frame_path):
                continue
            
            frame_objects = []
            results = model(frame_path, verbose=False)
            
            for result in results:
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        class_id = int(box.cls)
                        confidence = float(box.conf)
                        label = model.names[class_id]
                        frame_objects.append({
                            'object': label,
                            'confidence': round(confidence, 2)
                        })
            
            frame_analysis[os.path.basename(frame_path)] = frame_objects
    
    except Exception as e:
        print(f"Error analyzing frames: {e}")
    
    return frame_analysis


def get_object_summary(frame_paths):
    """
    Get summary statistics about detected objects.
    
    Args:
        frame_paths: List of paths to frame images
    
    Returns:
        dict: Summary statistics
    """
    
    all_objects = detect_objects(frame_paths)
    object_counts = {}
    
    for obj in all_objects:
        object_counts[obj] = object_counts.get(obj, 0) + 1
    
    return {
        'unique_objects': list(set(all_objects)),
        'total_detections': len(all_objects),
        'object_counts': object_counts,
        'most_common': max(object_counts.items(), key=lambda x: x[1])[0] if object_counts else None
    }