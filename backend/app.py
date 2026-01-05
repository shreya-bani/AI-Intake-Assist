from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
import uvicorn


# Create FastAPI application
app = FastAPI(
    title="AI Intake Assistant API",
    description="Healthcare intake assistant with natural conversation and progressive form filling",
    version="1.0.0",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Intake Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "provider": settings.LLM_PROVIDER,
        "model": settings.MODEL_NAME
    }


# Import and include API routes
try:
    from api.routes import router as api_router
    app.include_router(api_router, prefix="/api")
except ImportError:
    print("Warning: API routes not yet implemented")


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
