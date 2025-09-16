from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from config.settings import settings
from routers import auth, deals, market, kyc, risk, workflow

app = FastAPI(
    title="OpenMineralHub Trading Platform API",
    description="AI-driven trading platform for mineral commodities",
    version="0.1.0"
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
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(deals.router, prefix="/api/deals", tags=["Deal Management"])
app.include_router(market.router, prefix="/api/market", tags=["Market Analysis"])
app.include_router(kyc.router, prefix="/api/kyc", tags=["KYC & Compliance"])
app.include_router(risk.router, prefix="/api/risk", tags=["Risk Assessment"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["Workflow Automation"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
