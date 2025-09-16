from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import uvicorn
import asyncio
import random
import json
from pathlib import Path
import os

# Database setup
DATABASE_URL = "sqlite:///./openmineral_enhanced.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100))
    hashed_password = Column(String(255))
    full_name = Column(String(100))
    role = Column(String(20), default="trader")
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class DealDB(Base):
    __tablename__ = "deals"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    commodity = Column(String(50))
    quantity = Column(Float)
    price = Column(Float)
    counterparty = Column(String(100))
    status = Column(String(20), default="draft")
    user_id = Column(Integer)
    ai_analysis = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class AIAnalysisDB(Base):
    __tablename__ = "ai_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer)
    analysis_type = Column(String(50))  # deal, risk, market
    analysis_data = Column(Text)  # JSON string
    confidence = Column(Float)
    processing_time_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="OpenMineral Enhanced Mock Demo API",
    description="Enhanced demo with SQLite database and realistic AI responses",
    version="0.2.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str = "trader"

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
    ai_analysis: Optional[dict] = None

class AIAnalysisRequest(BaseModel):
    deal_id: int
    analysis_type: str = "deal"

class AIAnalysisResponse(BaseModel):
    analysis_id: int
    deal_id: int
    analysis_type: str
    market_assessment: str
    risk_score: float
    recommendations: List[str]
    confidence: float
    processing_time_ms: int
    ai_model: str
    timestamp: datetime

class MarketData(BaseModel):
    commodity: str
    price: float
    change: float
    volume: float
    timestamp: datetime

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database with demo data
def init_demo_data():
    db = SessionLocal()
    
    # Check if users exist
    if not db.query(UserDB).first():
        # Create demo users
        demo_users = [
            UserDB(
                username="demo",
                email="demo@openmineral.com", 
                hashed_password="demo123",  # In production, use proper hashing
                full_name="Demo User",
                role="demo"
            ),
            UserDB(
                username="trader",
                email="trader@openmineral.com",
                hashed_password="trader123",
                full_name="Mineral Trader", 
                role="trader"
            ),
            UserDB(
                username="analyst",
                email="analyst@openmineral.com",
                hashed_password="analyst123",
                full_name="Market Analyst",
                role="analyst"
            )
        ]
        for user in demo_users:
            db.add(user)
        
        # Create demo deals
        demo_deals = [
            DealDB(
                title="Iron Ore Purchase Agreement",
                description="Purchase of iron ore from Brazilian supplier",
                commodity="Iron Ore",
                quantity=10000.0,
                price=85.50,
                counterparty="Brazilian Mining Corp",
                status="active",
                user_id=1
            ),
            DealDB(
                title="Copper Sale Contract",
                description="Sale of copper concentrate to European smelter", 
                commodity="Copper",
                quantity=5000.0,
                price=9200.0,
                counterparty="European Copper Ltd",
                status="pending",
                user_id=1
            ),
            DealDB(
                title="Gold Forward Contract",
                description="Forward purchase of gold bullion",
                commodity="Gold",
                quantity=100.0,
                price=1950.0,
                counterparty="Swiss Precious Metals",
                status="completed",
                user_id=2
            )
        ]
        for deal in demo_deals:
            db.add(deal)
            
        db.commit()
    db.close()

# Auth functions
def verify_password(username: str, password: str, db: Session):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    return user and user.hashed_password == password  # In production, use proper hashing

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # Simple token validation (in production use JWT)
    if token == "demo-token":
        user = db.query(UserDB).filter(UserDB.username == "demo").first()
    elif token == "trader-token":
        user = db.query(UserDB).filter(UserDB.username == "trader").first()
    elif token == "analyst-token":
        user = db.query(UserDB).filter(UserDB.username == "analyst").first()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    return User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role
    )

