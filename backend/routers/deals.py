from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel
from datetime import datetime

from routers.auth import get_current_active_user
from models.user import User

router = APIRouter()

# Data models
class DealBase(BaseModel):
    title: str
    description: str
    commodity: str
    quantity: float
    price: float
    counterparty: str

class DealCreate(DealBase):
    pass

class DealUpdate(DealBase):
    status: str | None = None

class Deal(DealBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Mock data storage
deals_db = [
    {
        "id": 1,
        "title": "Iron Ore Purchase Agreement",
        "description": "Purchase of iron ore from Brazilian supplier",
        "commodity": "Iron Ore",
        "quantity": 10000.0,
        "price": 85.50,
        "counterparty": "Brazilian Mining Corp",
        "status": "active",
        "created_at": datetime(2025, 9, 15, 10, 30, 0),
        "updated_at": datetime(2025, 9, 15, 10, 30, 0)
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
        "created_at": datetime(2025, 9, 10, 14, 15, 0),
        "updated_at": datetime(2025, 9, 12, 9, 45, 0)
    }
]

# Endpoints
@router.get("/", response_model=List[Deal])
async def get_deals(current_user: User = Depends(get_current_active_user)):
    """Get all deals"""
    return deals_db

@router.get("/{deal_id}", response_model=Deal)
async def get_deal(deal_id: int, current_user: User = Depends(get_current_active_user)):
    """Get a specific deal by ID"""
    for deal in deals_db:
        if deal["id"] == deal_id:
            return deal
    raise HTTPException(status_code=404, detail="Deal not found")

@router.post("/", response_model=Deal)
async def create_deal(deal: DealCreate, current_user: User = Depends(get_current_active_user)):
    """Create a new deal"""
    new_deal = {
        "id": len(deals_db) + 1,
        "title": deal.title,
        "description": deal.description,
        "commodity": deal.commodity,
        "quantity": deal.quantity,
        "price": deal.price,
        "counterparty": deal.counterparty,
        "status": "draft",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    deals_db.append(new_deal)
    return new_deal

@router.put("/{deal_id}", response_model=Deal)
async def update_deal(deal_id: int, deal: DealUpdate, current_user: User = Depends(get_current_active_user)):
    """Update an existing deal"""
    for i, existing_deal in enumerate(deals_db):
        if existing_deal["id"] == deal_id:
            updated_deal = existing_deal.copy()
            updated_deal.update({
                "title": deal.title,
                "description": deal.description,
                "commodity": deal.commodity,
                "quantity": deal.quantity,
                "price": deal.price,
                "counterparty": deal.counterparty,
                "updated_at": datetime.now()
            })
            if deal.status:
                updated_deal["status"] = deal.status
            deals_db[i] = updated_deal
            return updated_deal
    raise HTTPException(status_code=404, detail="Deal not found")

@router.delete("/{deal_id}")
async def delete_deal(deal_id: int, current_user: User = Depends(get_current_active_user)):
    """Delete a deal"""
    for i, deal in enumerate(deals_db):
        if deal["id"] == deal_id:
            deals_db.pop(i)
            return {"message": "Deal deleted successfully"}
    raise HTTPException(status_code=404, detail="Deal not found")