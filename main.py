import os
import json
from datetime import datetime
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from agent import get_agent_response
from tools.fonnte_tool import send_whatsapp

load_dotenv()

app = FastAPI(title="Toko Bot")

@app.get("/health")
def health():
    return {"status": "running", "timestamp": str(datetime.now())}

@app.get("/webhook")
def webhook_get():
    return {"status": "ok", "message": "webhook active"}

@app.post("/webhook")
async def webhook(request: Request):
    try:
        payload = await request.json()
        
        sender = payload.get("sender", "").strip()
        message = payload.get("message", "").strip()
        device = payload.get("device", "")
        
        # Skip if no data
        if not sender or not message:
            return {"status": "skip"}
        
        # Log incoming
        print(f"\n[{datetime.now()}] IN: {sender} → {message[:50]}")
        
        # Process with agent
        response = get_agent_response(message, session_id=sender)
        
        # Validate response
        if not response:
            response = "Maaf, ada kesalahan. Coba lagi 😊"
        
        # Send back
        success = send_whatsapp(sender, response)
        
        if success:
            print(f"[{datetime.now()}] OUT: {sender} ← {response[:50]}")
            return {"status": "ok"}
        else:
            return {"status": "error"}
    
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {"status": "error", "reason": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("Bot running on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
