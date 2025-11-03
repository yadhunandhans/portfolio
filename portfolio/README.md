# Medical Image Chatbot (MVP)

A minimal FastAPI backend and lightweight frontend to analyze medical images with a vision LLM and chat. Non-diagnostic, educational use only.

## Setup

### Server
1. Create env: copy `server/.env.example` to `server/.env` and set `OPENAI_API_KEY`.
2. Install deps:
   ```bash
   pip install -r server/requirements.txt
   ```
3. Run server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   Run this from the `server/` directory.

### Frontend
Open `client/index.html` directly in a browser, or serve it with a simple server. Ensure CORS origin is allowed in `server/.env`.

## Endpoints
- `POST /analyze` (multipart): fields `image` (file), `prompt` (text)
- `POST /chat` (multipart): parts `req` (json blob with `{messages, include_last_image}`), optional `image` (file)

## Notes
- Data handling is ephemeral by default; no storage at rest.
- This is not medical advice. Do not upload PHI.
