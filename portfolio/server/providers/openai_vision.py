from typing import List, Optional
import base64
import httpx

from config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_VISION_MODEL

OPENAI_CHAT_URL = f"{OPENAI_BASE_URL}/chat/completions"

class OpenAIVisionProvider:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.model = OPENAI_VISION_MODEL
        self.url = OPENAI_CHAT_URL

    def _image_to_b64(self, image_bytes: bytes) -> str:
        return base64.b64encode(image_bytes).decode("utf-8")

    async def analyze(self, prompt: str, image_bytes: bytes) -> str:
        if not self.api_key:
            return "[Provider not configured] Set OPENAI_API_KEY to enable vision analysis."

        b64 = self._image_to_b64(image_bytes)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a medical assistant. Provide non-diagnostic, educational insights only. Always include a disclaimer that this is not medical advice.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt or "Analyze this medical image."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{b64}"},
                        },
                    ],
                },
            ],
            "temperature": 0.2,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(self.url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()

    async def chat(self, messages: List[dict], image_bytes: Optional[bytes] = None) -> str:
        if not self.api_key:
            return "[Provider not configured] Set OPENAI_API_KEY to enable chat."

        content_blocks = []
        # Convert last user message content into multimodal blocks
        for m in messages:
            if m.get("role") == "user" and isinstance(m.get("content"), str):
                content_blocks.append({"type": "text", "text": m["content"]})

        if image_bytes:
            b64 = self._image_to_b64(image_bytes)
            content_blocks.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a medical assistant. Provide non-diagnostic, educational insights only. Include a brief disclaimer."},
                {"role": "user", "content": content_blocks or [{"type": "text", "text": "Continue the analysis."}]},
            ],
            "temperature": 0.2,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(self.url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()
