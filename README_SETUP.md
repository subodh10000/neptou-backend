# Neptou Backend Setup & Run Guide

## Quick Start

### 1. Navigate to Backend Directory
```bash
cd neptou-backend
```

### 2. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt.

### 3. Set Up Environment Variables

Create a `.env` file in the `neptou-backend` directory:

```bash
# Create .env file
touch .env
```

Then add your API key:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

**To get your Anthropic API key:**
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste it into your `.env` file

### 4. Run the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag enables auto-reload when you make code changes (useful for development).

### 5. Verify It's Running

You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Test it by opening in your browser:
- http://localhost:8000
- http://127.0.0.1:8000

You should see: `{"message": "Namaste! Neptou Backend is running."}`

### 6. Test API Endpoints

**Test Chat Endpoint:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"history": [{"role": "user", "content": "Hello!"}]}'
```

## Troubleshooting

### "ANTHROPIC_API_KEY environment variable is not set"
- Make sure you created the `.env` file
- Check that the file is in the `neptou-backend` directory
- Verify the API key is correct (no extra spaces)

### "Port 8000 is already in use"
- Change the port in `main.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`
- Or kill the process using port 8000:
  ```bash
  lsof -ti:8000 | xargs kill
  ```

### "Module not found" errors
- Make sure virtual environment is activated (`venv` should appear in prompt)
- Reinstall dependencies if needed:
  ```bash
  pip install fastapi uvicorn python-dotenv anthropic
  ```

### CORS Errors from iOS App
- Make sure `ALLOWED_ORIGINS` in `.env` includes your Mac's local IP
- For iOS Simulator: use `http://127.0.0.1:8000`
- For real device: use your Mac's IP (e.g., `http://192.168.1.5:8000`)

## Stopping the Server

Press `CTRL+C` in the terminal where the server is running.

## Deactivate Virtual Environment

When you're done:
```bash
deactivate
```

