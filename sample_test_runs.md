# Sample Test Queries & LLM Outputs (PS 15: Library Assistant Bot)

Tested with: **Google Gemini 2.5 Flash**  
Evaluation Criterion: 5 diverse student queries testing topic search, author queries, level matching, and location lookup.

---

### Test Case 1: Beginner Programming Query
- **User Input:**  
  `"I am a first-year student and want a friendly book to start learning Python from scratch."`
- **Filter Step (Keyword search):**  
  Matched keywords: `python`, `beginners`, `programming`  
  Retrieved candidate rows: `BK-102 (Python Crash Course)`, `BK-103 (Fluent Python)`, `BK-124 (Grokking Algorithms)`
- **LLM Output (Top 3 Recommendations):**
  1. **Python Crash Course** (Author: Eric Matthes)
     - *Reading Level:* Beginner
     - *Shelf Location:* Floor 1 - Rack PR-02 | Available Copies: 8
     - *Why Recommended:* Perfectly suited for first-year beginners; guides you from basic syntax to simple games and data visualization projects without assuming prior coding background.
  2. **Grokking Algorithms** (Author: Aditya Bhargava)
     - *Reading Level:* Beginner to Intermediate
     - *Shelf Location:* Floor 2 - Rack CS-02 | Available Copies: 9
     - *Why Recommended:* Features friendly visual illustrations that help novice programmers visualize basic data structures and algorithms while learning Python.
  3. **Fluent Python** (Author: Luciano Ramalho)
     - *Reading Level:* Intermediate to Advanced
     - *Shelf Location:* Floor 1 - Rack PR-03 | Available Copies: 4
     - *Why Recommended:* Recommended as your next step once you master the fundamentals in Python Crash Course.
  - *Librarian Tip:* Start with Chapters 1–8 of Python Crash Course and practice coding in VS Code or Jupyter Notebook.

---

### Test Case 2: Author-Specific AI Query
- **User Input:**  
  `"Can you find the textbook on Artificial Intelligence written by Stuart Russell and Peter Norvig?"`
- **Filter Step (Author & Title search):**  
  Matched keywords: `stuart russell`, `peter norvig`, `artificial intelligence`  
  Retrieved candidate rows: `BK-104 (Artificial Intelligence: A Modern Approach)`, `BK-105 (Deep Learning)`, `BK-106 (Hands-On ML)`
- **LLM Output (Top 3 Recommendations):**
  1. **Artificial Intelligence: A Modern Approach** (Author: Stuart Russell & Peter Norvig)
     - *Reading Level:* Comprehensive / Academic Reference
     - *Shelf Location:* Floor 2 - Rack AI-01 | Available Copies: 5
     - *Why Recommended:* Direct match for your requested authors; this is the universally recognized gold-standard textbook covering intelligent agents, state-space search, logic, and probabilistic reasoning.
  2. **Deep Learning** (Author: Ian Goodfellow, Yoshua Bengio, Aaron Courville)
     - *Reading Level:* Advanced
     - *Shelf Location:* Floor 2 - Rack AI-02 | Available Copies: 3
     - *Why Recommended:* Excellent companion reading for deep learning chapters in Russell & Norvig.
  3. **Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow** (Author: Aurélien Géron)
     - *Reading Level:* Practical / Applied
     - *Shelf Location:* Floor 2 - Rack DS-01 | Available Copies: 7
     - *Why Recommended:* Complements theoretical AI foundations with hands-on Python code implementation.
  - *Librarian Tip:* Copies of Russell & Norvig are located in Rack AI-01; please check out with Book ID BK-104.

---

### Test Case 3: Semester Exam / Core Coursework
- **User Input:**  
  `"I need a good reference book for Database Management Systems and SQL normalization for my semester exams."`
- **Filter Step (Topic keywords search):**  
  Matched keywords: `database`, `dbms`, `sql`, `normalization`  
  Retrieved candidate rows: `BK-107 (Database System Concepts)`, `BK-115 (Learning SQL)`, `BK-108 (Designing Data-Intensive Applications)`
