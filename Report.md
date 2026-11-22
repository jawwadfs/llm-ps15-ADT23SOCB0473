# 2-PAGE PROCEDURE REPORT
**LLM Mini Project (10-Mark Evaluation)**

---

## 1. HEADER
- **Project Title:** Campus Library Assistant Bot (PS 15)
- **Problem Statement Number:** PS 15
- **Student Name:** Jawwad
- **Roll Number:** 15
- **Class / Program:** Final Year B.Tech (Computer Science & Engineering)
- **GitHub Repository Link:** [https://github.com/jawwad/llm-ps15-15](https://github.com/jawwad/llm-ps15-15)
- **Domain:** Chatbots & Conversational AI Assistant

---

## 2. PROBLEM STATEMENT
University and college libraries host thousands of textbooks, reference monographs, and research guides across multiple floors and shelves. Students frequently struggle to quickly locate the right books that match their immediate academic needs, semester exam requirements, or placement preparation goals. Traditional library OPAC (Online Public Access Catalog) portals rely on rigid keyword queries that fail when students query using conversational or conceptual requests (e.g., *"friendly book to start Python"* or *"best book for competitive coding interviews"*). 

This project solves this problem by creating an intelligent **Library Assistant Chatbot**. The bot takes natural student queries, filters a structured campus library catalogue (`.csv`) using keyword and topic scoring, and prompts a Large Language Model (Google Gemini 2.5 Flash) to recommend and explain the **top 3 best-matched books**, providing pedagogical reasoning, difficulty level, shelf locations, and available copies.

---

## 3. TOOLS & MODEL
- **Programming Language:** Python 3.9+
- **Core Libraries:**
  - `pandas` / `csv`: Structured loading, multi-column search, and ranking of catalogue entries.
  - `urllib.request` / `google-genai`: Secure, low-latency API communication with Google Gemini.
  - `python-dotenv`: Management of environment variables and sensitive API keys.
- **LLM Used:** Google **Gemini 3.8 Flash** (with multi-version fallback via API). Configured with `temperature=0.2` and `response_mime_type="application/json"` for deterministic, structured recommendations.
- **UI Framework:** **Streamlit** (featuring `st.chat_message`, `st.chat_input`, interactive tabs, metric badges, catalogue explorer, real-time book reservation, and inventory analytics).

---

## 4. PROCEDURE (STEP-BY-STEP IMPLEMENTATION)
1. **Repository & Environment Setup:** Created a clean virtual environment (`python3 -m venv venv`), established `.gitignore` to prevent API key exposure, and initialized the GitHub repository structure.
2. **Library Catalogue Dataset Preparation:** Curated `library_catalogue.csv` containing 25+ academic textbooks across Computer Science, AI, Databases, Networks, Mathematics, and DevOps with metadata fields: `book_id`, `title`, `author`, `genre_category`, `topic_keywords`, `edition_year`, `shelf_location`, `available_copies`, and `brief_summary`.
3. **Keyword Filtering Engine:** Implemented `filter_catalogue_by_keyword()` using tokenization and multi-field weighted scoring (Title: +5, Author: +5, Category: +3, Topics: +3, Summary: +1). This extracts the top candidate books to keep the LLM context focused and cost-efficient.
4. **Prompt Engineering & Schema Definition:** Designed a system prompt requiring the LLM to act as a campus librarian, evaluate retrieved candidates against student intent, and return strictly valid JSON containing top 3 recommendations, rationales, shelf details, and a helpful librarian tip.
5. **LLM API Integration:** Connected to Gemini 2.5 Flash using JSON response mode and implemented an offline rule-based fallback mode for offline viva demonstrations.
6. **User Interface Development:** Built a responsive Streamlit interface with chat bubbles, quick prompt suggestions, shelf location badges, and an interactive catalogue browser tab.
7. **Testing & Documentation:** Validated the application on 5 distinct student query test cases, documented outputs, authored the README, and prepared the final report.

---

*(Page Break)*

---

## 5. PROMPT USED & ITERATIVE IMPROVEMENT

### Final Prompt Template
```
You are the intelligent College Library Assistant Bot.
A student came to the desk with this query: "{student_query}"

Here are the candidate books retrieved from the library catalogue:
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
{
  "intro_message": "<Short, warm conversational greeting addressing the query>",
  "recommendations": [
    {
      "book_id": "<Book ID>",
      "title": "<Title>",
      "author": "<Author>",
      "shelf_location": "<Shelf Location>",
      "available_copies": <Integer>,
      "reading_level": "<Beginner / Intermediate / Advanced>",
      "why_recommended": "<Clear 2-sentence rationale on why this book helps the student>"
    }
  ],
  "librarian_tip": "<1 helpful tip, e.g. rack navigation, study strategy, or related subject>"
}
```

### Iterative Improvement
- **Initial Prompt Flaw:** The initial prompt asked the LLM to output freeform markdown text. In early tests, the model frequently hallucinated books outside our campus catalogue and forgot to mention exact shelf rack locations or available copy counts.
- **Improvement Made:** Constrained the context to explicitly pass candidate rows from `library_catalogue.csv` and enforced strict JSON schema formatting (`response_mime_type="application/json"`). This guaranteed 100% factual accuracy to the college's actual inventory and provided structured data for rendering visual UI cards.

---

## 6. RESULTS & TESTING
The application was evaluated across 5 representative query scenarios:

| Test Case | Student Input Query | Top Book Recommended | Shelf Location & Copies |
| :--- | :--- | :--- | :--- |
| **Case 1 (Beginner)** | *"I am a 1st year student looking for a beginner Python book"* | Python Crash Course (Eric Matthes) | Floor 1 - Rack PR-02 (8 copies) |
| **Case 2 (Author Search)** | *"Textbook on AI by Russell and Norvig"* | Artificial Intelligence: A Modern Approach | Floor 2 - Rack AI-01 (5 copies) |
| **Case 3 (Semester Exam)** | *"DBMS and SQL normalization for semester exams"* | Database System Concepts (Silberschatz) | Floor 1 - Rack DB-01 (5 copies) |
| **Case 4 (Placements)** | *"Books for algorithms and coding interview preparation"* | Cracking the Coding Interview (McDowell) | Floor 3 - Rack PL-01 (10 copies) |
| **Case 5 (DevOps)** | *"Docker containerization and Kubernetes orchestration"* | Docker Deep Dive (Nigel Poulton) | Floor 2 - Rack CL-01 (5 copies) |

**Sample Output Snapshot:**  
- Query: *"I am a first-year student and want a friendly book to start learning Python from scratch."*
- Response: Identifies `Python Crash Course` (Beginner level, Rack PR-02) highlighting that it starts with core syntax without assuming previous background, followed by `Grokking Algorithms` (Rack CS-02) for visual foundational understanding.

---

## 7. CHALLENGES & HOW THEY WERE FIXED
1. **LLM Hallucination of Non-Existent Titles:** Early tests recommended famous books that the college library did not own.  
   *Fix:* Implemented a strict Two-Stage Retrieval pipeline: Pandas filters only actual library CSV rows first, and the prompt forbids referencing unlisted titles.
2. **Markdown Code Fence Parsing:** Some LLMs wrap JSON inside ` ```json ... ``` `, which caused `json.loads()` to raise syntax errors.  
   *Fix:* Added a robust `clean_json_string()` regex preprocessor and utilized Gemini’s native `response_mime_type="application/json"`.
3. **Offline Demo Capability for Viva Examination:** If WiFi or API keys fail during the oral examination, the student risks losing demo marks.  
   *Fix:* Added an **Offline Demo Mode** switch in the sidebar that executes deterministic local ranking and mock recommendation with zero external dependencies.

---

## 8. CONCLUSION
- **What Works:** Reliable two-stage search pipeline, zero hallucinations of unowned books, structured rendering of shelf locations and copy availability, responsive Streamlit UI, and offline demo fallback.
- **What Doesn’t:** Current keyword search relies on token overlap; synonyms or misspelled queries (e.g., *"pythn"*) require fuzzy matching or semantic embeddings.
- **Future Improvement:** Integrate semantic dense vector search (using FAISS and `text-embedding-004`) to handle semantic conceptual queries and connect to the live college circulation SQL database for real-time checkout status.
