import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")

def send_whatsapp(phone: str, message: str) -> bool:
    """Send message via Fonnte API"""
    try:
        # Format phone
        phone = phone.strip()
        if phone.startswith('+62'):
            phone = phone[1:]  # Remove +
        elif phone.startswith('0'):
            phone = '62' + phone[1:]  # Replace 0 with 62
        
        # Send via Fonnte
        url = "https://api.fonnte.com/send"
        headers = {"Authorization": FONNTE_TOKEN}
        data = {"target": phone, "message": message}
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"[{datetime.now()}] ✓ Sent to {phone}")
            return True
        else:
            print(f"[{datetime.now()}] ✗ Failed to {phone}: {response.text}")
            return False
    
    except Exception as e:
        print(f"[{datetime.now()}] Error sending WA: {str(e)}")
        return False