# Enhanced AI mock functions
async def enhanced_ai_deal_analysis(deal: DealDB) -> dict:
    """Enhanced mock AI analysis with realistic processing time and responses"""
    
    # Simulate AI processing time
    processing_start = datetime.utcnow()
    await asyncio.sleep(random.uniform(2.0, 4.5))  # Realistic AI processing delay
    processing_time = int((datetime.utcnow() - processing_start).total_seconds() * 1000)
    
    # Generate contextual analysis based on commodity and deal data
    commodity_context = {
        "Iron Ore": {
            "market_trends": [
                "Chinese steel production increasing by 3.2% this quarter",
                "Brazilian mine expansion projects delayed by weather",
                "Shipping costs from Brazil up 15% due to fuel prices"
            ],
            "risk_factors": [
                "Price volatility due to weather disruptions",
                "Chinese policy changes affecting demand",
                "Supply chain bottlenecks in shipping"
            ],
            "opportunities": [
                "Infrastructure spending boom in Asia", 
                "Green steel initiatives driving demand",
                "Strategic stockpiling by major consumers"
            ]
        },
        "Copper": {
            "market_trends": [
                "Electric vehicle demand driving copper prices",
                "Chile mining strikes affecting global supply",
                "Renewable energy projects increasing demand"
            ],
            "risk_factors": [
                "Political instability in major producing countries",
                "Environmental regulations tightening",
                "Substitution risks from aluminum"
            ],
            "opportunities": [
                "5G infrastructure rollout",
                "Energy storage system growth",
                "Smart city development projects"
            ]
        },
        "Gold": {
            "market_trends": [
                "Central bank buying increased 152% YoY",
                "Dollar weakness supporting gold prices",
                "Inflation hedging demand rising"
            ],
            "risk_factors": [
                "Interest rate volatility",
                "Strong dollar scenarios",
                "ETF outflows during risk-on periods"
            ],
            "opportunities": [
                "Geopolitical uncertainty hedging",
                "Portfolio diversification demand",
                "Jewelry demand recovery in Asia"
            ]
        }
    }
    
    context = commodity_context.get(deal.commodity, {
        "market_trends": ["General market volatility observed"],
        "risk_factors": ["Standard commodity trading risks"],
        "opportunities": ["Market-specific opportunities available"]
    })
    
    # Calculate mock risk score based on deal parameters
    base_risk = 5.0
    quantity_risk = min(deal.quantity / 10000 * 2, 3.0)  # Higher quantity = higher risk
    price_volatility = random.uniform(0.5, 2.5)
    counterparty_risk = random.uniform(1.0, 3.0)
    
    total_risk = min(base_risk + quantity_risk + price_volatility + counterparty_risk, 10.0)
    
    # Generate recommendations based on risk level
    recommendations = []
    if total_risk > 7.0:
        recommendations = [
            "Consider reducing position size by 25-30%",
            "Implement hedging strategy immediately",
            "Require additional counterparty guarantees",
            "Monitor market conditions daily"
        ]
    elif total_risk > 5.0:
        recommendations = [
            "Moderate hedging recommended (50% coverage)",
            "Monitor counterparty credit rating",
            "Set stop-loss at 5% below entry price",
            "Review position weekly"
        ]
    else:
        recommendations = [
            "Position size appropriate for current market",
            "Standard monitoring procedures sufficient",
            "Consider scaling position if opportunity arises",
            "Maintain current risk parameters"
        ]
    
    return {
        "analysis_id": random.randint(10000, 99999),
        "deal_id": deal.id,
        "analysis_type": "comprehensive_deal_analysis",
        "market_assessment": f"Current {deal.commodity} market analysis reveals {random.choice(context['market_trends'])}. Trading conditions are {'favorable' if total_risk < 6 else 'challenging'} with moderate to {'low' if total_risk < 5 else 'high'} volatility expected.",
        "risk_score": round(total_risk, 2),
        "risk_level": "Low" if total_risk < 4 else "Medium" if total_risk < 7 else "High",
        "price_competitiveness": "Competitive" if abs(deal.price - random.uniform(deal.price * 0.95, deal.price * 1.05)) < deal.price * 0.02 else "Review needed",
        "recommendations": recommendations,
        "market_factors": {
            "trends": context["market_trends"][:2],
            "risks": context["risk_factors"][:2], 
            "opportunities": context["opportunities"][:1]
        },
        "confidence": round(random.uniform(0.75, 0.95), 3),
        "processing_time_ms": processing_time,
        "ai_model": "Enhanced Mock AI v2.0",
        "timestamp": datetime.utcnow(),
        "next_review_date": datetime.utcnow() + timedelta(days=7)
    }

# API Endpoints
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "0.2.0", 
        "demo": "enhanced-mock",
        "database": "sqlite",
        "ai_mode": "enhanced_mock",
        "timestamp": datetime.utcnow()
    }

