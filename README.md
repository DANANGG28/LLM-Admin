# toko-bot 🛒🤖

An AI-powered WhatsApp store bot using Google ADK, RAG (Retrieval-Augmented Generation), Google Sheets, and Fonnte for WhatsApp messaging.

---

## 📁 Project Structure

```
toko-bot/
├── main.py              # Entry point (FastAPI server)
├── agent.py             # Google ADK agent definition
├── rag/
│   ├── ingest.py        # Ingest katalog.txt into ChromaDB
│   └── retriever.py     # RAG retrieval logic
├── tools/
│   ├── sheets_tool.py   # Google Sheets integration
│   └── fonnte_tool.py   # Fonnte WhatsApp sender
├── data/
│   └── katalog.txt      # Product catalog (plain text)
├── .env                 # Environment variables (do NOT commit)
├── .env.example         # Environment variable template
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🚀 Setup Steps

### 1. Clone the Project

```bash
git clone https://github.com/your-username/toko-bot.git
cd toko-bot
```

---

### 2. Install Dependencies

Make sure you have Python 3.10+ installed, then run:

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Copy the example env file and fill in your actual values:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
GEMINI_API_KEY=your_key_here
FONNTE_TOKEN=your_token_here
GOOGLE_SHEET_ID=your_sheet_id_here
GOOGLE_CREDENTIALS_PATH=credentials.json
```

---

## 🔑 How to Get Each API Key

### GEMINI_API_KEY
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API key**
4. Copy the key and paste it into `.env`

---

### FONNTE_TOKEN
1. Register at [Fonnte](https://fonnte.com)
2. Connect your WhatsApp number in the dashboard
3. Go to **Settings → Token**
4. Copy your device token and paste it into `.env`

---

### GOOGLE_SHEET_ID
1. Open your Google Sheet in the browser
2. The Sheet ID is in the URL:
   `https://docs.google.com/spreadsheets/d/**SHEET_ID_HERE**/edit`
3. Copy that portion and paste it into `.env`

---

### GOOGLE_CREDENTIALS_PATH (Service Account)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use an existing one)
3. Enable the **Google Sheets API** and **Google Drive API**
4. Go to **IAM & Admin → Service Accounts**
5. Create a Service Account and download the JSON key
6. Rename it to `credentials.json` and place it in the project root
7. Share your Google Sheet with the service account email

---

## ▶️ Running the Bot

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📌 Notes

- Never commit your `.env` or `credentials.json` to version control
- Make sure to add them to `.gitignore`
