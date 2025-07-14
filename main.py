import os
import openai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask_legal_question(request: Request):
    data = await request.json()
    question = data.get("question", "").strip()

    if not openai.api_key:
        return {"answer": "OpenAI key not found. Please add your API key to the environment."}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Vakeel Saab, a highly knowledgeable, friendly Indian legal assistant. You answer legal questions about Indian law clearly, in simple English and Hindi when needed."},
                {"role": "user", "content": question}
            ],
            temperature=0.4,
            max_tokens=500
        )
        return {"answer": response["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"answer": f"An error occurred: {str(e)}"}