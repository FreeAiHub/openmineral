"""
OpenMineral FastAPI Application
Main entry point for the trading platform API
"""

import sys
import os
from pathlib import Path

# Add root directory to Python path for imports
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import after sys.path fix
from config.settings import settings
from backend.routers import auth, deals, market, kyc, risk, workflow, bc_parser

app = FastAPI(
    title="OpenMineral Trading Platform API",
    description="AI-driven trading platform for mineral commodities with Chroma vector search",
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(deals.router, prefix="/api/deals", tags=["Deal Management"])
app.include_router(market.router, prefix="/api/market", tags=["Market Analysis"])
app.include_router(kyc.router, prefix="/api/kyc", tags=["KYC & Compliance"])
app.include_router(risk.router, prefix="/api/risk", tags=["Risk Assessment"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["Workflow Automation"])
app.include_router(bc_parser.router, prefix="/api/bc-parser", tags=["Business Confirmation Parser"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "OpenMineral Trading Platform API",
        "version": settings.app_version,
        "environment": settings.environment,
        "chroma_provider": settings.chroma_embedding_provider,
        "docs": "/docs" if settings.debug else None
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    from ai.chroma_service import get_chroma_service
    
    try:
        # Quick Chroma check
        service = get_chroma_service(is_test_mode=settings.testing)
        stats = service.get_collection_stats()
        chroma_status = "healthy" if stats["success"] else "degraded"
        
        return {
            "status": "healthy",
            "version": settings.app_version,
            "environment": settings.environment,
            "chroma_status": chroma_status,
            "chroma_vectors": stats["data"]["total_vectors"] if stats["success"] else 0,
            "debug": settings.debug,
            "testing": settings.testing
        }
    except Exception as e:
        return {
            "status": "degraded",
            "version": settings.app_version,
            "environment": settings.environment,
            "chroma_status": "unavailable",
            "error": str(e)[:100]
        }

@app.get("/api/chroma/test")
async def test_chroma():
    """Test Chroma connectivity"""
    from ai.chroma_service import get_chroma_service
    from ai.data_loader import DataLoader
    
    try:
        # Use test mode if TESTING=true
        test_mode = settings.testing
        
        service = get_chroma_service(is_test_mode=test_mode)
        
        # Load test data if needed
        if test_mode and settings.load_test_data:
            print("Loading test data...")
            DataLoader.load_all_data(test_mode=True)
        
        # Get stats
        stats = service.get_collection_stats()
        
        # Simple search test
        search_results = service.search_minerals("медь", n_results=1)
        
        return {
            "success": True,
            "test_mode": test_mode,
            "chroma_connected": stats["success"],
            "total_vectors": stats["data"]["total_vectors"] if stats["success"] else 0,
            "search_works": search_results["success"],
            "results_count": search_results["results_count"],
            "environment": stats["data"].get("environment", "unknown") if stats["success"] else "unknown"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "test_mode": settings.testing
        }

if __name__ == "__main__":
    print(f"🚀 Starting OpenMineral API")
    print(f"   Environment: {settings.environment}")
    print(f"   Debug: {settings.debug}")
    print(f"   Testing: {settings.testing}")
    print(f"   Port: {settings.port}")
    print(f"   Chroma: {'Local' if settings.testing else 'Cloud'}")
    
    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level="debug" if settings.debug else "info",
        access_log=settings.debug
    )
