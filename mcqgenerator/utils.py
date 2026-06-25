import json
import traceback
import PyPDF2
from mcqgenerator.logger import get_logger

logger = get_logger(__name__)


def read_file(file) -> str:
    """Extract text from uploaded PDF or TXT file."""
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            logger.error(f"PDF read error: {e}")
            raise Exception(f"Error reading PDF: {e}")

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception("Unsupported file format. Upload PDF or TXT only.")


def get_table_data(quiz_str: str) -> list:
    """
    Parse JSON quiz string into list of dicts for DataFrame display.
    Expected format:
    {
      "1": {"mcq": "...", "options": {"a": "...", "b": "...", "c": "...", "d": "..."}, "correct": "a"},
      ...
    }
    """
    try:
        quiz_str = quiz_str.strip()
        if quiz_str.startswith("```"):
            quiz_str = quiz_str.split("```")[1]
            if quiz_str.startswith("json"):
                quiz_str = quiz_str[4:]
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value.get("mcq", "")
            options = value.get("options", {})
            opts_str = " | ".join([f"{k}: {v}" for k, v in options.items()])
            correct = value.get("correct", "")
            quiz_table_data.append({
                "MCQ": mcq,
                "Options": opts_str,
                "Correct": correct
            })
        return quiz_table_data
    except Exception as e:
        logger.error(f"Table parse error: {traceback.format_exc()}")
        return []