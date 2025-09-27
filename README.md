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
```

### 2. Quick Start (Recommended)
```bash
# Install all dependencies and start development server
npm run setup
npm run dev
```

### 3. Manual Setup
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

## 🚀 Available Scripts

- `npm run dev` - Start development server with auto-reload
- `npm run start` - Start production server
- `npm run install-deps` - Install Python dependencies
- `npm run setup` - Install both Node.js and Python dependencies
- `npm run test` - Run tests
- `npm run lint` - Run linting
- `npm run format` - Format code