- **LLM Output (Top 3 Recommendations):**
  1. **Database System Concepts** (Author: Abraham Silberschatz, Henry F. Korth, S. Sudarshan)
     - *Reading Level:* University Core Curriculum
     - *Shelf Location:* Floor 1 - Rack DB-01 | Available Copies: 5
     - *Why Recommended:* Directly follows standard university syllabus for B.Tech/B.E.; covers 1NF, 2NF, 3NF, BCNF normalization proofs, relational algebra, and ACID transaction mechanics in depth.
  2. **Learning SQL** (Author: Alan Beaulieu)
     - *Reading Level:* Beginner to Intermediate
     - *Shelf Location:* Floor 1 - Rack DB-02 | Available Copies: 6
     - *Why Recommended:* Great for mastering practical SQL queries, multi-table joins, subqueries, and group-by aggregations for database lab exams.
  3. **Designing Data-Intensive Applications** (Author: Martin Kleppmann)
     - *Reading Level:* Advanced / Systems
     - *Shelf Location:* Floor 2 - Rack CS-05 | Available Copies: 6
     - *Why Recommended:* Helpful for advanced semester questions regarding database indexing (B-Trees vs LSM-Trees) and replication.
  - *Librarian Tip:* For exam prep, review Chapter 7 (Relational Database Design) in Silberschatz & Korth.

---

### Test Case 4: Career & Placement Interview Preparation
- **User Input:**  
  `"I have campus placement coding rounds in two months. Which books should I read for algorithms and interview problems?"`
- **Filter Step:**  
  Matched keywords: `interview`, `algorithms`, `coding`, `placement`  
  Retrieved candidate rows: `BK-113 (Cracking the Coding Interview)`, `BK-101 (Introduction to Algorithms)`, `BK-114 (Competitive Programming 4)`
- **LLM Output (Top 3 Recommendations):**
  1. **Cracking the Coding Interview** (Author: Gayle Laakmann McDowell)
     - *Reading Level:* Placement / Interview Prep
     - *Shelf Location:* Floor 3 - Rack PL-01 | Available Copies: 10
     - *Why Recommended:* Specifically structured for tech interviews with 189 handpicked coding problems, Big-O breakdown, and optimal solution walks.
  2. **Introduction to Algorithms (CLRS)** (Author: Cormen, Leiserson, Rivest, Stein)
     - *Reading Level:* Rigorous / Academic
     - *Shelf Location:* Floor 2 - Rack CS-01 | Available Copies: 6
     - *Why Recommended:* Unbeatable theoretical foundation for deep understanding of dynamic programming, graph algorithms (Dijkstra, Bellman-Ford), and asymptotic bounds.
  3. **Competitive Programming 4** (Author: Steven Halim & Felix Halim)
     - *Reading Level:* Advanced Problem Solving
     - *Shelf Location:* Floor 3 - Rack PL-02 | Available Copies: 4
     - *Why Recommended:* Accelerates speed and pattern recognition for online assessment rounds (OA) on HackerRank and LeetCode.
  - *Librarian Tip:* Solve problems on paper or whiteboard first before typing, as recommended in Chapter 3 of CTCI.

---

### Test Case 5: DevOps & Cloud Infrastructure
- **User Input:**  
  `"Recommend books for learning Docker containerization and Kubernetes orchestration."`
- **Filter Step:**  
  Matched keywords: `docker`, `kubernetes`, `cloud`, `containers`  
  Retrieved candidate rows: `BK-116 (Docker Deep Dive)`, `BK-117 (Kubernetes Up & Running)`, `BK-108 (Designing Data-Intensive Applications)`
- **LLM Output (Top 3 Recommendations):**
  1. **Docker Deep Dive** (Author: Nigel Poulton)
     - *Reading Level:* Beginner to Intermediate
     - *Shelf Location:* Floor 2 - Rack CL-01 | Available Copies: 5
     - *Why Recommended:* Crystal-clear breakdown of container architecture, Dockerfiles, images, layers, and networking without overwhelming jargon.
  2. **Kubernetes Up & Running** (Author: Brendan Burns, Joe Beda, Kelsey Hightower)
     - *Reading Level:* Intermediate to Production
     - *Shelf Location:* Floor 2 - Rack CL-02 | Available Copies: 3
     - *Why Recommended:* Written directly by the co-creators of Kubernetes; explains Pods, Deployments, Services, and Ingress with practical YAML examples.
  3. **Designing Data-Intensive Applications** (Author: Martin Kleppmann)
     - *Reading Level:* Architecture / Cloud Systems
     - *Shelf Location:* Floor 2 - Rack CS-05 | Available Copies: 6
     - *Why Recommended:* Provides the big-picture distributed systems rationale behind modern containerized cloud microservices.
  - *Librarian Tip:* Read Docker Deep Dive first before starting Kubernetes Up & Running for a smooth learning curve.
