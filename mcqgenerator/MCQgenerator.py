import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from mcqgenerator.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

# ─── LLM ─────────────────────────────────────────────────────────────────────
llm = ChatOpenAI(
    model="gpt-5",
    temperature=0.5,
    openai_api_key=os.getenv("OPENAI_API_KEY")   # pulled from .env
)

# ─── PROMPT 1: Generate MCQs ─────────────────────────────────────────────────
TEMPLATE_1 = """
Text: {text}

You are an expert MCQ maker. Given the above text, create {number} multiple choice \
questions for {subject} students in a {tone} tone. Questions must not repeat and must \
conform to the text.

Format your response exactly like RESPONSE_JSON below. Return ONLY the JSON, no extra text.

### RESPONSE_JSON
{response_json}
"""

quiz_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE_1
)

# ─── PROMPT 2: Review MCQs ───────────────────────────────────────────────────
TEMPLATE_2 = """
You are an expert evaluator. Review the following MCQ quiz for {subject} students. \
Give a concise review in 1-2 sentences only — mention the difficulty level and \
whether it suits the students.

Quiz:
{quiz}

Review:
"""

review_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE_2
)

# ─── LCEL CHAINS ─────────────────────────────────────────────────────────────
quiz_chain   = quiz_prompt   | llm | StrOutputParser()
review_chain = review_prompt | llm | StrOutputParser()


def generate_evaluate_chain(inputs: dict) -> dict:
    quiz = quiz_chain.invoke({
        "text":          inputs["text"],
        "number":        inputs["number"],
        "subject":       inputs["subject"],
        "tone":          inputs["tone"],
        "response_json": inputs["response_json"]
    })

    review = review_chain.invoke({
        "subject": inputs["subject"],
        "quiz":    quiz
    })

    return {"quiz": quiz, "review": review}


logger.info("MCQgenerator chain initialized successfully")