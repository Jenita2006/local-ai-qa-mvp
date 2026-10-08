import requests


OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "qwen2.5:3b"


def check_ollama():
    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=5
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


def ask_llm(question, context):

    prompt = f"""
You are a local document question-answering assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I could not find this information in the uploaded documents."

Do not invent facts.
Do not use outside knowledge.
Keep the answer concise.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"].strip()