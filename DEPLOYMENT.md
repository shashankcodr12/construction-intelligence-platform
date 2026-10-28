# 🚀 Deployment & Submission Guide

This guide details how to deploy the **Multimodal Construction Intelligence Platform** for **free** so you can submit a live, working URL and GitHub repository to your professor.

---

## 📋 Table of Contents
1. [Push to Your GitHub](#1-push-to-your-github)
2. [Option A: 1-Click Free Deployment on Render (Recommended)](#option-a-1-click-free-deployment-on-render-recommended)
3. [Option B: Vercel (Frontend) + Render (Backend)](#option-b-vercel-frontend--render-backend)
4. [Option C: Hugging Face Spaces (Docker — 100% Free, Always On)](#option-c-hugging-face-spaces-docker--100-free-always-on)
5. [Configuring the Gemini API Key](#configuring-the-gemini-api-key)
6. [Professor Submission Checklist](#professor-submission-checklist)

---

## 1. Push to Your GitHub

The local repository is already initialized on branch `main` with all files committed and configured.

### Step 1: Create a New GitHub Repository
1. Go to [GitHub.com/new](https://github.com/new).
2. Repository name: `construction-intelligence-platform` (or your preferred name).
3. Keep it **Public** (or Private if required by your university).
4. **Do NOT** check "Add a README file", `.gitignore`, or license (the codebase already has them).
5. Click **Create repository**.

### Step 2: Push Your Local Code
Open PowerShell or your terminal in this project directory and run:

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git

# Push the main branch
git push -u origin main
```

*(If prompted, sign in via your browser or paste your GitHub Personal Access Token.)*

---

## Option A: 1-Click Free Deployment on Render (Recommended)

Render offers a generous **free tier** that hosts both the FastAPI backend and React frontend together.

### Why this is best for college submission:
- **Single URL**: One link (`https://your-app.onrender.com`) containing both frontend and backend.
- **Zero CORS issues**: Frontend and backend are served on the same domain.
- **Included Blueprint**: A `render.yaml` file is already in your repository.

### Steps:
1. Sign up or log in at [render.com](https://render.com) (you can click **Sign in with GitHub**).
2. Click **New +** in the top navigation and select **Web Service**.
3. Choose **Build and deploy from a Git repository** and select your `construction-intelligence-platform` repo.
4. Fill in the settings:
   - **Name**: `construction-intelligence-platform` (or any unique name)
   - **Region**: Closest to you (e.g., Singapore, Frankfurt, or Oregon)
   - **Branch**: `main`
   - **Root Directory**: *(leave blank)*
   - **Runtime**: `Python`
   - **Build Command**: 
     ```bash
     cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type**: **Free**
5. Under **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.11.9`
   - `GEMINI_API_KEY`: `AIza...` *(Your Google AI Studio key)*
   - `GEMINI_MODEL`: `gemini-2.0-flash`
   - `ALLOWED_ORIGINS`: `*`
6. Click **Deploy Web Service**.

> ⏳ *Render will build the React frontend, install backend requirements, and start the app in ~3-4 minutes. Your live app will be live at `https://<your-service-name>.onrender.com`.*

---

## Option B: Vercel (Frontend) + Render (Backend)

If you want ultra-fast global CDN delivery for the frontend:

### Part 1: Deploy Backend on Render
1. In Render, select **New +** -> **Web Service**.
2. Connect your repository.
3. Configure:
   - **Root Directory**: `backend`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `GEMINI_API_KEY`: `AIza...`
     - `GEMINI_MODEL`: `gemini-2.0-flash`
     - `ALLOWED_ORIGINS`: `*`
4. Copy the backend URL (e.g., `https://construction-api.onrender.com`).

### Part 2: Deploy Frontend on Vercel
1. Sign up or log in at [vercel.com](https://vercel.com) using your GitHub account.
2. Click **Add New...** -> **Project**.
3. Import your GitHub repository.
4. In the configuration:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click *Edit* and select `frontend`.
5. Under **Environment Variables**, add:
   - `VITE_API_URL`: `https://construction-api.onrender.com` *(Paste your Render backend URL)*
6. Click **Deploy**.

> 🚀 *Vercel will deploy the frontend in under 60 seconds with an instant `https://your-project.vercel.app` link!*

---

## Option C: Hugging Face Spaces (Docker — 100% Free, Always On)

Hugging Face Spaces provides 100% free hosting with 16GB RAM and no cold-start sleep using Docker:

1. Sign up at [huggingface.co](https://huggingface.co).
2. Go to **Spaces** -> **Create new Space**.
3. Space name: `construction-intelligence-platform`.
4. License: `mit` or `apache-2.0`.
5. Space SDK: Select **Docker** -> **Blank**.
6. Set Space hardware to **Free CPU basic (2 vCPU, 16GB RAM)**.
7. Click **Create Space**.
8. In Space Settings -> **Variables and secrets**, add a secret:
   - Name: `GEMINI_API_KEY`
   - Value: `AIza...`
9. Push your repository to the Hugging Face git remote (instructions provided in your Space dashboard).
   *The multi-stage `Dockerfile` in the root will build and run both the React frontend and FastAPI backend automatically on port 7860/8000.*

---

## Configuring the Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Sign in with any Google account.
3. Click **Create API Key** and copy it (`AIza...`).
4. Set it as an environment variable (`GEMINI_API_KEY`) in your cloud provider's dashboard.
5. **Built-in Demo Fallback**: Even without an API key, the platform includes a complete **Simulated Fallback Mode** with realistic safety hazards, crack classification, and project estimates, so the demo will never crash in front of your professor!

---

## Professor Submission Checklist

When submitting your assignment or project, include:

1. **Live Demo URL**:
   `https://<your-service>.onrender.com` (or your Vercel URL)
2. **API Documentation (Swagger UI)**:
   `https://<your-service>.onrender.com/docs`
3. **GitHub Repository**:
   `https://github.com/<your-username>/<repo-name>`
4. **Key Features to Test**:
   - 🦺 **Safety Monitoring**: Upload `sample_data/site_photo.jpg` to detect PPE and site hazards.
   - 🔍 **Crack Detection**: Upload `sample_data/crack_sample.jpg` to classify crack type and severity.
   - 🏠 **Valuation**: Calculate real-estate estimates with Indian market pricing.
   - 📅 **Planning**: Generate multi-phase construction schedules and risk registers.
   - 🌤️ **Daily Site Assistant**: View live weather advisories for concrete pouring, painting, and cranes.
   - 💬 **Code Assistant**: Query Indian Standards (IS 456, IS 800, NBC 2016).
