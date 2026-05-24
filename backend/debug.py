from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print("API KEY FOUND:", api_key is not None)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

print("API KEY =", os.getenv("OPENAI_API_KEY"))
print(repr(api_key))
print(len(api_key))

class DebugRequest(BaseModel):
    code: str
    error: str

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/debug")
def debug_java(req: DebugRequest):

    try:
        print("POST HIT")
        print("CODE:", req.code)
        print("ERROR:", req.error)

        print("Request received")

        prompt = f"""
Java Code:
{req.code}

Error:
{req.error}
"""

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Java debugging expert"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "result": response.choices[0].message.content
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {
            "error": str(e)
        }