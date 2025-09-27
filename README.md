# 🎒 ASU Lost & Found (Backend)

A FastAPI backend for managing lost & found items at ASU.  
Built at SunHacks 2025 🚀

---

## ⚡ Features
- Report **lost items** with description + location
- Report **found items**
- Retrieve all lost/found items
- SQLite database (file-based, no setup needed)
- Auto-generated API docs at `/docs`

---

## 🛠 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/dhruvrohitpatel/lostfound-sunhacks-25.git
cd lostfound-sunhacks-25

Run the server with : uvicorn main:app --reload