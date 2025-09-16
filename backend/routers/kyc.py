from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime

from routers.auth import get_current_active_user
from models.user import User

router = APIRouter()

# Data models
class KYCRequest(BaseModel):
    user_id: int
    full_name: str
    date_of_birth: str
    nationality: str
    address: str
    identification_type: str
    identification_number: str

class KYCStatus(BaseModel):
    user_id: int
    status: str  # pending, approved, rejected
    risk_level: str  # low, medium, high
    last_updated: datetime
    notes: str | None = None

class ComplianceCheck(BaseModel):
    deal_id: int
    regulations: List[str]
    status: str  # compliant, non-compliant, pending
    violations: List[str] | None = None
    checked_by: str
    checked_at: datetime

# Mock data
kyc_db = [
    {
        "user_id": 1,
        "status": "approved",
        "risk_level": "low",
        "last_updated": datetime(2025, 9, 10, 14, 30, 0),
        "notes": "Standard verification completed"
    },
    {
        "user_id": 2,
        "status": "pending",
        "risk_level": "medium",
        "last_updated": datetime(2025, 9, 15, 9, 15, 0),
        "notes": "Additional documentation required"
    }
]

compliance_db = [
    {
        "deal_id": 1,
        "regulations": ["IMCO Maritime Law", "EU Sanctions List"],
        "status": "compliant",
        "violations": None,
        "checked_by": "compliance@openmineral.com",
        "checked_at": datetime(2025, 9, 15, 11, 0, 0)
    }
]

# Endpoints
@router.post("/kyc/request")
async def submit_kyc_request(kyc_request: KYCRequest, current_user: User = Depends(get_current_active_user)):
    """Submit a new KYC request"""
    # In a real implementation, this would trigger verification processes
    return {
        "message": "KYC request submitted successfully",
        "request_id": f"kyc_{kyc_request.user_id}_{int(datetime.now().timestamp())}",
        "status": "pending"
    }

@router.get("/kyc/status/{user_id}", response_model=KYCStatus)
async def get_kyc_status(user_id: int, current_user: User = Depends(get_current_active_user)):
    """Get KYC status for a user"""
    for kyc in kyc_db:
        if kyc["user_id"] == user_id:
            return kyc
    raise HTTPException(status_code=404, detail="KYC record not found")

@router.post("/compliance/check")
async def check_compliance(compliance_check: ComplianceCheck, current_user: User = Depends(get_current_active_user)):
    """Perform a compliance check on a deal"""
    # In a real implementation, this would check against various regulations
    compliance_db.append(compliance_check.dict())
    return {
        "message": "Compliance check completed",
        "deal_id": compliance_check.deal_id,
        "status": compliance_check.status
    }

@router.get("/compliance/deal/{deal_id}", response_model=ComplianceCheck)
async def get_compliance_check(deal_id: int, current_user: User = Depends(get_current_active_user)):
    """Get compliance check results for a deal"""
    for compliance in compliance_db:
        if compliance["deal_id"] == deal_id:
            return compliance
    raise HTTPException(status_code=404, detail="Compliance check not found")