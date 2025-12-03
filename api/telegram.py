from fastapi import FastAPI, Response, Request
import httpx
from core.settings import settings
from handler.start import openai_client
import openai
from fastapi.responses import JSONResponse


app = FastAPI()
openai_client = openai.OpenAI() 


async def send_to_telegram(chat_id: str, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            settings.TELEGRAM_URL,
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown"
            })

@app.post("/api/telegram")
async def telegram_webhook(request: Request):
    body = request.json()

    message = body.get("message", {})
    chat_id = body.get("chat_id", {})

    if not chat_id:
        return Response(status_code=400)

    if "text" in message:
        user_text = message["text"]
        response = openai_client.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {
                    "role": "system", 
                    "content": "You AI - assitent for help user to their questions"
                },
                {   
                    "role": "user",
                    "content": user_text
                }
            ],
            temperature = 0.7,
        )

        reply = response.choices[0].message.content
        await send_to_telegram(chat_id=chat_id, text=reply)

    else:
        await send_to_telegram(chat_id=chat_id, text = "I dont understand your request")

    return JSONResponse(content={"status": "ok"})