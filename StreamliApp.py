import streamlit as st
import time
import tempfile
import os
import requests
from datetime import datetime

st.set_page_config(
    page_title="Textify - Video to Text",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { 
    font-family: 'Inter', sans-serif !important; 
    box-sizing: border-box; 
}

html, body,
.stApp, .main,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="block-container"],
[data-testid="stMainBlockContainer"] {
    background-color: #FFFFFF !important;
    color: #1A1A2E !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    visibility: hidden !important;
    display: none !important;
}

.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    max-width: 900px !important;
}

/* NAV */
.nav {
    background: #fff;
    border-bottom: 1px solid #F0EEF6;
    padding: 1rem 0;
    display: flex; 
    align-items: center; 
    justify-content: space-between;
    margin-bottom: 2rem;
}
.nav-brand { 
    display: flex; 
    align-items: center; 
    gap: 12px; 
    font-weight: 700; 
    font-size: 1.2rem; 
    color: #E879A0; 
}
.nav-logo {
    width: 40px; 
    height: 40px; 
    border-radius: 10px;
    background: linear-gradient(135deg, #F0E6FF, #FFD6E0);
    display: flex; 
    align-items: center; 
    justify-content: center; 
    font-size: 1.2rem;
}

/* HERO */
.hero {
    background: linear-gradient(145deg, #FFF0F5 0%, #FFD6E0 30%, #E8D5FF 62%, #C8E8FF 100%);
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    border-radius: 20px;
}
.hero-title { 
    font-size: 2.5rem; 
    font-weight: 800; 
    color: #E879A0; 
    line-height: 1.2; 
    margin-bottom: 0.8rem; 
}
.hero-sub { 
    font-size: 1rem; 
    color: #6B7280; 
    max-width: 600px; 
    margin: 0 auto; 
    line-height: 1.6; 
}

/* CARD */
.card {
    background: #fff;
    border: 1.5px solid #EEE9F8;
    border-radius: 16px;
    padding: 1.8rem;
    box-shadow: 0 2px 14px rgba(120, 80, 200, 0.07);
    margin-bottom: 1.5rem;
}
.card-title { 
    font-size: 1.1rem; 
    font-weight: 700; 
    color: #1A1A2E; 
    margin-bottom: 0.8rem;
}

/* TRANSCRIPT BOX */
.transcript-box {
    background: #F9FAFB; 
    border: 1.5px solid #F0EEF6; 
    border-radius: 12px;
    padding: 1.2rem;
    font-size: 0.95rem; 
    color: #374151;
    line-height: 1.8; 
    min-height: 140px;
    max-height: 400px;
    overflow-y: auto;
}

/* LANGUAGE BADGE */
.lang-badge {
    display: inline-block;
    background: #EDE9FE;
    color: #7C3AED;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

/* BUTTON STYLES */
.stButton > button {
    background: linear-gradient(135deg, #F472B6, #E879A0) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.9rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 18px rgba(232, 121, 160, 0.35) !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover { opacity: 0.87 !important; }

/* TEXTAREA */
.stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid #E5E7EB !important;
    font-size: 0.95rem !important;
    padding: 0.9rem 1rem !important;
}

/* DIVIDER */
.divider {
    border: none;
    border-top: 1.5px solid #F0EEF6;
    margin: 2rem 0;
}

/* STATS */
.stat-card {
    background: #fff;
    border: 1.5px solid #EEE9F8;
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 1px 10px rgba(120, 80, 200, 0.05);
}
.stat-value {
    font-size: 2rem;
    font-weight: 800;
    color: #E879A0;
    line-height: 1;
}
.stat-label {
    font-size: 0.85rem;
    color: #9CA3AF;
    margin-top: 0.5rem;
}

/* FEEDBACK */
.feedback-box {
    border-radius: 12px;
    padding: 1rem;
    border-left: 4px solid;
    line-height: 1.6;
    font-size: 0.95rem;
}
.feedback-excellent { 
    background: #ECFDF5; 
    border-color: #10B981; 
    color: #065F46; 
}
.feedback-good { 
    background: #EFF6FF; 
    border-color: #3B82F6; 
    color: #1E3A8A; 
}
.feedback-fair { 
    background: #FFFBEB; 
    border-color: #F59E0B; 
    color: #92400E; 
}
.feedback-poor { 
    background: #FFF1F2; 
    border-color: #F43F5E; 
    color: #881337; 
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  NAVIGATION
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="nav">
  <div class="nav-brand">
    <div class="nav-logo">🎬</div>
    Textify
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-title">🎬 Textify</div>
  <div class="hero-sub">
    Upload any video or paste a link. Get instant transcription with optional similarity comparison.
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  SECTION 1: VIDEO UPLOAD or URL
# ══════════════════════════════════════════════════════════════
st.markdown("""<div class="card">
  <div class="card-title">📹 Step 1: Add Video</div>
</div>""", unsafe_allow_html=True)

# Choose between upload and URL
input_method = st.radio(
    "How do you want to add the video?",
    options=["Upload File", "Paste URL"],
    horizontal=True,
    label_visibility="collapsed"
)

uploaded_file = None
video_url = None

if input_method == "Upload File":
    uploaded_file = st.file_uploader(
        "Upload any video file",
        type=["mp4", "mov", "avi", "webm", "mkv", "flv", "wav", "m4a", "mp3"],
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        st.success(f"✅ **{uploaded_file.name}** uploaded · {uploaded_file.size / 1024 / 1024:.2f} MB")
else:
    video_url = st.text_input(
        "Paste video URL:",
        placeholder="Example: https://example.com/video.mp4 or YouTube link",
        label_visibility="collapsed"
    )
    if video_url:
        st.success(f"✅ URL provided: {video_url[:50]}...")

# ══════════════════════════════════════════════════════════════
#  SECTION 2: LANGUAGE SELECTION (Optional)
# ══════════════════════════════════════════════════════════════
st.markdown("""<div class="card">
  <div class="card-title">🌐 Step 2: Language (Optional)</div>
  <div style="font-size: 0.9rem; color: #9CA3AF;">Auto-detected if not specified</div>
</div>""", unsafe_allow_html=True)

language = st.selectbox(
    "Select language (or leave blank for auto-detect):",
    options=[
        ("Auto-detect", None),
        ("English", "en"),
        ("Spanish", "es"),
        ("French", "fr"),
        ("German", "de"),
        ("Hindi", "hi"),
        ("Telugu", "te"),
        ("Tamil", "ta"),
        ("Chinese", "zh"),
        ("Japanese", "ja"),
        ("Arabic", "ar"),
        ("Portuguese", "pt"),
    ],
    label_visibility="collapsed",
    index=0
)

# ══════════════════════════════════════════════════════════════
#  SECTION 3: OPTIONAL REFERENCE TEXT
# ══════════════════════════════════════════════════════════════
st.markdown("""<div class="card">
  <div class="card-title">📄 Step 3: Reference Answer (Optional)</div>
  <div style="font-size: 0.9rem; color: #9CA3AF;">Leave blank for transcript-only mode</div>
</div>""", unsafe_allow_html=True)

reference = st.text_area(
    "Paste reference answer here (optional):",
    placeholder="If you want to compare the video explanation with a reference, paste it here. Otherwise, leave blank to just get the transcript.",
    height=120,
    label_visibility="collapsed",
)

# ══════════════════════════════════════════════════════════════
#  EVALUATE BUTTON
# ══════════════════════════════════════════════════════════════
evaluate_clicked = st.button("⚡ Analyze Video", use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  RESULTS SECTION
# ══════════════════════════════════════════════════════════════
if evaluate_clicked:
    # Validation
    if not uploaded_file and not video_url:
        st.warning("⚠️ Please upload a video file or provide a URL.")
        st.stop()

    # Show processing animation
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    
    with st.spinner("Processing video... This may take a minute or two."):
        try:
            # Prepare files/data
            if uploaded_file:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(uploaded_file.read())
                    temp_path = tmp.name
                
                files = {"file": open(temp_path, "rb")}
                data = {
                    "reference_text": reference if reference.strip() else None,
                    "language": language
                }
            else:
                # Use URL
                files = {}
                data = {
                    "video_url": video_url,
                    "reference_text": reference if reference.strip() else None,
                    "language": language
                }

            # Call backend
            response = requests.post(
                "http://127.0.0.1:8000/upload",
                files=files if files else None,
                data=data,
                timeout=600  # 10 minute timeout for large videos
            )

            result = response.json()

            if response.status_code != 200:
                st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                st.stop()

            # Extract results
            transcript = result.get("speech_text", "")
            detected_language = result.get("language_name", "Unknown")
            video_duration = result.get("video_duration", "N/A")
            word_count = result.get("word_count", 0)
            processing_time = result.get("processing_time", 0)
            objects = result.get("objects", [])
            speaking_rate = result.get("speaking_rate", 0)

            # ══════════════════════════════════════════════════════════════
            #  TRANSCRIPT DISPLAY
            # ══════════════════════════════════════════════════════════════
            st.markdown("<div style='font-size: 1.3rem; font-weight: 700; margin-bottom: 1.5rem;'>📝 Transcript</div>", unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""<span class="lang-badge">🌐 {detected_language}</span>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="transcript-box">{transcript}</div>""", unsafe_allow_html=True)

            # Transcript stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""<div class="stat-card">
                  <div class="stat-value">{video_duration}</div>
                  <div class="stat-label">Duration</div>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div class="stat-card">
                  <div class="stat-value">{word_count}</div>
                  <div class="stat-label">Words</div>
                </div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""<div class="stat-card">
                  <div class="stat-value">{speaking_rate}</div>
                  <div class="stat-label">WPM</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

            # ══════════════════════════════════════════════════════════════
            #  COMPARISON SECTION (Only if reference provided)
            # ══════════════════════════════════════════════════════════════
            if result.get("has_comparison", False):
                st.markdown("<div style='font-size: 1.3rem; font-weight: 700; margin-bottom: 1.5rem;'>📊 Comparison Analysis</div>", unsafe_allow_html=True)

                score_pct = result.get("score_percentage", 0)
                similarity_score = result.get("similarity_score", 0)
                feedback = result.get("feedback", "")
                concept_coverage = result.get("concept_coverage", {})

                # Similarity Score Visualization
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 3.5rem; font-weight: 800; color: #E879A0;">{score_pct}%</div>
                        <div style="font-size: 1rem; color: #9CA3AF; margin-top: 0.5rem;">Similarity Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    coverage_pct = concept_coverage.get("coverage_percentage", 0)
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 3.5rem; font-weight: 800; color: #3B82F6;">{coverage_pct}%</div>
                        <div style="font-size: 1rem; color: #9CA3AF; margin-top: 0.5rem;">Concept Coverage</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Feedback
                if score_pct >= 80:
                    fb_class = "feedback-excellent"
                elif score_pct >= 60:
                    fb_class = "feedback-good"
                elif score_pct >= 40:
                    fb_class = "feedback-fair"
                else:
                    fb_class = "feedback-poor"

                st.markdown(f"""<div class="feedback-box {fb_class}">
                  💡 <strong>Feedback:</strong> {feedback}
                </div>""", unsafe_allow_html=True)

                # Concept Analysis
                if concept_coverage.get("missing_concepts"):
                    st.markdown("**Missing Concepts:**")
                    missing = concept_coverage.get("missing_concepts", [])
                    st.write(", ".join(missing[:10]))

                if concept_coverage.get("extra_concepts"):
                    st.markdown("**Extra Concepts (Not in reference):**")
                    extra = concept_coverage.get("extra_concepts", [])
                    st.write(", ".join(extra[:10]))

            else:
                st.info("💡 Add a reference answer and re-analyze to see comparison metrics!")

            # ══════════════════════════════════════════════════════════════
            #  DETAILS
            # ══════════════════════════════════════════════════════════════
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size: 1.3rem; font-weight: 700; margin-bottom: 1rem;'>⚙️ Details</div>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Processing Time:** {processing_time}s")
                st.markdown(f"**Language Detected:** {detected_language}")
            with col2:
                if objects:
                    st.markdown(f"**Detected Objects:** {', '.join(objects[:8])}")
                else:
                    st.markdown("**Detected Objects:** None")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        finally:
            # Clean up temp file if it exists
            if uploaded_file and 'temp_path' in locals():
                try:
                    os.remove(temp_path)
                except:
                    pass