@app.post("/api/auth/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if not verify_password(form_data.username, form_data.password, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Simple token generation (in production use JWT)
    token = f"{form_data.username}-token"
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/api/deals", response_model=List[Deal])
async def get_deals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deals = db.query(DealDB).all()
    result = []
    for deal in deals:
        ai_analysis = None
        if deal.ai_analysis:
            try:
                ai_analysis = json.loads(deal.ai_analysis)
            except:
                pass
        
        result.append(Deal(
            id=deal.id,
            title=deal.title,
            description=deal.description,
            commodity=deal.commodity,
            quantity=deal.quantity,
            price=deal.price,
            counterparty=deal.counterparty,
            status=deal.status,
            created_at=deal.created_at,
            ai_analysis=ai_analysis
        ))
    return result

@app.get("/api/deals/{deal_id}", response_model=Deal)
async def get_deal(deal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deal = db.query(DealDB).filter(DealDB.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    ai_analysis = None
    if deal.ai_analysis:
        try:
            ai_analysis = json.loads(deal.ai_analysis)
        except:
            pass
    
    return Deal(
        id=deal.id,
        title=deal.title,
        description=deal.description,
        commodity=deal.commodity,
        quantity=deal.quantity,
        price=deal.price,
        counterparty=deal.counterparty,
        status=deal.status,
        created_at=deal.created_at,
        ai_analysis=ai_analysis
    )

@app.post("/api/deals", response_model=Deal)
async def create_deal(deal: DealCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_deal = DealDB(
        title=deal.title,
        description=deal.description,
        commodity=deal.commodity,
        quantity=deal.quantity,
        price=deal.price,
        counterparty=deal.counterparty,
        status="draft",
        user_id=1  # Simplified for demo
    )
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    
    return Deal(
        id=db_deal.id,
        title=db_deal.title,
        description=db_deal.description,
        commodity=db_deal.commodity,
        quantity=db_deal.quantity,
        price=db_deal.price,
        counterparty=db_deal.counterparty,
        status=db_deal.status,
        created_at=db_deal.created_at
    )

@app.post("/api/deals/{deal_id}/ai-analysis", response_model=AIAnalysisResponse)
async def analyze_deal_with_ai(
    deal_id: int, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Enhanced AI analysis with realistic processing and responses"""
    deal = db.query(DealDB).filter(DealDB.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    # Generate enhanced AI analysis
    analysis_result = await enhanced_ai_deal_analysis(deal)
    
    # Save analysis to database
    ai_analysis_db = AIAnalysisDB(
        deal_id=deal_id,
        analysis_type="deal",
        analysis_data=json.dumps(analysis_result),
        confidence=analysis_result["confidence"],
        processing_time_ms=analysis_result["processing_time_ms"]
    )
    db.add(ai_analysis_db)
    
    # Update deal with analysis
    deal.ai_analysis = json.dumps(analysis_result)
    deal.updated_at = datetime.utcnow()
    
    db.commit()
    
    return AIAnalysisResponse(**analysis_result)

@app.get("/api/market/prices", response_model=List[MarketData])
async def get_market_prices(current_user: User = Depends(get_current_user)):
    # Enhanced mock market data with realistic fluctuations
    base_prices = {
        "Iron Ore": 85.50,
        "Copper": 9200.0,
        "Gold": 1950.0,
        "Silver": 23.50,
        "Zinc": 2850.0,
        "Aluminum": 2340.0
    }
    
    market_data = []
    for commodity, base_price in base_prices.items():
        # Add realistic price fluctuation
        price_change = random.uniform(-3.0, 3.0)
        current_price = base_price * (1 + price_change / 100)
        volume = random.uniform(50000, 200000)
        
        market_data.append(MarketData(
            commodity=commodity,
            price=round(current_price, 2),
            change=round(price_change, 2),
            volume=round(volume, 0),
            timestamp=datetime.utcnow()
        ))
    
    return market_data

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_deals = db.query(DealDB).count()
    active_deals = db.query(DealDB).filter(DealDB.status == "active").count()
    pending_deals = db.query(DealDB).filter(DealDB.status == "pending").count()
    completed_deals = db.query(DealDB).filter(DealDB.status == "completed").count()
    
    # Calculate total portfolio value
    deals = db.query(DealDB).all()
    total_value = sum(deal.quantity * deal.price for deal in deals)
    
    return {
        "total_deals": total_deals,
        "active_deals": active_deals,
        "pending_deals": pending_deals,
        "completed_deals": completed_deals,
        "total_value": round(total_value, 2),
        "last_updated": datetime.utcnow(),
        "performance_metrics": {
            "avg_deal_size": round(total_value / max(total_deals, 1), 2),
            "success_rate": round((completed_deals / max(total_deals, 1)) * 100, 1),
            "pending_rate": round((pending_deals / max(total_deals, 1)) * 100, 1)
        }
    }

# Initialize demo data on startup
@app.on_event("startup")
async def startup_event():
    init_demo_data()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)