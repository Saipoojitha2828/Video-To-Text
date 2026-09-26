import requests
import os

# Using LibreTranslate API (free, self-hosted friendly)
LIBRE_TRANSLATE_API = "https://libretranslate.de/translate"

# Language mapping
LANGUAGE_MAP = {
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

def get_available_languages():
    """Get list of available languages for translation"""
    return LANGUAGE_MAP

def translate_text(text, source_language, target_language):
    """
    Translate text from source language to target language using LibreTranslate API.
    
    Args:
        text: Text to translate
        source_language: Source language code (e.g., 'en')
        target_language: Target language code (e.g., 'es')
    
    Returns:
        str: Translated text, or original text if translation fails
    """
    if not text or len(text.strip()) == 0:
        return text
    
    if source_language == target_language:
        return text
    
    try:
        payload = {
            "q": text,
            "source": source_language,
            "target": target_language
        }
        
        response = requests.post(LIBRE_TRANSLATE_API, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result.get("translatedText", text)
            return translated_text
        else:
            print(f"Translation API error: {response.status_code}")
            return text
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Translation service unavailable. Showing original text.")
        return text
    except Exception as e:
        print(f"Error translating text: {e}")
        return text

def translate_transcript(transcript, source_language, target_languages):
    """
    Translate transcript to multiple languages.
    
    Args:
        transcript: Original transcript text
        source_language: Source language code
        target_languages: List of target language codes
    
    Returns:
        dict: {language_code: translated_text, ...}
    """
    translations = {source_language: transcript}
    
    for target_lang in target_languages:
        if target_lang != source_language:
            translated = translate_text(transcript, source_language, target_lang)
            translations[target_lang] = translated
    
    return translations

def get_language_name(language_code):
    """Get human-readable language name from code"""
    return LANGUAGE_MAP.get(language_code, language_code.upper())

def split_text_for_translation(text, chunk_size=500):
    """
    Split text into chunks for more reliable translation of large texts.
    
    Args:
        text: Text to split
        chunk_size: Maximum characters per chunk
    
    Returns:
        list: List of text chunks
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def translate_large_text(text, source_language, target_language):
    """
    Translate large text by splitting into chunks.
    
    Args:
        text: Large text to translate
        source_language: Source language code
        target_language: Target language code
    
    Returns:
        str: Full translated text
    """
    chunks = split_text_for_translation(text)
    translated_chunks = []
    
    for chunk in chunks:
        translated = translate_text(chunk, source_language, target_language)
        translated_chunks.append(translated)
    
    return ' '.join(translated_chunks)