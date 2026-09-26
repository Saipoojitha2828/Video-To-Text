from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import numpy as np
import re

# Load sentence transformer model for semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_similarity(text1, text2):
    """
    Calculate TF-IDF based similarity score between two texts.
    
    Args:
        text1: Reference text
        text2: User's transcript/explanation
    
    Returns:
        float: Similarity score between 0 and 1
    """
    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(vectors[0], vectors[1])
        return float(similarity[0][0])
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0


def calculate_semantic_similarity(text1, text2):
    """
    Calculate semantic similarity using sentence transformers.
    Better for understanding meaning beyond word overlap.
    
    Args:
        text1: Reference text
        text2: User's transcript/explanation
    
    Returns:
        float: Similarity score between 0 and 1
    """
    try:
        embeddings1 = model.encode(text1, convert_to_tensor=True)
        embeddings2 = model.encode(text2, convert_to_tensor=True)
        
        similarity = cosine_similarity(
            [embeddings1.cpu().numpy()],
            [embeddings2.cpu().numpy()]
        )
        return float(similarity[0][0])
    except Exception as e:
        print(f"Error calculating semantic similarity: {e}")
        return 0.0


def extract_concepts(text):
    """
    Extract key concepts/keywords from text.
    Uses simple tokenization and filtering.
    
    Args:
        text: Text to extract concepts from
    
    Returns:
        list: List of concepts
    """
    # Remove special characters and convert to lowercase
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Split into words
    words = text.split()
    
    # Filter out common words (stopwords)
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
        'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
        'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
        'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
        'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
        'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'same', 'so',
        'than', 'too', 'very', 'just', 'as', 'if', 'with', 'from', 'by', 'about',
        'into', 'through', 'during', 'up', 'down', 'out', 'off', 'over', 'under',
        'again', 'further', 'then', 'once', 'here', 'there', 'am', 'my', 'me'
    }
    
    concepts = [w for w in words if w not in stopwords and len(w) > 2]
    
    # Return unique concepts
    return list(set(concepts))


def calculate_concept_coverage(speech_concepts, reference_concepts):
    """
    Calculate what percentage of reference concepts are covered in speech.
    
    Args:
        speech_concepts: List of concepts from user's speech
        reference_concepts: List of concepts from reference text
    
    Returns:
        dict: Coverage statistics
    """
    if not reference_concepts:
        return {
            "coverage_percentage": 100.0,
            "covered_concepts": [],
            "missing_concepts": [],
            "extra_concepts": []
        }
    
    speech_set = set(speech_concepts)
    reference_set = set(reference_concepts)
    
    covered = speech_set.intersection(reference_set)
    missing = reference_set - speech_set
    extra = speech_set - reference_set
    
    coverage_percentage = round((len(covered) / len(reference_set)) * 100, 2) if reference_set else 0
    
    return {
        "coverage_percentage": coverage_percentage,
        "covered_concepts": list(covered),
        "missing_concepts": list(missing),
        "extra_concepts": list(extra),
        "total_reference_concepts": len(reference_set),
        "total_covered_concepts": len(covered)
    }


def get_detailed_comparison(reference_text, speech_text):
    """
    Get detailed comparison between reference and speech.
    
    Args:
        reference_text: Reference text
        speech_text: User's speech text
    
    Returns:
        dict: Detailed comparison metrics
    """
    # Basic similarity
    tfidf_similarity = calculate_similarity(reference_text, speech_text)
    semantic_similarity = calculate_semantic_similarity(reference_text, speech_text)
    
    # Concept analysis
    reference_concepts = extract_concepts(reference_text)
    speech_concepts = extract_concepts(speech_text)
    concept_coverage = calculate_concept_coverage(speech_concepts, reference_concepts)
    
    # Length comparison
    ref_words = len(reference_text.split())
    speech_words = len(speech_text.split())
    length_ratio = round(speech_words / ref_words, 2) if ref_words > 0 else 0
    
    # Determine if too brief, appropriate, or too verbose
    if length_ratio < 0.5:
        length_verdict = "Too Brief"
    elif length_ratio > 2.0:
        length_verdict = "Too Verbose"
    else:
        length_verdict = "Appropriate Length"
    
    return {
        "tfidf_similarity": round(tfidf_similarity, 4),
        "semantic_similarity": round(semantic_similarity, 4),
        "average_similarity": round((tfidf_similarity + semantic_similarity) / 2, 4),
        "concept_coverage": concept_coverage,
        "reference_word_count": ref_words,
        "speech_word_count": speech_words,
        "length_ratio": length_ratio,
        "length_verdict": length_verdict
    }


def highlight_missing_concepts(reference_text, speech_text):
    """
    Identify and highlight concepts missing from speech.
    
    Args:
        reference_text: Reference text
        speech_text: User's speech text
    
    Returns:
        dict: Analysis of missing concepts
    """
    reference_concepts = extract_concepts(reference_text)
    speech_concepts = extract_concepts(speech_text)
    
    missing = set(reference_concepts) - set(speech_concepts)
    
    return {
        "missing_concepts": list(missing),
        "count": len(missing),
        "percentage_missing": round((len(missing) / len(reference_concepts) * 100), 2) if reference_concepts else 0
    }


def extract_sentences(text):
    """Extract sentences from text"""
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def calculate_sentence_similarity(reference_text, speech_text):
    """
    Calculate similarity at sentence level.
    
    Args:
        reference_text: Reference text
        speech_text: User's speech text
    
    Returns:
        list: Similarity scores for each sentence
    """
    ref_sentences = extract_sentences(reference_text)
    speech_sentences = extract_sentences(speech_text)
    
    similarities = []
    
    for ref_sent in ref_sentences:
        if not ref_sent:
            continue
        
        sent_similarities = []
        for speech_sent in speech_sentences:
            if speech_sent:
                sim = calculate_semantic_similarity(ref_sent, speech_sent)
                sent_similarities.append(sim)
        
        if sent_similarities:
            best_match = max(sent_similarities)
            similarities.append({
                "reference_sentence": ref_sent,
                "best_match_score": round(best_match, 4)
            })
    
    return similarities