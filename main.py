from fastapi import FastAPI, Request
import json
from openai import OpenAI

app = FastAPI()

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    message = body.get("text", "")
    sender = body.get("sender", "unknown")

    prompt = f"""
    Extract this cargo enquiry:
    '{message}'
    Return JSON like: {{
      "cargo_type": "", "quantity": "", "origin": "", "destination": "", "laycan": "", "notes": ""
    }}
    """

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = chat_completion.choices[0].message.content
        try:
            details = json.loads(response_text)
        except Exception:
            return {
                "error": "Failed to parse OpenAI response",
                "raw_response": response_text
            }

        return {
            "message": message,
            "sender": sender,
            "cargo_data": details
        }

    except Exception as e:
        return {"error": str(e)}
