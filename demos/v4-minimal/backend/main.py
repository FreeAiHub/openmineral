from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import uvicorn

# Simple in-memory storage
app = FastAPI(
    title="OpenMineral Minimal Demo API",
    description="Minimal working demo of commodity trading platform",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class DealCreate(BaseModel):
    title: str
    description: str
    commodity: str
    quantity: float
    price: float
    counterparty: str

class Deal(DealCreate):
    id: int
    status: str
    created_at: datetime

class MarketData(BaseModel):
    commodity: str
    price: float
    change: float
    volume: float
    timestamp: datetime

# In-memory storage
USERS = {
    "demo": {
        "username": "demo",
        "password": "demo123",
        "email": "demo@openmineral.com",
        "full_name": "Demo User"
    },
    "trader": {
        "username": "trader", 
        "password": "trader123",
        "email": "trader@openmineral.com",
        "full_name": "Mineral Trader"
    }
}

DEALS = [
    {
        "id": 1,
        "title": "Iron Ore Purchase Agreement",
        "description": "Purchase of iron ore from Brazilian supplier",
        "commodity": "Iron Ore",
        "quantity": 10000.0,
        "price": 85.50,
        "counterparty": "Brazilian Mining Corp",
        "status": "active",
        "created_at": datetime(2025, 9, 15, 10, 30, 0)
    },
    {
        "id": 2,
        "title": "Copper Sale Contract", 
        "description": "Sale of copper concentrate to European smelter",
        "commodity": "Copper",
        "quantity": 5000.0,
        "price": 9200.0,
        "counterparty": "European Copper Ltd",
        "status": "pending",
        "created_at": datetime(2025, 9, 10, 14, 15, 0)
    }
]

MARKET_DATA = [
    {
        "commodity": "Iron Ore",
        "price": 85.50,
        "change": 2.3,
        "volume": 150000.0,
        "timestamp": datetime.now()
    },
    {
        "commodity": "Copper",
        "price": 9200.0,
        "change": -1.2,
        "volume": 85000.0,
        "timestamp": datetime.now()
    },
    {
        "commodity": "Gold",
        "price": 1950.0,
        "change": 0.8,
        "volume": 12000.0,
        "timestamp": datetime.now()
    },
    {
        "commodity": "Silver",
        "price": 23.50,
        "change": 3.1,
        "volume": 25000.0,
        "timestamp": datetime.now()
    }
]

# Helper functions
def verify_password(username: str, password: str) -> bool:
    user = USERS.get(username)
    return user and user["password"] == password

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Simple token validation (in production use JWT)
    if token == "demo-token":
        return User(**USERS["demo"])
    elif token == "trader-token":
        return User(**USERS["trader"])
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Health check
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "0.1.0",
        "demo": "minimal",
        "timestamp": datetime.now()
    }

# Authentication
@app.post("/api/auth/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not verify_password(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Simple token (in production use JWT)
    token = f"{form_data.username}-token"
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Deals endpoints
@app.get("/api/deals", response_model=List[Deal])
async def get_deals(current_user: User = Depends(get_current_user)):
    return DEALS

@app.get("/api/deals/{deal_id}", response_model=Deal)
async def get_deal(deal_id: int, current_user: User = Depends(get_current_user)):
    for deal in DEALS:
        if deal["id"] == deal_id:
            return deal
    raise HTTPException(status_code=404, detail="Deal not found")

@app.post("/api/deals", response_model=Deal)
async def create_deal(deal: DealCreate, current_user: User = Depends(get_current_user)):
    new_deal = {
        "id": len(DEALS) + 1,
        "title": deal.title,
        "description": deal.description,
        "commodity": deal.commodity,
        "quantity": deal.quantity,
        "price": deal.price,
        "counterparty": deal.counterparty,
        "status": "draft",
        "created_at": datetime.now()
    }
    DEALS.append(new_deal)
    return new_deal

@app.put("/api/deals/{deal_id}", response_model=Deal)
async def update_deal(deal_id: int, deal: DealCreate, current_user: User = Depends(get_current_user)):
    for i, existing_deal in enumerate(DEALS):
        if existing_deal["id"] == deal_id:
            updated_deal = {
                **existing_deal,
                "title": deal.title,
                "description": deal.description,
                "commodity": deal.commodity,
                "quantity": deal.quantity,
                "price": deal.price,
                "counterparty": deal.counterparty,
            }
            DEALS[i] = updated_deal
            return updated_deal
    raise HTTPException(status_code=404, detail="Deal not found")

@app.delete("/api/deals/{deal_id}")
async def delete_deal(deal_id: int, current_user: User = Depends(get_current_user)):
    for i, deal in enumerate(DEALS):
        if deal["id"] == deal_id:
            DEALS.pop(i)
            return {"message": "Deal deleted successfully"}
    raise HTTPException(status_code=404, detail="Deal not found")

# Market data endpoints
@app.get("/api/market/prices", response_model=List[MarketData])
async def get_market_prices(current_user: User = Depends(get_current_user)):
    # Update timestamps to current time
    for item in MARKET_DATA:
        item["timestamp"] = datetime.now()
    return MARKET_DATA

@app.get("/api/market/analysis/{commodity}")
async def get_commodity_analysis(commodity: str, current_user: User = Depends(get_current_user)):
    return {
        "commodity": commodity,
        "analysis": f"Basic analysis for {commodity}: Market conditions are stable with moderate volatility.",
        "recommendations": ["Monitor price trends", "Consider position sizing"],
        "risk_factors": ["Market volatility", "Supply chain disruptions"]
    }

# Dashboard stats
@app.get("/api/dashboard/stats")
async def get_dashboard_stats(current_user: User = Depends(get_current_user)):
    active_deals = len([d for d in DEALS if d["status"] == "active"])
    pending_deals = len([d for d in DEALS if d["status"] == "pending"])
    
    return {
        "total_deals": len(DEALS),
        "active_deals": active_deals,
        "pending_deals": pending_deals,
        "completed_deals": len([d for d in DEALS if d["status"] == "completed"]),
        "total_value": sum(d["quantity"] * d["price"] for d in DEALS),
        "last_updated": datetime.now()
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)