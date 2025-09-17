"""
BC Flow router for multi-step business confirmation form
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import time
import uuid
import sys
import os

# Add root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from bc_flow.backend.schemas.base import (
    BCFormData,
    BCValidationResponse,
    DealBasics,
    CommercialTerms,
    PaymentTerms
)

router = APIRouter(prefix="/bc-flow", tags=["BC Flow"])

# Mock AI suggestions database
MOCK_AI_SUGGESTIONS = {
    "rc_ag": {
        "threshold": 5.0,
        "suggestion": "Your RC is higher than market average. Consider lowering to $4.50/oz"
    },
    "tc": {
        "threshold": 350.0,
        "suggestion": "Treatment charge is 15% higher than last month. Review pricing"
    },
    "surveyor": {
        "missing": "Surveyor not selected. Recommended: Intertek or SGS"
    }
}

@router.post("/validate/step1", response_model=BCValidationResponse)
async def validate_deal_basics(deal_basics: DealBasics):
    """Validate Step 1: Deal Basics"""
    suggestions = []
    warnings = []

    # Basic validations
    if deal_basics.quantity <= 0:
        warnings.append("Quantity must be greater than 0")

    if deal_basics.quantity_tolerance > 20:
        suggestions.append("High tolerance may affect pricing. Consider 10-15%")

    # Mock AI suggestions
    if "copper" in deal_basics.material.lower():
        suggestions.append("Copper concentrate typically requires specialized packaging")

    return BCValidationResponse(
        is_valid=len(warnings) == 0,
        suggestions=suggestions,
        warnings=warnings
    )

@router.post("/validate/step2", response_model=BCValidationResponse)
async def validate_commercial_terms(commercial_terms: CommercialTerms):
    """Validate Step 2: Commercial Terms"""
    suggestions = []
    warnings = []

    # Basic validations
    if commercial_terms.tc_usd_per_dmt <= 0:
        warnings.append("Treatment charge must be greater than 0")

    if commercial_terms.rc_ag_usd_per_toz <= 0:
        warnings.append("Refining charge must be greater than 0")

    # AI suggestions based on mock data
    if commercial_terms.rc_ag_usd_per_toz > MOCK_AI_SUGGESTIONS["rc_ag"]["threshold"]:
        suggestions.append(MOCK_AI_SUGGESTIONS["rc_ag"]["suggestion"])

    if commercial_terms.tc_usd_per_dmt > MOCK_AI_SUGGESTIONS["tc"]["threshold"]:
        suggestions.append(MOCK_AI_SUGGESTIONS["tc"]["suggestion"])

    # Delivery mode logic
    if commercial_terms.delivery_mode.lower() == "rail":
        if "bulk" not in commercial_terms.packaging.lower():
            suggestions.append("Rail transport typically uses bulk packaging")
    elif commercial_terms.delivery_mode.lower() == "ship":
        if "big bags" in commercial_terms.packaging.lower():
            suggestions.append("Ship transport typically uses bulk, not big bags")

    return BCValidationResponse(
        is_valid=len(warnings) == 0,
        suggestions=suggestions,
        warnings=warnings
    )

@router.post("/validate/step3", response_model=BCValidationResponse)
async def validate_payment_terms(payment_terms: PaymentTerms):
    """Validate Step 3: Payment Terms"""
    suggestions = []
    warnings = []

    # Basic validations
    total_percentage = (
        payment_terms.prepayment_percentage +
        payment_terms.provisional_percentage +
        payment_terms.final_percentage
    )

    if total_percentage != 100:
        warnings.append(f"Payment percentages must total 100%. Current: {total_percentage}%")

    if payment_terms.prepayment_percentage > 50:
        suggestions.append("High prepayment may require additional credit checks")

    # Surveyor validation
    if not payment_terms.surveyor or payment_terms.surveyor.lower() == "lorem ipsum":
        suggestions.append(MOCK_AI_SUGGESTIONS["surveyor"]["missing"])

    return BCValidationResponse(
        is_valid=len(warnings) == 0,
        suggestions=suggestions,
        warnings=warnings
    )

@router.post("/validate/all", response_model=BCValidationResponse)
async def validate_complete_form(form_data: BCFormData):
    """Validate complete BC form"""
    all_suggestions = []
    all_warnings = []

    # Validate each step
    step1_validation = await validate_deal_basics(form_data.deal_basics)
    step2_validation = await validate_commercial_terms(form_data.commercial_terms)
    step3_validation = await validate_payment_terms(form_data.payment_terms)

    # Combine results
    all_suggestions.extend(step1_validation.suggestions)
    all_suggestions.extend(step2_validation.suggestions)
    all_suggestions.extend(step3_validation.suggestions)

    all_warnings.extend(step1_validation.warnings)
    all_warnings.extend(step2_validation.warnings)
    all_warnings.extend(step3_validation.warnings)

    return BCValidationResponse(
        is_valid=len(all_warnings) == 0,
        suggestions=all_suggestions,
        warnings=all_warnings
    )

@router.post("/submit")
async def submit_bc_form(
    form_data: BCFormData,
    background_tasks: BackgroundTasks
):
    """Submit BC form with background processing"""
    # Generate task ID
    task_id = str(uuid.uuid4())

    # Add background task
    background_tasks.add_task(process_bc_submission, task_id, form_data)

    return {
        "task_id": task_id,
        "status": "processing",
        "message": "BC form submitted for processing"
    }

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """Get background task status"""
    # Mock task status (in real app, this would check database/redis)
    return {
        "task_id": task_id,
        "status": "completed",
        "result": "BC form processed successfully",
        "processing_time": 15
    }

async def process_bc_submission(task_id: str, form_data: BCFormData):
    """Background task to process BC submission"""
    # Simulate processing time
    time.sleep(15)

    # Mock processing result
    result = {
        "task_id": task_id,
        "status": "completed",
        "processed_data": {
            "seller": form_data.deal_basics.seller,
            "buyer": form_data.deal_basics.buyer,
            "material": form_data.deal_basics.material,
            "quantity": form_data.deal_basics.quantity,
            "tc": form_data.commercial_terms.tc_usd_per_dmt,
            "rc_ag": form_data.commercial_terms.rc_ag_usd_per_toz
        },
        "confirmation_number": f"BC-{task_id[:8].upper()}",
        "timestamp": "2024-01-15T10:30:00Z"
    }

    # In real app, save to database
    print(f"BC Processing completed: {result}")

    return result

@router.get("/dropdown-data")
async def get_dropdown_data():
    """Get data for dropdowns from database"""
    return {
        "materials": [
            "Copper Concentrate",
            "Lead Concentrate",
            "Zinc Concentrate",
            "Iron Ore",
            "Gold Ore",
            "Silver Ore"
        ],
        "delivery_terms": [
            "FOB",
            "CIF",
            "DAP",
            "DDP",
            "EXW"
        ],
        "delivery_modes": [
            "Rail",
            "Ship",
            "Truck",
            "Air"
        ],
        "packaging_options": {
            "rail": ["Bulk", "Big Bags"],
            "ship": ["Bulk"],
            "truck": ["Bulk", "Big Bags", "Drums"],
            "air": ["Drums", "Small Bags"]
        },
        "currencies": ["USD", "EUR", "GBP", "JPY"],
        "surveyors": [
            "Intertek",
            "SGS",
            "Bureau Veritas",
            "ALS Global",
            "Alex Stewart"
        ]
    }
