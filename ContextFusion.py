def fuse_context(speech_text, objects):
    """
    Fuse speech transcript and detected visual objects into a unified context.
    
    Args:
        speech_text: Transcribed speech from audio
        objects: List of detected objects from video frames
    
    Returns:
        str: Fused context combining both modalities
    """
    
    # Create visual context string
    if objects and len(objects) > 0:
        # Remove duplicates while preserving some order
        unique_objects = list(dict.fromkeys(objects))
        
        # Format objects nicely
        if len(unique_objects) == 1:
            visual_sentence = f"Visual element: {unique_objects[0]}."
        else:
            objects_str = ", ".join(unique_objects[:-1]) + f", and {unique_objects[-1]}"
            visual_sentence = f"Visual elements include: {objects_str}."
    else:
        visual_sentence = ""
    
    # Combine speech and visual context
    if visual_sentence:
        final_context = f"The person explains: \"{speech_text}\" While showing: {visual_sentence}"
    else:
        final_context = f"The person explains: \"{speech_text}\""
    
    return final_context


def fuse_context_with_confidence(speech_text, objects, objects_confidence=None):
    """
    Enhanced version: fuse context with confidence scores for objects.
    
    Args:
        speech_text: Transcribed speech
        objects: List of detected objects
        objects_confidence: List of confidence scores for each object
    
    Returns:
        str: Fused context with confidence information
    """
    
    if not objects or len(objects) == 0:
        return f"The person explains: \"{speech_text}\""
    
    # Create visual context with confidence
    unique_objects = list(dict.fromkeys(objects))
    
    if objects_confidence and len(objects_confidence) == len(objects):
        # Include confidence for high-confidence detections
        confident_objects = [
            obj for obj, conf in zip(objects, objects_confidence)
            if conf > 0.5  # Only include detections with >50% confidence
        ]
        confident_objects = list(dict.fromkeys(confident_objects))
    else:
        confident_objects = unique_objects
    
    if confident_objects:
        objects_str = ", ".join(confident_objects)
        visual_sentence = f"Visual elements observed: {objects_str}."
    else:
        visual_sentence = ""
    
    if visual_sentence:
        final_context = f"Explanation: \"{speech_text}\" Visual context: {visual_sentence}"
    else:
        final_context = f"Explanation: \"{speech_text}\""
    
    return final_context


def fuse_context_with_timing(speech_text, objects, object_timestamps=None):
    """
    Advanced fusion: include timing information for when objects appear.
    
    Args:
        speech_text: Transcribed speech
        objects: List of detected objects
        object_timestamps: List of timestamps when objects were detected
    
    Returns:
        str: Enriched context with temporal information
    """
    
    if not objects:
        return f"The person explains: \"{speech_text}\""
    
    unique_objects = list(dict.fromkeys(objects))
    objects_str = ", ".join(unique_objects)
    
    final_context = f"Speech: \"{speech_text}\" Visual elements throughout video: {objects_str}."
    
    return final_context