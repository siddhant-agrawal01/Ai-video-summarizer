# Deployment Plan: Render via CI/CD Dockerization

This document outlines the detailed steps required to containerize the AI Video Summarizer backend and deploy it to [Render.com](https://render.com) using a continuous integration and continuous deployment (CI/CD) approach. 

## Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Step 1: Containerizing the Application (Docker)](#step-1-containerizing-the-application-docker)
3. [Step 2: Version Control & Repository Setup](#step-2-version-control--repository-setup)
4. [Step 3: Render Setup & Configuration](#step-3-render-setup--configuration)
5. [Step 4: Continuous Deployment (CI/CD)](#step-4-continuous-deployment-cicd)
6. [Crucial Architectural Considerations](#crucial-architectural-considerations)

---

## 1. Prerequisites
- A **GitHub** account with your code pushed to a repository.
- A **Render** account (linked to your GitHub).
- Required API Keys (`MISTRAL_API_KEY`, `SARVAM_API_KEY`, etc.).

---

## Step 1: Containerizing the Application (Docker)

To deploy on Render using Docker, we need to create a `Dockerfile` and a `.dockerignore` file in the root directory. 

### 1.1 Create the `Dockerfile`
Create a file named `Dockerfile` (no extension) in the root of your project:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (ffmpeg is required for pydub and yt-dlp)
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY Requirements.txt .

# Install Python dependencies
# We use --no-cache-dir to keep the image size small
RUN pip install --no-cache-dir -r Requirements.txt

# Install uvicorn separately if it's not in Requirements.txt
RUN pip install --no-cache-dir uvicorn

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 1.2 Create the `.dockerignore`
Create a file named `.dockerignore` to prevent unnecessary files from inflating the container size:

```text
.venv/
__pycache__/
*.pyc
.env
.git/
.gitignore
vector_db/
uploads/
downloades/
*.md
```

---

## Step 2: Version Control & Repository Setup

Render's CI/CD works by listening to pushes to a specific branch (usually `main` or `master`) in your GitHub repository.

1. **Commit your Docker files**: 
   ```bash
   git add Dockerfile .dockerignore
   git commit -m "Add Docker configuration for Render deployment"
   ```
2. **Push to GitHub**:
   ```bash
   git push origin main
   ```

---

## Step 3: Render Setup & Configuration

1. **Log in to Render Dashboard**: Go to [dashboard.render.com](https://dashboard.render.com/).
2. **Create a New Web Service**:
   - Click the **"New +"** button and select **"Web Service"**.
   - Connect your GitHub account and select your repository.
3. **Configure the Service**:
   - **Name**: e.g., `ai-video-summarizer-api`
   - **Region**: Choose the one closest to you or your users.
   - **Branch**: `main` (or whichever branch you push code to).
   - **Environment**: Select **Docker** (Render will automatically detect your `Dockerfile`).
4. **Instance Type (Important!)**:
   - Because you are running **PyTorch** and **Local Whisper Models** (`openai-whisper`), a free tier or micro instance **will likely fail** due to Out-Of-Memory (OOM) errors. 
   - **Recommendation**: Select an instance with at least **2GB to 4GB of RAM** (e.g., Starter or Standard tier).
5. **Environment Variables**:
   Scroll down to "Environment Variables" and add all the keys from your `.env` file:
   - `MISTRAL_API_KEY` = `your_key`
   - `SARVAM_API_KEY` = `your_key`
   - `WHISPER_MODEL` = `small` (or `base` / `tiny` if you need to save RAM)
6. **Advanced Settings (Health Check)**:
   - Set the **Health Check Path** to `/api/health`. Render will use this to ensure your app is running successfully.
7. **Deploy**:
   - Click **"Create Web Service"**.

---

## Step 4: Continuous Deployment (CI/CD)

Once your Web Service is created, Render will automatically build the Docker image and deploy it. 

**How the CI/CD Pipeline Works:**
1. You make changes to your local code.
2. You commit and push those changes to the `main` branch on GitHub.
3. Render intercepts the GitHub webhook.
4. Render automatically pulls the new code, rebuilds the Docker container, and performs a zero-downtime deployment.

You can monitor the build logs directly in the Render dashboard. Once deployed, Render will provide you with a live URL (e.g., `https://ai-video-summarizer-api.onrender.com`).

---

## Crucial Architectural Considerations

Before going to production, you must be aware of how Render's ephemeral filesystem affects your current code architecture:

### 1. Ephemeral File System
Render's default filesystem is **ephemeral**. This means every time you deploy a new version, or Render restarts the instance, all files written to disk are wiped.
- **`uploads/` and `downloades/`**: Temporary processing files will be deleted. This is fine for temporary video processing.
- **`vector_db/`**: Your ChromaDB embeddings will be deleted on restart. If you need historical meetings to be searchable across restarts, you **must** attach a **Render Persistent Disk** and map it to your `/app/vector_db` directory in the Render dashboard.

### 2. In-Memory State (`sessions` dictionary)
In `api.py`, you are storing the LangChain `rag_chain` in a global dictionary:
```python
sessions = {}
# ...
sessions[session_id] = rag_chain
```
- This means state is tied to the specific server instance's memory. 
- If the instance restarts, **all active chat sessions will be lost**. 
- If you scale to multiple instances, requests might be routed to a server that doesn't have the session in memory.
- *Fix for Production*: For true scale, you should not store LangChain objects in memory. You should rebuild the chain per request using a session ID, or store session contexts in a persistent database (like Redis or Postgres).

### 3. CPU vs GPU
Render Web Services run on CPUs. Local Whisper models (especially `small` and above) can take several minutes to transcribe an hour-long video on a CPU. Expect longer processing times compared to your local machine if you run a dedicated GPU locally. Consider using `tiny` or `base` for the `WHISPER_MODEL` in your Render environment variables if speed becomes an issue.
