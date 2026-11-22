"""
====================================================================
LLM Mini Project (PS 15): Intelligent Library Assistant
Roll Number: 15

Architecture:
  Stage 1: Multi-field fuzzy & keyword pre-filtering via Pandas
  Stage 2: LLM reasoning, ranking & pedagogical explanation (Gemini 3.8 Flash)
  Stage 3: Interactive Streamlit UI with live inventory & analytics
====================================================================
"""

import os
import json
import re
import urllib.request
import urllib.error
from typing import List, Dict, Any, Tuple

import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit Page Config
st.set_page_config(
    page_title="Campus Library Assistant (PS 15)",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Polished Modern Custom CSS
st.markdown("""
<style>
    /* Global Typography & Font Styling */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hero Banner Header */
    .hero-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 50%, #3B82F6 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 14px;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px -2px rgba(30, 58, 138, 0.25);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.02rem;
        opacity: 0.92;
        margin: 0 0 14px 0;
        line-height: 1.4;
    }
    .pill-tag {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
        border: 1px solid rgba(255, 255, 255, 0.25);
    }

    /* Recommendation Book Cards */
    .recommendation-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 6px solid #2563EB;
        padding: 18px 20px;
        border-radius: 12px;
        margin: 14px 0;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .recommendation-card:hover {
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.08);
        border-color: #BFDBFE;
    }
    .card-title {
        font-size: 1.22rem;
        font-weight: 700;
        color: #1E3A8A;
        margin: 0 0 4px 0;
    }
    .card-meta {
        font-size: 0.92rem;
        color: #4B5563;
        margin-bottom: 10px;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 4px;
    }
    .badge-shelf {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
    }
    .badge-copies {
        background-color: #DCFCE7;
        color: #166534;
        border: 1px solid #BBF7D0;
    }
    .badge-level {
        background-color: #EDE9FE;
        color: #5B21B6;
        border: 1px solid #DDD6FE;
    }
    .badge-id {
        background-color: #F1F5F9;
        color: #334155;
        border: 1px solid #E2E8F0;
    }
    .rationale-box {
        background-color: #F8FAFC;
        border-left: 3px solid #3B82F6;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 0.93rem;
        color: #1F2937;
        margin-top: 10px;
        line-height: 1.45;
    }

    /* Tip & Callout Styling */
    .librarian-tip-box {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-left: 5px solid #2563EB;
        padding: 12px 16px;
        border-radius: 8px;
        color: #1E40AF;
        font-size: 0.92rem;
        margin-top: 12px;
        display: flex;
        align-items: center;
    }

    /* Sidebar Clean Metrics */
    .stat-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .stat-number {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1E3A8A;
    }
    .stat-label {
        font-size: 0.78rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "library_catalogue.csv")

# Academic & Tech Acronym Dictionary for Student Query Normalization
TECH_ACRONYMS = {
    "dsa": "data structures algorithms",
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "dbms": "database management systems sql",
    "sql": "sql database queries",
    "os": "operating systems kernel processes",
    "cn": "computer networking tcp ip",
    "k8s": "kubernetes container orchestration",
    "clrs": "introduction to algorithms cormen",
    "nlp": "natural language processing transformers",
    "oops": "object oriented programming design patterns",
    "oop": "object oriented programming design patterns",
}


def load_initial_catalogue() -> List[Dict[str, Any]]:
    """Loads catalogue from CSV file."""
    if not os.path.exists(CSV_PATH):
        st.error(f"Catalogue file not found at {CSV_PATH}")
        return []
    df = pd.read_csv(CSV_PATH)
    df.fillna("", inplace=True)
    return df.to_dict(orient="records")


# Persist catalogue inventory in session state so users can interactively borrow/return books
if "catalogue" not in st.session_state:
    st.session_state["catalogue"] = load_initial_catalogue()

# Track borrowed books in session
if "borrowed_books" not in st.session_state:
    st.session_state["borrowed_books"] = []


def expand_query_acronyms(query: str) -> str:
    """Expands student shorthand acronyms (e.g. 'dsa' -> 'data structures algorithms')."""
    words = query.lower().split()
    expanded = [TECH_ACRONYMS.get(w, w) for w in words]
    return " ".join(expanded)


def filter_catalogue_by_keyword(query: str, books: List[Dict[str, Any]], top_k: int = 6) -> List[Dict[str, Any]]:
    """
    Stage 1: Multi-field relevance scoring engine.
    Matches expanded query tokens against Title, Author, Category, Keywords, and Summary.
    """
    expanded_query = expand_query_acronyms(query)
    tokens = [t for t in re.findall(r"\b\w{2,}\b", expanded_query.lower())]

    stop_words = {
        "the", "and", "for", "with", "book", "books", "need", "want", "recommend",
        "show", "give", "can", "you", "about", "some", "good", "best", "please",
        "find", "looking", "have", "read", "study"
    }
    keywords = [t for t in tokens if t not in stop_words]

    if not keywords:
        return books[:top_k]

    scored_books = []
    for book in books:
        score = 0
        title_lower = str(book.get("title", "")).lower()
        author_lower = str(book.get("author", "")).lower()
        genre_lower = str(book.get("genre_category", "")).lower()
        topics_lower = str(book.get("topic_keywords", "")).lower()
        summary_lower = str(book.get("brief_summary", "")).lower()

        for kw in keywords:
            if kw in title_lower:
                score += 6
            if kw in author_lower:
                score += 5
            if kw in topics_lower:
                score += 4
            if kw in genre_lower:
                score += 3
            if kw in summary_lower:
                score += 2

        if score > 0:
            scored_books.append((score, book))

    scored_books.sort(key=lambda x: x[0], reverse=True)

    if scored_books:
        return [b for _, b in scored_books[:top_k]]
    return books[:top_k]


def build_recommendation_prompt(student_query: str, matched_books: List[Dict[str, Any]]) -> str:
    """Prompt engineering for LLM to recommend and explain the top 3 books."""
    catalogue_summary = []
    for idx, b in enumerate(matched_books, 1):
        catalogue_summary.append(
            f"Candidate #{idx}:\n"
            f"- Book ID: {b.get('book_id')}\n"
            f"- Title: {b.get('title')}\n"
            f"- Author: {b.get('author')}\n"
            f"- Category: {b.get('genre_category')}\n"
            f"- Shelf Location: {b.get('shelf_location')}\n"
            f"- Available Copies: {b.get('available_copies')}\n"
            f"- Summary: {b.get('brief_summary')}\n"
        )
    candidate_str = "\n".join(catalogue_summary)

    return f"""You are the intelligent College Library Assistant Bot.
A student came to the desk with this query:
"{student_query}"

Here are the candidate books retrieved from the campus library catalogue:
{candidate_str}

=== INSTRUCTIONS ===
1. Select the top 3 most relevant books from the candidates for this student.
2. For each recommended book, provide:
   - Exactly why it fits their request (clear, encouraging pedagogical explanation).
   - The book's shelf location and available copies.
   - The ideal reading level (e.g. Beginner, Intermediate, Advanced / Exam Prep).
3. If fewer than 3 candidates are relevant, recommend the available ones and suggest a closely related topic.
4. Conclude with a helpful librarian tip or follow-up question.

Format your output strictly as a valid JSON object matching this schema:
{{
  "intro_message": "<Short, warm conversational greeting addressing the query>",
  "recommendations": [
    {{
      "book_id": "<Book ID>",
      "title": "<Title>",
      "author": "<Author>",
      "shelf_location": "<Shelf Location>",
      "available_copies": <Integer>,
      "reading_level": "<Beginner / Intermediate / Advanced>",
      "why_recommended": "<Clear 2-sentence rationale on why this book helps the student>"
    }}
  ],
  "librarian_tip": "<1 helpful tip, e.g. rack navigation, study strategy, or related subject>"
}}
"""


def mock_llm_recommend(student_query: str, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Offline rule-based fallback when no API key is provided."""
    recs = []
    for b in candidates[:3]:
        recs.append({
            "book_id": b.get("book_id", "BK-000"),
            "title": b.get("title", "Unknown"),
            "author": b.get("author", "Unknown"),
            "shelf_location": b.get("shelf_location", "Main Stacks"),
            "available_copies": int(b.get("available_copies", 1)),
            "reading_level": "Recommended Study",
            "why_recommended": f"Directly covers topics related to your query. {b.get('brief_summary', '')}"
        })

    return {
        "intro_message": f"Hello! Here are the top 3 books from our library catalogue matching your search:",
        "recommendations": recs,
        "librarian_tip": "You can locate these books immediately using their respective Rack numbers, or reserve a copy at the circulation counter."
    }


import ssl

def get_ssl_context():
    """Create SSL context with fallback for macOS certificate stores."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        try:
            return ssl.create_default_context()
        except Exception:
            return ssl._create_unverified_context()


def fetch_available_models(api_key: str) -> List[str]:
    """Queries ModelService.ListModels to get exact models supported by this specific API key."""
    clean_key = api_key.strip()
    if not clean_key:
        return []
    
    ctx = get_ssl_context()
    for ver in ["v1beta", "v1"]:
        url = f"https://generativelanguage.googleapis.com/{ver}/models?key={clean_key}"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = []
                for m in data.get("models", []):
                    methods = m.get("supportedGenerationMethods", [])
                    if "generateContent" in methods:
                        name = m.get("name", "").replace("models/", "")
                        if name:
                            models.append(name)
                if models:
                    return models
        except Exception:
            continue
    return []


def call_gemini_llm(api_key: str, model_name: str, prompt: str) -> Dict[str, Any]:
    """Calls Gemini using official google-genai SDK with automatic gemini-3.8-flash fallback."""
    clean_key = api_key.strip()
    clean_model = model_name.strip()
    if clean_model.startswith("models/"):
        clean_model = clean_model.replace("models/", "")

    models_to_try = [clean_model]
    if "gemini-3.8-flash" not in models_to_try:
        models_to_try.append("gemini-3.8-flash")

    sdk_err_msg = ""
    # Primary Method: Official Google GenAI SDK (Native for Gemini 3.8 / 2.5)
    try:
        from google import genai
        client = genai.Client(api_key=clean_key)
        for m in models_to_try:
            try:
                response = client.models.generate_content(
                    model=m,
                    contents=prompt,
                )
                clean_text = response.text.strip()
                if clean_text.startswith("```"):
                    clean_text = re.sub(r"^```(?:json)?\s*", "", clean_text)
                    clean_text = re.sub(r"\s*```$", "", clean_text)
                return json.loads(clean_text)
            except Exception as m_err:
                sdk_err_msg = str(m_err)
                continue
    except Exception as e:
        sdk_err_msg = str(e)

    # Fallback Method: REST API with compatibility headers
    ctx = get_ssl_context()
    for m in models_to_try:
        for ver in ["v1beta", "v1"]:
            url = f"https://generativelanguage.googleapis.com/{ver}/models/{m}:generateContent?key={clean_key}"
            cfg = {"temperature": 0.2}
            if ver == "v1beta":
                cfg["responseMimeType"] = "application/json"

            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": cfg
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    text_out = data["candidates"][0]["content"]["parts"][0]["text"]
                    clean_text = text_out.strip()
                    if clean_text.startswith("```"):
                        clean_text = re.sub(r"^```(?:json)?\s*", "", clean_text)
                        clean_text = re.sub(r"\s*```$", "", clean_text)
                    return json.loads(clean_text)
            except Exception:
                continue

    raise RuntimeError(f"Connection failed: {sdk_err_msg}")


# ==========================================================
# SIDEBAR CONTROLS & LIVE STATS
# ==========================================================
with st.sidebar:
    st.markdown("### ⚙️ System Configuration")
    
    env_key = os.getenv("GEMINI_API_KEY", "")
    api_key = st.text_input(
        "Gemini API Key",
        value=env_key,
        type="password",
        help="Paste your free Gemini key from Google AI Studio. Can also be saved in .env."
    )

    if "available_models" not in st.session_state or "gemini-3.8-flash" not in st.session_state["available_models"]:
        st.session_state["available_models"] = [
            "gemini-3.8-flash",
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-2.0-flash",
            "gemini-1.5-flash"
        ]

    model_option = st.selectbox(
        "LLM Model",
        options=st.session_state["available_models"],
        index=0
    )

    if "api_test_status" not in st.session_state:
        st.session_state["api_test_status"] = None

    if st.button("🔌 Test API Connection", use_container_width=True):
        if not api_key.strip():
            st.session_state["api_test_status"] = ("error", "Please paste a Gemini API key first.")
        else:
            with st.spinner(f"Testing connection to {model_option}..."):
                try:
                    test_out = call_gemini_llm(api_key, model_option, "Respond with valid JSON: {\"status\": \"ok\", \"message\": \"connection successful\"}")
                    st.session_state["api_test_status"] = ("success", f"Connected to {model_option} successfully! Live GenAI is ready.")
                except Exception as t_err:
                    err_msg = str(t_err)
                    st.session_state["api_test_status"] = ("error", f"Connection test failed for {model_option}:\n\n`{err_msg}`")

    if st.session_state["api_test_status"]:
        s_type, s_msg = st.session_state["api_test_status"]
        if s_type == "success":
            st.success(s_msg)
        elif s_type == "info":
            st.info(s_msg)
        else:
            st.error(s_msg)

    use_mock = st.checkbox(
        "Offline Demo Mode (No API required)",
        value=False if api_key else True,
        help="Enable to test the entire application and UI without using external API quota."
    )

    # Status Pill
    if not use_mock and api_key:
        st.success("🟢 API Connected & Ready")
    else:
        st.info("⚪ Offline Demo Mode Active")

    st.markdown("---")
    st.markdown("### 📊 Inventory Summary")

    total_books = len(st.session_state["catalogue"])
    total_copies = sum(int(b.get("available_copies", 0)) for b in st.session_state["catalogue"])
    unique_categories = len(set(b.get("genre_category", "") for b in st.session_state["catalogue"]))

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{total_books}</div><div class="stat-label">Titles</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{total_copies}</div><div class="stat-label">Available Copies</div></div>', unsafe_allow_html=True)

    if st.session_state["borrowed_books"]:
        st.caption(f"📌 **Your Reserved Books:** {len(st.session_state['borrowed_books'])}")

    st.markdown("---")
    if st.button("🗑️ Reset Chat History", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #64748B; text-align: center; margin-top: 15px;">
            <strong>Roll No: 15</strong> | Problem Statement 15<br/>
            Final Year Mini Project Evaluation
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# MAIN HERO SECTION
# ==========================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">📚 Campus Library Assistant</div>
    <div class="hero-subtitle">
        Find the right textbooks, syllabus reference monographs, and interview preparation guides using conversational AI.
    </div>
    <div>
        <span class="pill-tag">🎯 Roll No. 15</span>
        <span class="pill-tag">🤖 Google Gemini 3.8 Flash</span>
        <span class="pill-tag">⚡ Two-Stage Retrieval</span>
        <span class="pill-tag">📍 Physical Shelf Locator</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# TAB NAVIGATION
# ==========================================================
tab_chat, tab_browse = st.tabs([
    "💬 AI Librarian Chat",
    "🔍 Catalogue Explorer"
])

# ----------------------------------------------------------
# TAB 1: AI LIBRARIAN CHAT
# ----------------------------------------------------------
with tab_chat:
    st.write("**💡 Frequently Asked Academic Queries:**")
    quick_cols = st.columns(5)
    quick_prompts = [
        ("🐍 Python for Beginners", "I am a first-year student looking for a beginner Python book with practical examples."),
        ("🤖 AI (Russell & Norvig)", "Can you find the textbook on Artificial Intelligence written by Stuart Russell and Peter Norvig?"),
        ("🗄️ DBMS & Normalization", "I need a reference book for Database Management Systems and SQL normalization for exams."),
        ("⚡ Placement & Algorithms", "I have campus placement coding rounds in two months. Which books should I read for algorithms?"),
        ("☁️ Docker & Kubernetes", "Recommend books for learning Docker containerization and Kubernetes orchestration.")
    ]

    selected_query = None
    for i, (label, prompt_text) in enumerate(quick_prompts):
        if quick_cols[i].button(label, key=f"quick_btn_{i}", use_container_width=True):
            selected_query = prompt_text

    # Initialize chat history
    if "messages" not in st.session_state or not st.session_state["messages"]:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "👋 **Hello! I am your Campus Library Assistant.** Ask me about any topic, author, course code, or exam preparation need (e.g., *'Best books for Python'*, *'Database normalization'*, or *'Competitive programming'*)."
            }
        ]

    # Render Chat History
    for msg_idx, msg in enumerate(st.session_state["messages"]):
        with st.chat_message(msg["role"]):
            if isinstance(msg["content"], dict):
                data = msg["content"]
                st.write(data.get("intro_message", ""))
                
                for rec_idx, rec in enumerate(data.get("recommendations", [])):
                    book_id = rec.get("book_id", "BK-000")
                    # Check current copies in session
                    current_book = next((b for b in st.session_state["catalogue"] if b.get("book_id") == book_id), None)
                    copies_left = current_book.get("available_copies", rec.get("available_copies", 0)) if current_book else rec.get("available_copies", 0)

                    st.markdown(f"""
                    <div class="recommendation-card">
                        <div class="card-title">📖 {rec.get('title')}</div>
                        <div class="card-meta"><strong>Author:</strong> {rec.get('author')} &bull; <strong>Book ID:</strong> {book_id}</div>
                        <div>
                            <span class="badge badge-id">ID: {book_id}</span>
                            <span class="badge badge-shelf">📍 {rec.get('shelf_location')}</span>
                            <span class="badge badge-copies">🟢 {copies_left} Copies In Stacks</span>
                            <span class="badge badge-level">🎯 Level: {rec.get('reading_level')}</span>
                        </div>
                        <div class="rationale-box">
                            <strong>Why Recommended:</strong> {rec.get('why_recommended')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                if data.get("librarian_tip"):
                    st.markdown(f"""
                    <div class="librarian-tip-box">
                        💡 <strong>Librarian Advice:</strong>&nbsp;{data.get('librarian_tip')}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])

    # User Chat Input
    user_input = st.chat_input("Ask about books, authors, semester exams, or coding interview prep...")
    active_prompt = selected_query or user_input

    if active_prompt:
        st.session_state["messages"].append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching catalogue and synthesizing recommendations..."):
                # Step 1: Pre-filter candidate books
                candidates = filter_catalogue_by_keyword(active_prompt, st.session_state["catalogue"], top_k=6)

                # Step 2: Call LLM / Fallback
                try:
                    if use_mock or not api_key or not api_key.strip():
                        result = mock_llm_recommend(active_prompt, candidates)
                    else:
                        try:
                            prompt_str = build_recommendation_prompt(active_prompt, candidates)
                            result = call_gemini_llm(api_key.strip(), model_option, prompt_str)
                        except Exception as api_err:
                            st.warning(f"⚠️ Live Gemini API could not be reached: `{api_err}`")
                            st.info("ℹ️ Showing instant catalogue recommendations below using the local engine.")
                            result = mock_llm_recommend(active_prompt, candidates)

                    # Display Response Cards
                    st.write(result.get("intro_message", ""))
                    for rec in result.get("recommendations", []):
                        b_id = rec.get("book_id", "BK-000")
                        c_book = next((b for b in st.session_state["catalogue"] if b.get("book_id") == b_id), None)
                        copies_avail = c_book.get("available_copies", rec.get("available_copies", 0)) if c_book else rec.get("available_copies", 0)

                        st.markdown(f"""
                        <div class="recommendation-card">
                            <div class="card-title">📖 {rec.get('title')}</div>
                            <div class="card-meta"><strong>Author:</strong> {rec.get('author')} &bull; <strong>Book ID:</strong> {b_id}</div>
                            <div>
                                <span class="badge badge-id">ID: {b_id}</span>
                                <span class="badge badge-shelf">📍 {rec.get('shelf_location')}</span>
                                <span class="badge badge-copies">🟢 {copies_avail} Copies In Stacks</span>
                                <span class="badge badge-level">🎯 Level: {rec.get('reading_level')}</span>
                            </div>
                            <div class="rationale-box">
                                <strong>Why Recommended:</strong> {rec.get('why_recommended')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    if result.get("librarian_tip"):
                        st.markdown(f"""
                        <div class="librarian-tip-box">
                            💡 <strong>Librarian Advice:</strong>&nbsp;{result.get('librarian_tip')}
                        </div>
                        """, unsafe_allow_html=True)

                    st.session_state["messages"].append({"role": "assistant", "content": result})

                except Exception as err:
                    err_text = f"⚠️ Recommendation Error: {str(err)}"
                    st.error(err_text)
                    st.session_state["messages"].append({"role": "assistant", "content": err_text})

    # Download Report Button
    if len(st.session_state["messages"]) > 1:
        st.markdown("---")
        chat_export = json.dumps(st.session_state["messages"], indent=2)
        st.download_button(
            label="📥 Export Chat History (JSON)",
            data=chat_export,
            file_name="library_chat_session.json",
            mime="application/json"
        )


# ----------------------------------------------------------
# TAB 2: CATALOGUE EXPLORER
# ----------------------------------------------------------
with tab_browse:
    st.subheader("Campus Library Book Repository")
    st.caption("Live view of all academic holdings with real-time stock levels.")

    df_catalogue = pd.DataFrame(st.session_state["catalogue"])

    col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
    with col_s1:
        search_kw = st.text_input("🔍 Search by title, author, or keywords:", "")
    with col_s2:
        genre_list = ["All Categories"] + sorted(list(df_catalogue["genre_category"].unique()))
        selected_genre = st.selectbox("Filter Category:", genre_list)
    with col_s3:
        only_in_stock = st.checkbox("Show Only In-Stock Copies", value=False)

    # Filter DataFrame
    filtered_df = df_catalogue.copy()
    if search_kw:
        mask = filtered_df.apply(lambda row: search_kw.lower() in str(row.values).lower(), axis=1)
        filtered_df = filtered_df[mask]
    if selected_genre != "All Categories":
        filtered_df = filtered_df[filtered_df["genre_category"] == selected_genre]
    if only_in_stock:
        filtered_df = filtered_df[pd.to_numeric(filtered_df["available_copies"], errors="coerce") > 0]

    st.dataframe(
        filtered_df[[
            "book_id", "title", "author", "genre_category",
            "edition_year", "shelf_location", "available_copies"
        ]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.subheader("📚 Book Reservation Desk")
    st.caption("Simulate borrowing a copy from the library in real-time.")

    col_borrow_select, col_borrow_action = st.columns([3, 1])
    with col_borrow_select:
        book_options = {f"{b['book_id']}: {b['title']} (Rack: {b['shelf_location']})": b['book_id'] for b in st.session_state["catalogue"]}
        selected_book_label = st.selectbox("Select book to reserve/checkout:", list(book_options.keys()))
        selected_book_id = book_options[selected_book_label]
    with col_borrow_action:
        st.write("")
        st.write("")
        if st.button("🔖 Borrow 1 Copy", use_container_width=True):
            for b in st.session_state["catalogue"]:
                if b["book_id"] == selected_book_id:
                    current = int(b.get("available_copies", 0))
                    if current > 0:
                        b["available_copies"] = current - 1
                        st.session_state["borrowed_books"].append(b["title"])
                        st.success(f"Reserved '{b['title']}'. Remaining copies: {b['available_copies']}")
                        st.rerun()
                    else:
                        st.warning("Sorry, no copies currently available in the stacks!")



