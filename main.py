# main.py
from fastapi import FastAPI, Request
from openai import OpenAI
import os

app = FastAPI()

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    text = data.get("text")
    sender = data.get("sender")

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        reply = response.choices[0].message.content
        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}
