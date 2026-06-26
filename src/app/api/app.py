from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.jobs import router as jobs_router
from app.api.routes.files import router as files_router
from app.api.routes.live_jobs import router as live_jobs_router
from app.config.settings import settings

def create_app() -> FastAPI:
    # Ensure all data directories exist
    settings.ensure_dirs()
    
    app = FastAPI(
        title="Karaoke Separation API",
        description="Local Dev API for YouTube to Karaoke audio separation",
        version="0.1.0"
    )
    
    # Add local CORS middleware for local frontend development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount routers under /api
    app.include_router(jobs_router, prefix="/api")
    app.include_router(files_router, prefix="/api")
    app.include_router(live_jobs_router, prefix="/api")
    
    @app.get("/")
    def read_root() -> dict:
        return {
            "name": "Karaoke Separation API",
            "status": "healthy",
            "version": "0.1.0"
        }
        
    return app
