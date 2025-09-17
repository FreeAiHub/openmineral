"""
Counterparty CRUD router for BC Flow
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import sys
import os

# Add root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from bc_flow.backend.models.base import Counterparty
from bc_flow.backend.schemas.base import CounterpartyCreate, CounterpartyUpdate, Counterparty as CounterpartySchema

router = APIRouter(prefix="/counterparties", tags=["Counterparties"])

# Mock database session for now
def get_db():
    # TODO: Implement proper database session
    return None

@router.get("/", response_model=List[CounterpartySchema])
async def get_counterparties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all counterparties"""
    # Mock data for now
    mock_counterparties = [
        CounterpartySchema(
            id=1,
            name="Brazilian Mining Corp",
            country="Brazil",
            kyc_status="approved",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z"
        ),
        CounterpartySchema(
            id=2,
            name="European Copper Ltd",
            country="Germany",
            kyc_status="pending",
            created_at="2024-01-02T00:00:00Z",
            updated_at="2024-01-02T00:00:00Z"
        )
    ]
    return mock_counterparties[skip:skip + limit]

@router.post("/", response_model=CounterpartySchema, status_code=status.HTTP_201_CREATED)
async def create_counterparty(counterparty: CounterpartyCreate, db: Session = Depends(get_db)):
    """Create a new counterparty"""
    # Mock creation
    return CounterpartySchema(
        id=3,
        name=counterparty.name,
        country=counterparty.country,
        kyc_status=counterparty.kyc_status,
        created_at="2024-01-03T00:00:00Z",
        updated_at="2024-01-03T00:00:00Z"
    )

@router.get("/{counterparty_id}", response_model=CounterpartySchema)
async def get_counterparty(counterparty_id: int, db: Session = Depends(get_db)):
    """Get a specific counterparty by ID"""
    # Mock data
    if counterparty_id == 1:
        return CounterpartySchema(
            id=1,
            name="Brazilian Mining Corp",
            country="Brazil",
            kyc_status="approved",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z"
        )
    raise HTTPException(status_code=404, detail="Counterparty not found")

@router.put("/{counterparty_id}", response_model=CounterpartySchema)
async def update_counterparty(
    counterparty_id: int,
    counterparty_update: CounterpartyUpdate,
    db: Session = Depends(get_db)
):
    """Update a counterparty"""
    # Mock update
    if counterparty_id == 1:
        return CounterpartySchema(
            id=1,
            name=counterparty_update.name or "Brazilian Mining Corp",
            country=counterparty_update.country or "Brazil",
            kyc_status=counterparty_update.kyc_status or "approved",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-03T00:00:00Z"
        )
    raise HTTPException(status_code=404, detail="Counterparty not found")

@router.delete("/{counterparty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_counterparty(counterparty_id: int, db: Session = Depends(get_db)):
    """Delete a counterparty"""
    # Mock deletion
    if counterparty_id == 1:
        return
    raise HTTPException(status_code=404, detail="Counterparty not found")
