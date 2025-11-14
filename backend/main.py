import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from routers import auth_router, tts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Using in-memory dictionaries for storage - no database connection needed
    yield
    


app = FastAPI(
    title="EduNeuro - ",
    description=" ",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

#cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(tts_router)
#app.include_router(users.router)
#app.include_router(analysis_router)
#app.include_router(monitoring.router)
#app.include_router(mitre.router)

# Mount static files for serving audio files
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
            "message": "LogIQ - MITRE ATT&CK Log Analysis API",
        "version": "1.0.0",
    "description": "AI-powered system log analysis with MITRE ATT&CK technique matching",
        "docs": "/docs",
        "health": "/health",
        "timestamp": datetime.utcnow().isoformat()
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000
    )