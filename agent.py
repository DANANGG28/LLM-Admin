import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from tools.sheets_tool import get_product_info
from rag.retriever import search_knowledge_base

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

conversation_history = {}

def get_agent_response(user_message: str, session_id: str) -> str:
    try:
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        user_lower = user_message.lower()
        product_keywords = ["harga", "stok", "ada gak", "berapa", "harganya", "tersedia", "ready"]
        is_product_query = any(kw in user_lower for kw in product_keywords)
        
        response = ""
        
        if is_product_query:
            product_name = user_message.replace("kak", "").replace("harga", "").replace("berapa", "").strip()
            product_info = get_product_info(product_name)
            
            if "error" not in product_info:
                resp = f"Halo! {product_info.get('nama', '')} tersedia dengan harga:\n\n"
                
                if product_info.get('harga_ecer'):
                    resp += f"• Ecer  : Rp {product_info['harga_ecer']:,}/pcs\n"
                
                if product_info.get('harga_lusin'):
                    resp += f"• Lusin : Rp {product_info['harga_lusin']:,} (12 pcs)\n"
                
                if product_info.get('harga_kolian'):
                    isi_kolian = product_info.get('isi_kolian', '?')
                    resp += f"• Kolian: Rp {product_info['harga_kolian']:,} ({isi_kolian} pcs)\n"
                
                if product_info.get('stok'):
                    resp += f"\n📦 Stok: {product_info['stok']} pcs tersedia"
                
                response = resp + "\n\nMau pesan berapa? 😊"
            else:
                response = "Produk tidak tersedia atau belum ada di katalog. Hubungi admin untuk info lebih lanjut 😊"
        
        else:
            kb_result = search_knowledge_base(user_message)
            if kb_result and kb_result != "Informasi tidak tersedia":
                response = kb_result + "\n\nAda yang lain bisa dibantu? 😊"
            else:
                response = "Maaf, pertanyaan ini diluar layanan toko kami. Silakan hubungi admin untuk bantuan lebih lanjut 😊"
        
        conversation_history[session_id].append({
            "user": user_message,
            "bot": response,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(conversation_history[session_id]) > 10:
            conversation_history[session_id] = conversation_history[session_id][-10:]
        
        return response
        
    except Exception as e:
        print(f"[{datetime.now()}] Error: {str(e)}")
        return "Maaf, terjadi kesalahan pada sistem kami. Silakan hubungi admin kami 😊"


if __name__ == "__main__":
    print("Testing agent...\n")
    
    response1 = get_agent_response("kak harga japanesse bowl a-6 berapa?", "test-session-1")
    print(f"Q: kak harga japanesse bowl a-6 berapa?\nA: {response1}\n")
    print("="*60 + "\n")
    
    response2 = get_agent_response("gimana cara pemesanan?", "test-session-1")
    print(f"Q: gimana cara pemesanan?\nA: {response2}\n")
    print("="*60 + "\n")
    
    response3 = get_agent_response("siapa presiden indonesia?", "test-session-1")
    print(f"Q: siapa presiden indonesia?\nA: {response3}\n")
    
    print("Agent testing complete!")
