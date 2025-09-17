"""
BC Flow FastAPI Application
Main entry point for the Business Confirmation Flow API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routers
from bc_flow.backend.routers.counterparties import router as counterparties_router
from bc_flow.backend.routers.bc_flow import router as bc_flow_router

app = FastAPI(
    title="OpenMineral BC Flow API",
    description="Business Confirmation Flow API with AI-powered validation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(counterparties_router)
app.include_router(bc_flow_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "OpenMineral BC Flow API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "BC Flow API"
    }

if __name__ == "__main__":
    print("🚀 Starting BC Flow API")
    print("   Docs: http://localhost:8000/docs")
    uvicorn.run(
        "bc_flow.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
