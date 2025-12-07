# Quick Start - Run Backend

## ✅ Correct Commands (Copy & Paste)

```bash
cd /Users/subodhkathayat/Desktop/hackathon/neptou-backend
source venv/bin/activate
python3 main.py
```

**OR** use uvicorn directly:

```bash
cd /Users/subodhkathayat/Desktop/hackathon/neptou-backend
source venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔍 Why `python3` instead of `python`?

On macOS, Python 3 is accessed via `python3`. The venv has `python3` available.

## ✅ Verify It's Running

After running the command, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Test it: Open http://localhost:8000 in your browser

## 🛑 Stop the Server

Press `CTRL+C` in the terminal

