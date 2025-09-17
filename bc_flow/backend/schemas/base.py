"""
Pydantic schemas for BC Flow API
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Counterparty schemas
class CounterpartyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=50)
    kyc_status: str = Field(default="pending", regex="^(pending|approved|rejected)$")

class CounterpartyCreate(CounterpartyBase):
    pass

class CounterpartyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    country: Optional[str] = Field(None, min_length=1, max_length=50)
    kyc_status: Optional[str] = Field(None, regex="^(pending|approved|rejected)$")

class Counterparty(CounterpartyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Commodity schemas
class CommodityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    unit: str = Field(default="MT", min_length=1, max_length=20)

class CommodityCreate(CommodityBase):
    pass

class CommodityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    unit: Optional[str] = Field(None, min_length=1, max_length=20)

class Commodity(CommodityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Trade schemas
class TradeBase(BaseModel):
    counterparty_id: int = Field(..., gt=0)
    commodity_id: int = Field(..., gt=0)
    quantity: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    status: str = Field(default="draft", regex="^(draft|pending|active|completed)$")

class TradeCreate(TradeBase):
    pass

class TradeUpdate(BaseModel):
    counterparty_id: Optional[int] = Field(None, gt=0)
    commodity_id: Optional[int] = Field(None, gt=0)
    quantity: Optional[float] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[str] = Field(None, regex="^(draft|pending|active|completed)$")

class Trade(TradeBase):
    id: int
    trade_date: datetime
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Task schemas
class TaskBase(BaseModel):
    task_id: str = Field(..., min_length=1, max_length=100)
    status: str = Field(default="pending", regex="^(pending|processing|completed|failed)$")
    result: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    status: Optional[str] = Field(None, regex="^(pending|processing|completed|failed)$")
    result: Optional[str] = None

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# BC Flow specific schemas for multi-step form
class DealBasics(BaseModel):
    seller: str = Field(default="Open Mineral")
    buyer: str = Field(..., min_length=1)
    material: str = Field(..., min_length=1)
    quantity: float = Field(..., gt=0)
    quantity_tolerance: float = Field(default=10.0, ge=0, le=50)

class CommercialTerms(BaseModel):
    delivery_term: str = Field(..., min_length=1)
    delivery_point: str = Field(..., min_length=1)
    delivery_mode: str = Field(..., min_length=1)
    shipment_period: str = Field(..., min_length=1)
    packaging: str = Field(..., min_length=1)
    assay_data: dict = Field(default_factory=dict)  # Zn, Pb, Ag, etc.
    tc_usd_per_dmt: float = Field(..., ge=0)
    rc_ag_usd_per_toz: float = Field(..., ge=0)
    transportation_credit: bool = Field(default=False)
    other_payables: str = Field(default="")

class PaymentTerms(BaseModel):
    payment_method: str = Field(..., min_length=1)
    currency: str = Field(default="USD")
    prepayment_percentage: int = Field(..., ge=0, le=100)
    provisional_percentage: int = Field(..., ge=0, le=100)
    final_percentage: int = Field(..., ge=0, le=100)
    wsmd_location: str = Field(..., min_length=1)
    cost_sharing_percentage: int = Field(default=50, ge=0, le=100)
    surveyor: str = Field(..., min_length=1)

class BCFormData(BaseModel):
    deal_basics: DealBasics
    commercial_terms: CommercialTerms
    payment_terms: PaymentTerms

class BCValidationResponse(BaseModel):
    is_valid: bool
    suggestions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
