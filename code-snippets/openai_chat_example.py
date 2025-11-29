"""
Короткий пример диалога с LLM через OpenAI SDK.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    print(ask("Сделай краткий список задач для запуска RAG-проекта."))
