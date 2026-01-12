from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import re

app = FastAPI()

PADDLER_ENDPOINT = "https://medai.nomineelife.com/v1/chat/completions"
MODEL_NAME = "Qwen3 0.6B Instruct"

class ChatRequest(BaseModel):
    messages: list

def strip_think(text: str) -> str:
    return re.sub(r"<think>[\s\S]*?</think>", "", text).strip()

@app.get("/")
def serve_ui():
    return FileResponse("/var/www/chat-ui-backend/index.html")

@app.post("/api/chat")
def chat(req: ChatRequest):
    payload = {
        "model": MODEL_NAME,
        "stream": False,
        "messages": req.messages
    }

    response = requests.post(PADDLER_ENDPOINT, json=payload, timeout=60, verify=False)
    response.raise_for_status()

    data = response.json()
    raw = data["choices"][0]["message"]["content"]
    clean = strip_think(raw)

    return { "reply": clean }

