import openai
import os
from dotenv import load_dotenv
from app.core.prompt_builder import build_prompt

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

def extract_structured_data(template_id: str, text: str) -> dict:
    prompt = build_prompt(template_id, text)

    response = openai.ChatCompletion.create(
        model=os.getenv("GROQ_MODEL", "llama2-70b-4096"),
        messages=[
            {"role": "system", "content": "You extract structured data from financial documents."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    content = response['choices'][0]['message']['content']
    try:
        return eval(content) if content.startswith("{") else {}
    except Exception:
        return {"error": "Failed to parse LLM output"}