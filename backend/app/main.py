"""
Multimodal Construction Intelligence Platform — FastAPI Backend
"""
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.db import init_db
from app.routers import safety, cracks, valuation, planning, assistant, history, settings as settings_router

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()


# ── Lifespan ──────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🏗️  Starting Construction Intelligence Platform...")
    # Create uploads directory
    uploads_path = Path(settings.uploads_dir)
    uploads_path.mkdir(parents=True, exist_ok=True)
    # Initialize database
    await init_db()
    logger.info("✅ Database initialized")
    logger.info(f"✅ Uploads directory: {settings.uploads_dir}")
    logger.info(f"✅ Gemini model: {settings.gemini_model}")
    logger.info(f"✅ AI API key configured: {settings.has_valid_api_key}")
    yield
    logger.info("🛑 Shutting down...")


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Multimodal Construction Intelligence Platform",
    description="AI-powered decision-support system for construction professionals",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── Static Uploads Mount ──────────────────────────────────────────────────────
uploads_dir_path = Path(settings.uploads_dir)
uploads_dir_path.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir_path)), name="uploads")

# ── CORS ──────────────────────────────────────────────────────────────────────
origins = settings.allowed_origins_list + ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
if "*" in origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=r"https://.*\.vercel\.app|https://.*\.onrender\.com|https://.*\.netlify\.app",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(safety.router)
app.include_router(cracks.router)
app.include_router(valuation.router)
app.include_router(planning.router)
app.include_router(assistant.router)
app.include_router(history.router)
app.include_router(settings_router.router)


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["Health"])
async def health_check():
    current_settings = get_settings()
    is_valid = current_settings.has_valid_api_key
    return {
        "status": "healthy",
        "version": "1.0.0",
        "platform": "Multimodal Construction Intelligence Platform",
        "gemini_model": current_settings.gemini_model,
        "ai_key_configured": is_valid,
        "mode": "live" if is_valid else "demo_simulation",
    }


# ── Frontend Static Files / SPA Support ────────────────────────────────────────
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if not frontend_dist.exists():
    frontend_dist = Path(__file__).resolve().parent.parent / "dist"

if frontend_dist.exists() and (frontend_dist / "index.html").exists():
    if (frontend_dist / "assets").exists():
        app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}", tags=["Frontend"])
    async def serve_spa(full_path: str = ""):
        # Do not intercept API, docs, or uploads
        if full_path.startswith(("api/", "docs", "redoc", "openapi.json", "uploads/")):
            return JSONResponse(status_code=404, content={"detail": "Not found"})
        target_file = frontend_dist / full_path
        if full_path and target_file.is_file():
            return FileResponse(target_file)
        return FileResponse(frontend_dist / "index.html")
else:
    @app.get("/", tags=["Root"])
    async def root():
        return {
            "message": "Multimodal Construction Intelligence Platform API",
            "docs": "/docs",
            "health": "/api/health",
            "mode": "live" if get_settings().has_valid_api_key else "demo_simulation",
        }
