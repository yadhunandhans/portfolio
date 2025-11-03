from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import io
import json

from config import ALLOWED_ORIGINS, PORT
from providers.openai_vision import OpenAIVisionProvider

app = FastAPI(title="Medical Vision Chatbot", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

provider = OpenAIVisionProvider()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    include_last_image: Optional[bool] = False

@app.get("/")
def root():
    return {"status": "ok", "service": "medical-vision-chatbot"}

@app.post("/analyze")
async def analyze_image(prompt: Optional[str] = Form(default=""), image: UploadFile = File(...)):
    content = await image.read()
    text = await provider.analyze(prompt or "Analyze this medical image.", content)
    disclaimer = "This is not medical advice. Consult a qualified healthcare professional for diagnosis and treatment."
    return {"result": text, "disclaimer": disclaimer}

@app.post("/chat")
async def chat_endpoint(req: str = Form(...), image: Optional[UploadFile] = File(default=None)):
    parsed = ChatRequest(**json.loads(req))
    img_bytes = await image.read() if image else None
    msgs = [m.model_dump() for m in parsed.messages]
    text = await provider.chat(msgs, img_bytes if parsed.include_last_image else None)
    disclaimer = "This is not medical advice. Consult a qualified healthcare professional."
    return {"result": text, "disclaimer": disclaimer}

# To run: uvicorn main:app --reload --port 8000
