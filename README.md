# 🦜⛓️ MCQ Generator — AI-Powered Quiz Maker

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-Educational-green?style=for-the-badge"/>
</p>

<p align="center">
  An intelligent Streamlit web app that automatically generates Multiple Choice Questions (MCQs) from any uploaded <strong>PDF or TXT</strong> file using <strong>LangChain + OpenAI</strong>.
</p>

---

## 📸 Demo

> Upload a document → set parameters → get a quiz with AI review in seconds.

| Step | What you see |
|------|-------------|
| 1 | Upload PDF/TXT, configure MCQ count, subject, difficulty |
| 2 | AI generates structured MCQs as a clean table |
| 3 | AI review critiques quiz quality in ≤50 words |
| 4 | Token usage + USD cost shown in expandable panel |

---

## ✨ Features

- 📄 **File Upload** — PDF (via PyPDF2) and plain TXT support
- 🤖 **AI-Powered Generation** — LangChain `SequentialChain` with `gpt-5`
- 📊 **Structured Output** — JSON responses rendered as a readable pandas table
- 🧠 **Smart Review** — Second LLM pass evaluates quiz complexity and suggests improvements
- 💰 **Cost Tracking** — Live token usage + USD cost via `get_openai_callback`
- 🪵 **Logging** — Timestamped log files auto-created in `/logs`
- 🎯 **Clean UI** — Streamlit form + sidebar API key input, no setup friction

---

## 🗂️ Project Structure

```
mcqgen/
├── src/
│   └── mcqgenerator/
│       ├── __init__.py
│       ├── logger.py          # Timestamped logging to /logs
│       ├── utils.py           # read_file() + get_table_data()
│       └── MCQgenerator.py    # LangChain chains (quiz generation + review)
├── logs/                      # Auto-created at runtime
├── StreamlitAPP.py            # Main Streamlit UI
├── Response.json              # MCQ JSON format template fed to the prompt
├── requirements.txt
├── setup.py
├── test.txt                   # Sample input file for testing
└── .env.example
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone the repository

```bash
git clone https://github.com/Aman9051/mcqgen.git
cd mcqgen
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

```bash
cp .env.example .env
```

Open `.env` and add your key:

```
OPENAI_API_KEY=sk-your-key-here
```

> Alternatively, just paste your key in the **sidebar** when the app is running — no `.env` file needed.

### 4. Run the app

```bash
streamlit run StreamlitAPP.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🎮 Usage Guide

1. **Enter your OpenAI API key** in the sidebar (or set it via `.env`)
2. **Upload a document** — PDF or TXT file
3. **Configure parameters:**
   - Number of MCQs (1–20)
   - Subject (e.g. *Biology*, *History*, *Machine Learning*)
   - Difficulty level (*simple / medium / hard*)
4. **Click "Generate MCQs"**
5. **Review results:**
   - MCQ table with questions, options (a/b/c/d), and correct answers
   - AI-generated review of quiz quality
   - Token usage and cost breakdown (expandable)

---

## 🛠️ Core Components

### `logger.py`
Creates a timestamped `.log` file inside `/logs` on every run. Tracks application flow, warnings, and errors using Python's built-in `logging` module.

### `MCQgenerator.py`
The brain of the app. Uses a **LangChain `SequentialChain`** with two LLM passes:
- **Chain 1** — generates MCQs in structured JSON format based on the uploaded text
- **Chain 2** — reviews the quiz for complexity and suggests improvements

### `utils.py`
Two helper functions:
- `read_file(file)` — extracts text from PDF (PyPDF2) or TXT (UTF-8 decode)
- `get_table_data(quiz_str)` — parses the JSON quiz output into a list of dicts for pandas display

### `StreamlitAPP.py`
The Streamlit frontend. Handles file upload, user inputs, invokes the chain, and renders the MCQ table, review, and cost metrics.

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| LLM | [OpenAI](https://openai.com) `gpt-5` |
| Orchestration | [LangChain](https://python.langchain.com) `SequentialChain` |
| PDF Parsing | [PyPDF2](https://pypdf2.readthedocs.io) |
| Data Display | [pandas](https://pandas.pydata.org) |
| Config | [python-dotenv](https://github.com/theskumar/python-dotenv) |

---

## 🔧 Troubleshooting

| Issue | Solution |
|---|---|
| `AuthenticationError` | Check your `.env` file or sidebar key input |
| JSON parse error | Model returned malformed JSON — raw output shown as fallback |
| Empty file error | Ensure the PDF has selectable (not scanned) text |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| Missing logs | Check write permissions for the `/logs` directory |

---

## 💡 Use Cases

- 🎓 **Education** — Generate practice quizzes from textbooks or lecture notes
- 🏢 **Corporate Training** — Build assessments from internal documentation
- 📝 **Self-Study** — Turn your notes into interactive test questions
- 🧑‍💻 **Content Creation** — Rapid quiz generation for e-learning platforms

---

## ⚠️ Important Notes

- ✅ Supports **PDF and TXT** files only
- ✅ Requires a **valid OpenAI API key** (costs apply per token)
- ✅ JSON output must be valid for table rendering; raw fallback shown if parsing fails
- ⚠️ For scanned PDFs (image-based), text extraction may return empty — use a text-layer PDF

---

## 📧 Contact

**Aman Singh**
📬 [amankrsingh764@gmail.com](mailto:amankrsingh764@gmail.com)
🐙 [github.com/Aman9051](https://github.com/Aman9051)

---

## 📄 License

This project is for **educational and demonstration purposes** only.

---

<p align="center">Built with ❤️ using Streamlit and OpenAI</p>