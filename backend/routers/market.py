from fastapi import APIRouter, Depends
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime

from routers.auth import get_current_active_user
from models.user import User

router = APIRouter()

# Data models
class MarketData(BaseModel):
    commodity: str
    price: float
    change: float
    volume: float
    timestamp: datetime

class PriceForecast(BaseModel):
    commodity: str
    current_price: float
    forecast_price: float
    confidence: float
    timeframe: str

# Mock market data
market_data_db = [
    {
        "commodity": "Iron Ore",
        "price": 85.50,
        "change": 2.3,
        "volume": 150000.0,
        "timestamp": datetime(2025, 9, 16, 10, 0, 0)
    },
    {
        "commodity": "Copper",
        "price": 9200.0,
        "change": -1.2,
        "volume": 85000.0,
        "timestamp": datetime(2025, 9, 16, 10, 0, 0)
    },
    {
        "commodity": "Gold",
        "price": 1950.0,
        "change": 0.8,
        "volume": 12000.0,
        "timestamp": datetime(2025, 9, 16, 10, 0, 0)
    },
    {
        "commodity": "Silver",
        "price": 23.50,
        "change": 3.1,
        "volume": 25000.0,
        "timestamp": datetime(2025, 9, 16, 10, 0, 0)
    }
]

# Mock price forecasts
price_forecasts_db = [
    {
        "commodity": "Iron Ore",
        "current_price": 85.50,
        "forecast_price": 88.20,
        "confidence": 0.75,
        "timeframe": "30 days"
    },
    {
        "commodity": "Copper",
        "current_price": 9200.0,
        "forecast_price": 9100.0,
        "confidence": 0.68,
        "timeframe": "30 days"
    }
]

# Endpoints
@router.get("/prices", response_model=List[MarketData])
async def get_market_prices(current_user: User = Depends(get_current_active_user)):
    """Get current market prices for commodities"""
    return market_data_db

@router.get("/forecasts", response_model=List[PriceForecast])
async def get_price_forecasts(current_user: User = Depends(get_current_active_user)):
    """Get AI-generated price forecasts"""
    return price_forecasts_db

@router.get("/analysis/{commodity}")
async def get_commodity_analysis(commodity: str, current_user: User = Depends(get_current_active_user)):
    """Get detailed AI analysis for a specific commodity"""
    # In a real implementation, this would call AI models
    for data in market_data_db:
        if data["commodity"].lower() == commodity.lower():
            return {
                "commodity": commodity,
                "analysis": f"Detailed AI analysis for {commodity} market trends",
                "recommendations": ["Hold position", "Monitor supply chain disruptions"],
                "risk_factors": ["Geopolitical tensions", "Weather patterns"]
            }
    return {"commodity": commodity, "analysis": "No data available", "recommendations": [], "risk_factors": []}