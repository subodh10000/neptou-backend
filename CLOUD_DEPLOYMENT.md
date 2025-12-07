# Cloud Deployment Guide for Neptou Backend

This guide covers deploying your FastAPI backend to various cloud platforms.

## Prerequisites

1. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)
2. **API Keys**: Have your `ANTHROPIC_API_KEY` ready
3. **Data Files**: Ensure all JSON/data files are committed to your repository:
   - `tourism_data.json`
   - `tourism_embeddings.json`
   - `local_insights.json`
   - `emergency_contacts_embeddings.json`
   - `neptou.db` (if using SQLite)
   - Any other data files your app needs

---

## Option 1: Railway (Recommended for Beginners) 🚂

**Best for**: Quick deployment, automatic HTTPS, easy environment variables

### Steps:

1. **Sign up**: Go to [railway.app](https://railway.app) and sign up with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment Variables**:
   - Go to your project → Variables tab
   - Add:
     ```
     ANTHROPIC_API_KEY=your_key_here
     ALLOWED_ORIGINS=*
     PORT=8000
     ```

4. **Deploy**:
   - Railway will automatically detect the `Dockerfile` or `railway.json`
   - It will build and deploy your app
   - You'll get a URL like: `https://neptou-backend-production.up.railway.app`

5. **Update CORS in main.py** (if needed):
   - Update `ALLOWED_ORIGINS` to include your Railway URL

**Pricing**: Free tier available, then pay-as-you-go

---

## Option 2: Render 🎨

**Best for**: Free tier with automatic deployments

### Steps:

1. **Sign up**: Go to [render.com](https://render.com) and sign up

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure**:
   - **Name**: `neptou-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or paid for better performance)

4. **Environment Variables**:
   - Scroll down to "Environment Variables"
   - Add:
     ```
     ANTHROPIC_API_KEY=your_key_here
     ALLOWED_ORIGINS=*
     ```

5. **Deploy**:
   - Click "Create Web Service"
   - Render will build and deploy
   - You'll get a URL like: `https://neptou-backend.onrender.com`

**Note**: Free tier spins down after 15 minutes of inactivity (takes ~30s to wake up)

**Pricing**: Free tier available, $7/month for always-on

---

## Option 3: Fly.io 🚀

**Best for**: Global edge deployment, great performance

### Steps:

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Sign up and Login**:
   ```bash
   fly auth signup
   fly auth login
   ```

3. **Create Fly App**:
   ```bash
   fly launch
   ```
   - Follow prompts
   - Don't deploy yet (we'll configure first)

4. **Create `fly.toml`** (if not auto-generated):
   ```toml
   app = "neptou-backend"
   primary_region = "iad"

   [build]

   [http_service]
     internal_port = 8000
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0
     processes = ["app"]

   [[services]]
     protocol = "tcp"
     internal_port = 8000
     processes = ["app"]

     [[services.ports]]
       handlers = ["http"]
       port = 80

     [[services.ports]]
       handlers = ["tls", "http"]
       port = 443
   ```

5. **Set Secrets**:
   ```bash
   fly secrets set ANTHROPIC_API_KEY=your_key_here
   fly secrets set ALLOWED_ORIGINS=*
   ```

6. **Deploy**:
   ```bash
   fly deploy
   ```

**Pricing**: Generous free tier, pay for what you use

---

## Option 4: Google Cloud Run ☁️

**Best for**: Serverless, auto-scaling, pay-per-request

### Steps:

1. **Install Google Cloud SDK**:
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Login and Set Project**:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Build and Deploy**:
   ```bash
   # Build container
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/neptou-backend
   
   # Deploy to Cloud Run
   gcloud run deploy neptou-backend \
     --image gcr.io/YOUR_PROJECT_ID/neptou-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars ANTHROPIC_API_KEY=your_key_here,ALLOWED_ORIGINS=*
   ```

**Pricing**: Free tier: 2 million requests/month, then pay-per-use

---

## Option 5: AWS Elastic Beanstalk 🌐

**Best for**: AWS ecosystem integration

### Steps:

1. **Install EB CLI**:
   ```bash
   pip install awsebcli
   ```

2. **Initialize**:
   ```bash
   eb init -p python-3.13 neptou-backend --region us-east-1
   ```

3. **Create Environment**:
   ```bash
   eb create neptou-backend-env
   ```

4. **Set Environment Variables**:
   ```bash
   eb setenv ANTHROPIC_API_KEY=your_key_here ALLOWED_ORIGINS=*
   ```

5. **Deploy**:
   ```bash
   eb deploy
   ```

**Pricing**: Pay for EC2 instance (~$10-20/month minimum)

---

## Option 6: DigitalOcean App Platform 🌊

**Best for**: Simple deployment with good documentation

### Steps:

1. **Sign up**: [digitalocean.com](https://www.digitalocean.com)

2. **Create App**:
   - Go to App Platform
   - Click "Create App"
   - Connect GitHub repository

3. **Configure**:
   - **Type**: Web Service
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**:
   - Add `ANTHROPIC_API_KEY` and `ALLOWED_ORIGINS`

5. **Deploy**: Click "Create Resources"

**Pricing**: $5/month for basic plan

---

## Important Configuration Notes

### 1. Update CORS Settings

In `main.py`, update the CORS origins for production:

```python
# Production: Replace with your actual frontend URL
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://your-app.com").split(",")
```

### 2. Environment Variables

All platforms need these:
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins (or `*` for development)

### 3. Port Configuration

Most platforms set `PORT` automatically. Update `main.py` if needed:

```python
import os
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

### 4. File Size Limits

If your data files (JSON, FAISS index) are large:
- Consider using cloud storage (S3, Cloud Storage) and loading at runtime
- Or use a database instead of JSON files
- Check platform file size limits

### 5. Cold Starts

If using serverless (Render free tier, Cloud Run):
- First request after inactivity may be slow (~30s)
- Consider upgrading to always-on plan for production

---

## Testing Your Deployment

After deployment, test your API:

```bash
# Test root endpoint
curl https://your-app-url.com/

# Test chat endpoint
curl -X POST "https://your-app-url.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"history": [{"role": "user", "content": "Hello!"}]}'
```

---

## Monitoring & Logs

Most platforms provide:
- **Logs**: View real-time application logs
- **Metrics**: CPU, memory, request counts
- **Alerts**: Set up alerts for errors or downtime

---

## Recommended Platform by Use Case

- **Hackathon/Prototype**: Railway or Render (free, easy)
- **Production App**: Fly.io or Google Cloud Run (better performance)
- **Enterprise**: AWS Elastic Beanstalk or Google Cloud Run
- **Budget-Conscious**: Render free tier or Fly.io free tier

---

## Troubleshooting

### "Module not found" errors
- Ensure `requirements.txt` includes all dependencies
- Check build logs for installation errors

### "Port already in use"
- Most platforms set `PORT` automatically
- Use `os.getenv("PORT", 8000)` in your code

### "API key not found"
- Double-check environment variable names
- Ensure secrets are set correctly in platform dashboard

### Slow first request
- Normal for serverless platforms (cold start)
- Consider always-on plan for production

### CORS errors
- Update `ALLOWED_ORIGINS` to include your frontend URL
- Check that CORS middleware is configured correctly

---

## Next Steps

1. Choose a platform
2. Deploy using the steps above
3. Test all endpoints
4. Update your iOS app to use the new backend URL
5. Set up monitoring and alerts
6. Consider adding a custom domain

Good luck with your deployment! 🚀

