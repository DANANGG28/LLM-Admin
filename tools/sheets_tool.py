
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

def get_sheets_client():
    """Connect to Google Sheets"""
    try:
        # Check if credentials file exists
        if not Path(CREDENTIALS_PATH).exists():
            print(f"[sheets_tool] Error: {CREDENTIALS_PATH} not found")
            return None
        
        # Auth dengan service account
        creds = Credentials.from_service_account_file(
            CREDENTIALS_PATH,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        client = gspread.authorize(creds)
        return client
    
    except Exception as e:
        print(f"[sheets_tool] Error connecting to Sheets: {str(e)}")
        return None

def get_product_info(product_name: str) -> dict:
    """Get product info from Google Sheets"""
    try:
        client = get_sheets_client()
        if not client:
            return {"error": "Cannot connect to Google Sheets"}
        
        # Open sheet by ID
        sheet = client.open_by_key(GOOGLE_SHEET_ID)
        worksheet = sheet.worksheet("Grosir")
        
        # Get all values (skip header row 1-2)
        all_rows = worksheet.get_all_values()
        
        if len(all_rows) < 3:
            return {"error": "Sheet is empty"}
        
        # Search product (case-insensitive, partial match)
        product_lower = product_name.lower().strip()
        
        for row in all_rows[2:]:  # Skip header rows (0, 1)
            if len(row) > 1 and row[1]:  # Column B (index 1)
                if product_lower in row[1].lower():
                    return {
                        "nama": row[1] if len(row) > 1 else "",
                        "deskripsi": row[2] if len(row) > 2 else "",
                        "stok": row[3] if len(row) > 3 else "",
                        "harga_ecer": row[7] if len(row) > 7 else "",
                        "harga_lusin": row[8] if len(row) > 8 else "",
                        "harga_kolian": row[9] if len(row) > 9 else "",
                        "isi_kolian": row[10] if len(row) > 10 else ""
                    }
        
        return {"error": "Produk tidak ditemukan"}
    
    except Exception as e:
        print(f"[sheets_tool] Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    result = get_product_info("japanesse bowl")
    print(result)
