import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import init_db
from routers import sentinel_router, companion_router, detector_router, dashboard_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Asynchronous Database Tables
    await init_db()
    yield
    # Shutdown: Clean up resources if necessary

app = FastAPI(
    title=settings.app_name,
    description="Next-Generation Child Safety & Digital Wellness Ecosystem for AI Hackathon",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Assets (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 Template Engine
templates = Jinja2Templates(directory="templates")

# Include Modular API Routers
app.include_router(sentinel_router.router)
app.include_router(companion_router.router)
app.include_router(detector_router.router)
app.include_router(dashboard_router.router)

# ==================== Frontend Page Routes ====================

@app.get("/")
async def render_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "app_name": settings.app_name})

@app.get("/sentinel")
async def render_sentinel(request: Request):
    return templates.TemplateResponse("sentinel.html", {"request": request, "app_name": settings.app_name})

@app.get("/companion")
async def render_companion(request: Request):
    return templates.TemplateResponse("companion.html", {"request": request, "app_name": settings.app_name})

@app.get("/detector")
async def render_detector(request: Request):
    return templates.TemplateResponse("detector.html", {"request": request, "app_name": settings.app_name})

@app.get("/dashboard")
async def render_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "app_name": settings.app_name})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)