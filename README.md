# 🤖 Self Reflective RAG Chatbot

A Retrieval-Augmented Generation (RAG) assistant built with FastAPI, LangChain, FAISS, and LLMs (Vertex AI / Gemini).  
It allows users to query company documents and web sources with context-aware responses, strict grounding checks, and answer usefulness evaluation.

---

## 🛠️ Tech Stack

- **Language:** Python 3.13+
- **Backend:** FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Vector Store:** FAISS
- **LLM / AI:** Vertex AI Gemini (via `app/llm/llm_model.py`)
- **Workflow Engine:** LangGraph (`StateGraph`)
- **Logging:** Python logging via `logs.py`

---

## 📂 Project Structure
```
Self Reflective RAG
├── .env
├── .gitignore
├── .python-version
├── README.md
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── chat_router.py
│   │   ├── doc_router.py
│   │   ├── health_router.py
│   │   └── index_router.py
│   ├── config.py
│   ├── data
│   │   ├── Company_Policies.pdf
│   │   ├── Company_Profile.pdf
│   │   ├── Product_and_Pricing.pdf
│   │   └── context.txt
│   ├── embeddings
│   │   ├── __init__.py
│   │   └── vector_store.py
│   ├── graph
│   │   ├── __init__.py
│   │   ├── nodes.py
│   │   ├── prompts.py
│   │   ├── rag.py
│   │   └── routers.py
│   ├── llm
│   │   ├── __init__.py
│   │   └── llm_model.py
│   ├── main.py
│   └── models
│       ├── __init__.py
│       ├── schema.py
│       └── state.py
├── app.py
├── faiss_index
│   ├── index.faiss
│   └── index.pkl
├── frontend
│   ├── favicon.ico
│   ├── index.html
│   ├── script.js
│   └── style.css
├── logs.py
├── model_creds
│   └── ai-development-488417-f1cd2523b737.json
├── pyproject.toml
├── tree.py
├── tree.txt
├── uv.lock
└── workflow.png
```


---

## 🧠 How It Works

1. **Question Input:** User asks a question via frontend or API.
2. **Decide Retrieval:** LLM decides if external retrieval is needed (`decide_retrieval` node).
3. **Direct Answer Generation:** If retrieval is not needed, answer generated directly from LLM (`generate_direct`).
4. **Document Retrieval:** Relevant PDFs are searched using FAISS (`retrieve` node).
5. **Relevance Filtering:** LLM evaluates document relevance (`is_relevant`).
6. **Contextual Answer:** LLM generates answer from filtered documents (`generate_from_context`).
7. **Web Query (Optional):** If no relevant docs, question is rewritten for web search (`rewrite_query`) and answered (`web_search`).
8. **SUP Verification:** LLM checks if the answer is fully supported by context (`is_sup` node).
9. **Revision Loop:** Partially or unsupported answers are revised (`revise_answer`).
10. **USE Verification:** LLM checks if answer is useful to the user (`is_use` node).
11. **Chat History:** Conversation history updated for context and follow-ups (`update_history`).

Workflow visualization: `workflow.png`

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```
git clone https://github.com/lavisharma-25/Self_Reflective_RAG.git
cd your-repo
```

### 2️⃣ Install uv (if not already installed)
```
pip install uv
```

### 3️⃣ Initialize project environment
```
uv init       # Creates virtual environment and sets up project
uv sync       # Installs all dependencies automatically
```

### 4️⃣ Activate virtual environment
#### Linux / Mac:
```
source venv/bin/activate
```
#### Windows:
```
venv\Scripts\activate
```

### 5️⃣ Create .env file for credentials
```
GEMINI_API_KEY=""
SERVICE_ACCOUNT_FILE="model_creds/vertex_ai_credential.json"
LOCATION="global"
GEMINI_MODEL="gemini-2.5-pro"
EMBEDDING_MODEL="models/gemini-embedding-001"
TAVILY_API_KEY=""
PORT=8000
```

### 6️⃣ Run Project
```
python app.py
```

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

**Steps:**

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add feature"`
4. Push branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 👨‍💻 Author

**Lavish Sharma**  
- GitHub: [lavisharma-25](https://github.com/lavisharma-25)  
- Portfolio: [lavisharma-25.github.io](https://lavisharma-25.github.io/)