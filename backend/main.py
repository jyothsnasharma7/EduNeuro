import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

from core.database import connect_to_mongo, close_mongo_connection
from routers import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB on startup
    await connect_to_mongo()
    yield
    # Close MongoDB connection on shutdown
    await close_mongo_connection()
    


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
    allow_origins=["*","localhost:3000"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
#app.include_router(users.router)
#app.include_router(analysis_router)
#app.include_router(monitoring.router)
#app.include_router(mitre.router)

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