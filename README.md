# 🤖 Local AI Q&A System

A fully local document question-answering system that allows users to upload documents and ask questions about their content using **semantic search + a local Large Language Model (LLM)**.

The system retrieves relevant information from uploaded documents and generates answers using **Ollama + Qwen 2.5 3B**, without sending document data to external AI APIs.

## ✨ Features

* 📄 Upload **PDF, TXT, DOCX, and CSV** files
* 🔎 Semantic document search
* 🧠 Local AI-powered question answering
* 🤖 Uses **Qwen 2.5 3B** through Ollama
* ⚡ FAISS-based vector search
* 📊 Reliability score for generated answers
* 📚 Displays supporting evidence
* 🔐 Documents remain local
* 🌐 Works offline after the required models and dependencies are installed

## 🏗️ System Architecture

```text
                Uploaded Documents
                       │
                       ▼
              Document Processing
                       │
                       ▼
             Text Extraction
                       │
                       ▼
          SentenceTransformer Model
                       │
                       ▼
                FAISS Vector Store
                       │
                       ▼
                 User Question
                       │
                       ▼
              Semantic Retrieval
                       │
                       ▼
             Relevant Evidence
                       │
                       ▼
              Ollama + Qwen 2.5
                       │
                       ▼
                Final Answer
                       │
                       ▼
          Reliability + Evidence
```

## 🛠️ Technologies Used

| Technology           | Purpose                  |
| -------------------- | ------------------------ |
| Python               | Application development  |
| Streamlit            | Web interface            |
| FAISS                | Vector similarity search |
| SentenceTransformers | Text embeddings          |
| Ollama               | Local LLM runtime        |
| Qwen 2.5 3B          | Question answering       |
| PyPDF                | PDF text extraction      |
| python-docx          | DOCX processing          |
| Pandas               | CSV processing           |

## 📂 Project Structure

```text
local-ai-qa-mvp/
│
├── app.py
├── .gitignore
│
├── modules/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── reliability.py
│   └── vector_store.py
│
└── data/
    └── documents/
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Jenita2006/local-ai-qa-mvp.git
cd local-ai-qa-mvp
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install streamlit sentence-transformers faiss-cpu pypdf python-docx pandas requests
```

### 4. Install Ollama

Install Ollama on your system and make sure it is running.

Then download the Qwen model:

```bash
ollama pull qwen2.5:3b
```

### 5. Start the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 💡 Example Questions

After uploading documents, you can ask questions such as:

```text
What is my CGPA?

How many students are there?

What are the project objectives?

Who is the project coordinator?

What technologies are mentioned in the document?
```

The system searches the uploaded documents and generates an answer based only on the retrieved evidence.

## 📊 Reliability Score

The system provides a reliability score based on factors such as:

* Strength of retrieved document evidence
* Matching factual information
* Presence of important numerical values
* Answer-to-evidence relationship

This helps users understand how strongly an answer is supported by the uploaded documents.

## 🔒 Privacy

This project is designed around local processing.

Documents are processed locally, and the question-answering model runs through Ollama on the user's machine.

No external AI API is required for answering questions.

## 🚀 Future Improvements

* Automatic document indexing after upload
* Improved document chunking
* Multi-page PDF understanding
* Table-aware CSV and PDF retrieval
* Chat history
* Source highlighting
* Advanced confidence evaluation
* Improved dashboard UI
* Support for additional document formats

## 🎯 Project Goal

The goal of this project is to build a **privacy-friendly, local AI document assistant** that can retrieve information from personal documents and provide evidence-grounded answers without depending on cloud-based AI services.

## 👩‍💻 Author

**Jenita Jebaseelan**

B.Tech Artificial Intelligence & Data Science

Aspiring AI Engineer
