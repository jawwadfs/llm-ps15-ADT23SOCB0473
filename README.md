# 📚 Campus Library Assistant Bot (PS 15)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/LLM-Gemini%203.8%20Flash-green.svg)](https://aistudio.google.com/)

An intelligent conversational library assistant mini-project designed for engineering students. The bot connects students to relevant academic books, reference guides, and exam preparation material from the campus library catalogue by understanding their learning goals, topics, or favorite authors.

---

## 🎯 Problem Statement (Roll No: 15)
> **Problem Statement:** Students can’t easily find books. Build a chatbot that recommends books from a library catalogue CSV by topic or author.  
> **Approach:** Load catalogue CSV with pandas → filter by keyword first → send the matching rows to the LLM to recommend and explain the top 3 books.

---

## 🏗️ Architecture & Pipeline Flow

```
+---------------------------+
| Student Natural Query     | ("I need books to learn Python and data structures")
+-------------+-------------+
              |
              v
+---------------------------+
| Step 1: Acronyms & Tokens | (Expands 'dsa' -> 'data structures algorithms', etc.)
+-------------+-------------+
              |
              v
+---------------------------+
| Step 2: Pandas Filter     | (Multi-field weighted match: Title, Author, Genre & Topics)
+-------------+-------------+
              | Retrieves Top 6 Candidate Rows from library_catalogue.csv
              v
+---------------------------+
| Step 3: Prompt Engine     | (Formats Candidate Metadata + Evaluation Rules into JSON Schema)
+-------------+-------------+
              |
              v
+---------------------------+
| Step 4: Gemini 3.8 Flash  | (Ranks top 3, writes custom explanations, shelf locations & tips)
+-------------+-------------+
              | Structured JSON Response
              v
+---------------------------+
| Step 5: Streamlit UI      | (Renders Interactive Chat Cards, Shelf Badges, Live Reservation & Analytics)
+---------------------------+
```

---

## ✨ Advanced Features

- **Multi-Field Weighted Filter:** Pre-filters the library repository using pandas across `title`, `author`, `genre_category`, `topic_keywords`, and `brief_summary`.
- **Acronym Normalization Engine:** Automatically expands student shorthand terms (`dsa`, `dbms`, `os`, `ai`, `ml`, `k8s`, `clrs`) for improved discovery.
- **Intelligent LLM Recommendations:** Uses Google Gemini 3.8 Flash (with multi-version fallback) to analyze the student's background and select the top 3 best-suited books.
- **Pedagogical Rationale:** Explains *why* each book was chosen, including the recommended reading level (Beginner / Intermediate / Advanced).
- **Physical Rack Navigation:** Displays shelf location (e.g. `Floor 2 - Rack CS-01`) and live available copy counts.
- **Interactive Book Reservation Desk:** Allows students to simulate borrowing a physical book, decrementing available stock in real-time.
- **Visual Analytics Dashboard:** Visualizes library book distribution across subject categories and physical copy stock levels.
- **Offline / Viva Demo Mode:** Includes a built-in offline mode that functions seamlessly even without an API key or internet access.
- **Full Catalogue Browser:** Interactive searchable table allowing students and faculty to browse all library books directly.
- **Pedagogical Rationale:** Explains *why* each book was chosen, including the recommended reading level (Beginner / Intermediate / Advanced).
- **Physical Rack Navigation:** Displays shelf location (e.g. `Floor 2 - Rack CS-01`) and live available copy counts.
- **Offline / Viva Demo Mode:** Includes a built-in offline mode that functions seamlessly even without an API key or internet access.
- **Full Catalogue Browser:** Interactive searchable table allowing students and faculty to browse all library books directly.

---

## 📁 Project Directory Layout

```
llm-ps15-15/
├── app.py                      # Main Streamlit Chatbot Application
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git exclusions (.env, venv, pycache)
├── README.md                   # Project documentation
├── github_link.txt             # Repository link for submission
├── data/
│   └── library_catalogue.csv   # College library catalog dataset
├── sample_test_runs.md         # Documented 5 sample test cases & outputs
├── generate_report.py          # Script to generate 2-page procedure report PDF
└── Report.pdf                  # 2-Page Procedure Report (A4, 12pt)
```

---

## 🚀 Quickstart & Setup Guide

### 1. Clone or Extract the Project
```bash
git clone https://github.com/<your-username>/llm-ps15-15.git
cd llm-ps15-15
```

### 2. Create and Activate a Virtual Environment
```bash
# macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API Key (Optional)
You can obtain a free API key from [Google AI Studio](https://aistudio.google.com/).
Create a `.env` file in the root directory:
```bash
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```
*(Alternatively, enter your API key directly in the Streamlit sidebar password box, or toggle "Offline Demo Mode".)*

### 5. Launch the Application
```bash
streamlit run app.py
```
The application will open automatically in your browser at `http://localhost:8501`.

---

## 🧪 Sample Test Inputs for Evaluation

1. **Beginner Python:** `"I am a first-year student and want a friendly book to start learning Python from scratch."`
2. **Author Specific:** `"Can you find the textbook on Artificial Intelligence written by Stuart Russell and Peter Norvig?"`
3. **Core Exams:** `"I need a good reference book for Database Management Systems and SQL normalization for semester exams."`
4. **Placement Prep:** `"I have campus placement coding rounds in two months. Which books should I read for algorithms?"`
5. **DevOps & Cloud:** `"Recommend books for learning Docker containerization and Kubernetes orchestration."`

---

## 📋 Evaluation Criteria Mapping (10 Marks)

| Component | Marks | Implementation in Project |
| :--- | :---: | :--- |
| **Problem understanding & prompt design** | **2** | Structured ATS/Librarian prompt enforcing valid JSON schema, level tagging, and shelf guidance. |
| **Working implementation (core feature)** | **4** | Two-stage pipeline: Pandas keyword retrieval followed by Gemini LLM reasoning. |
| **Simple UI / demo** | **2** | Streamlit chat UI with styled recommendation cards, quick prompts, and catalogue search. |
| **Report, sample inputs & viva** | **2** | Complete 2-page procedure report, 5 sample test cases, and offline demo fallback. |

---

## 👤 Author
- **Roll Number:** 15
- **Problem Statement:** PS 15 - Library Assistant Bot
- **Course / Degree:** Final Year B.Tech / B.E. (Computer Science & Engineering)
