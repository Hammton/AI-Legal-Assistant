from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    logger.info("Starting Legal Document Verification Agent API")
    yield
    logger.info("Shutting down API")


app = FastAPI(
    title="Legal Document Verification Agent API",
    description="AI-powered document verification for legal operations",
    version="0.1.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Legal Document Verification Agent",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "checks": {
            "api": "ok",
            # Add more checks as needed (database, LLM, etc.)
        }
    }


# Import and include routers
from app.api.routes import agent
app.include_router(agent.router, prefix="/api/v1/agent", tags=["agent"])
