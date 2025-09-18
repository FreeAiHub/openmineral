from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from decimal import Decimal
from datetime import datetime, date
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OpenMineral BC Flow API",
    description="Production-grade Business Confirmation Flow for Commodity Trading",
    version="1.0.0"
)

# CORS with proper security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Trading domain models
class DealBasics(BaseModel):
    seller: str = Field(..., min_length=1, max_length=100)
    buyer: str = Field(..., min_length=1, max_length=100)
    material: str = Field(..., min_length=1, max_length=50)
    quantity: float = Field(..., gt=0, description="Quantity in MT")
    quantityTolerance: float = Field(default=10, ge=0, le=20, description="Tolerance percentage")

class CommercialTerms(BaseModel):
    deliveryTerm: str = Field(..., pattern="^(CIF|FOB|CFR|EXW|DDP|DAP)$")
    deliveryPoint: str = Field(..., min_length=1)
    deliveryMode: str = Field(..., pattern="^(Ship|Rails|Truck|Pipeline)$")
    shipmentPeriod: str = Field(..., min_length=1)
    packaging: str = Field(..., pattern="^(Bulk|Big Bags|Containers|Tank)$")
    tcUsdPerDmt: float = Field(..., ge=0, description="Treatment Charge USD/DMT")
    rcAgUsdPerToz: float = Field(..., ge=0, description="Refining Charge Ag USD/toz")
    transportationCredit: bool = Field(default=False)
    otherPayables: Optional[str] = Field(default="")

class PaymentTerms(BaseModel):
    paymentMethod: str = Field(..., pattern="^(LC at sight|TT in advance|Open account|CAD|DLC)$")
    currency: str = Field(..., pattern="^(USD|EUR|GBP|CNY|JPY)$")
    prepaymentPercentage: float = Field(..., ge=0, le=100)
    provisionalPercentage: float = Field(..., ge=0, le=100)
    finalPercentage: float = Field(..., ge=0, le=100)
    wsmdLocation: str = Field(..., min_length=1)
    costSharingPercentage: float = Field(..., ge=0, le=100)
    surveyor: str = Field(..., min_length=1)

class BCFlowData(BaseModel):
    dealBasics: DealBasics
    commercialTerms: CommercialTerms
    paymentTerms: PaymentTerms

# Professional trading data
TRADING_DATA = {
    "buyers": [
        "Glencore International AG", "Vitol Group", "Trafigura Group", 
        "Mercuria Energy Group", "Gunvor Group", "Cargill Inc",
        "Louis Dreyfus Company", "COFCO International", "Noble Group",
        "Olam International", "Wilmar International", "ADM Trading"
    ],
    "materials": [
        "Zinc Concentrate", "Copper Concentrate", "Lead Concentrate", 
        "Silver Ore", "Gold Ore", "Lithium Spodumene", "Lithium Hydroxide",
        "Iron Ore Fines", "Iron Ore Pellets", "Coking Coal", "Thermal Coal",
        "Nickel Matte", "Cobalt Hydroxide", "Molybdenum Concentrate"
    ],
    "delivery_terms": ["CIF", "FOB", "CFR", "EXW", "DDP", "DAP"],
    "delivery_points": [
        "Shanghai, China", "Hamburg, Germany", "Rotterdam, Netherlands",
        "Singapore", "Long Beach, USA", "Antwerp, Belgium", "Tianjin, China",
        "Qingdao, China", "Busan, South Korea", "Yokohama, Japan"
    ],
    "shipment_modes": ["Ship", "Rails", "Truck", "Pipeline"],
    "packaging": ["Bulk", "Big Bags", "Containers", "Tank"],
    "payment_methods": ["LC at sight", "TT in advance", "Open account", "CAD", "DLC"],
    "currencies": ["USD", "EUR", "GBP", "CNY", "JPY"],
    "surveyors": [
        "SGS SA", "Bureau Veritas", "Intertek Group", "Alex Stewart International",
        "ALS Limited", "Cotecna", "CIL (Camin Cargo)", "Inspectorate"
    ]
}

# Market intelligence for AI suggestions
MARKET_BENCHMARKS = {
    "zinc_concentrate": {"tc_usd_dmt": {"min": 280, "max": 320, "avg": 300}},
    "copper_concentrate": {"tc_usd_dmt": {"min": 65, "max": 85, "avg": 75}},
    "lead_concentrate": {"tc_usd_dmt": {"min": 120, "max": 160, "avg": 140}}
}

@app.get("/")
async def health_check():
    return {
        "service": "OpenMineral BC Flow API",
        "status": "operational",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/bc-flow/dropdown-data")
async def get_dropdown_data():
    """Get all dropdown data for BC Flow form"""
    logger.info("Fetching dropdown data")
    return {
        "status": "success",
        "data": TRADING_DATA
    }

@app.post("/bc-flow/validate/step1")
async def validate_step1(data: DealBasics):
    """Validate Deal Basics step with trading domain logic"""
    logger.info(f"Validating step 1: {data.material} - {data.quantity} MT")
    
    suggestions = []
    warnings = []
    
    # Quantity validation based on material type
    if "concentrate" in data.material.lower():
        if data.quantity < 1000:
            warnings.append("Concentrate shipments typically minimum 1,000 MT for economic viability")
        elif data.quantity > 50000:
            suggestions.append("Large shipments >50k MT may require multiple vessels - consider split shipments")
    
    # Tolerance validation
    if data.quantityTolerance > 15:
        warnings.append("Tolerance >15% unusual for concentrates - verify with counterparty")
    
    return {
        "is_valid": len(warnings) == 0,
        "suggestions": suggestions,
        "warnings": warnings
    }

@app.post("/bc-flow/validate/step2") 
async def validate_step2(data: CommercialTerms):
    """Validate Commercial Terms with market intelligence"""
    logger.info(f"Validating commercial terms: TC={data.tcUsdPerDmt}")
    
    suggestions = []
    warnings = []
    
    # TC/RC market intelligence
    material_key = data.material.lower().replace(" ", "_") if hasattr(data, 'material') else "zinc_concentrate"
    if material_key in MARKET_BENCHMARKS:
        benchmark = MARKET_BENCHMARKS[material_key]["tc_usd_dmt"]
        if data.tcUsdPerDmt > benchmark["avg"] * 1.2:
            suggestions.append(f"TC ${data.tcUsdPerDmt}/dmt significantly above market avg ${benchmark['avg']}/dmt")
        elif data.tcUsdPerDmt < benchmark["min"]:
            warnings.append(f"TC below typical range ${benchmark['min']}-${benchmark['max']}/dmt")
    
    # Delivery term logic
    if data.deliveryTerm == "FOB" and data.deliveryMode == "Rails":
        warnings.append("FOB terms typically used for ship deliveries - verify Incoterms")
    
    return {
        "is_valid": len(warnings) == 0,
        "suggestions": suggestions,
        "warnings": warnings
    }

@app.post("/bc-flow/validate/step3")
async def validate_step3(data: PaymentTerms):
    """Validate Payment Terms with compliance checks"""
    logger.info(f"Validating payment terms: {data.paymentMethod}")
    
    suggestions = []
    warnings = []
    
    # Payment percentage validation
    total_pct = data.prepaymentPercentage + data.provisionalPercentage + data.finalPercentage
    if abs(total_pct - 100) > 0.01:
        warnings.append(f"Payment percentages total {total_pct}% - must equal 100%")
    
    # Risk assessment
    if data.paymentMethod == "Open account" and data.prepaymentPercentage < 20:
        suggestions.append("Open account terms with low prepayment increases credit risk")
    
    # Surveyor validation
    if not data.surveyor:
        warnings.append("Independent surveyor required for concentrate shipments")
    
    return {
        "is_valid": len(warnings) == 0,
        "suggestions": suggestions,
        "warnings": warnings
    }

@app.post("/bc-flow/submit")
async def submit_bc_flow(deal_data: BCFlowData):
    """Submit BC Flow for processing with comprehensive validation"""
    logger.info("Processing BC Flow submission")
    
    try:
        # Generate realistic task ID
        task_id = f"BC{datetime.now().strftime('%Y%m%d')}{hash(str(deal_data)) % 10000:04d}"
        
        # Simulate async processing
        asyncio.create_task(process_bc_flow_async(task_id, deal_data))
        
        return {
            "message": "BC Flow submitted successfully",
            "task_id": task_id,
            "status": "processing",
            "estimated_time": 15,
            "deal_reference": f"OM-{task_id}"
        }
        
    except Exception as e:
        logger.error(f"BC Flow submission failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Submission processing failed")

# Global task storage (in production, use Redis/database)
task_results = {}

async def process_bc_flow_async(task_id: str, deal_data: BCFlowData):
    """Simulate async BC Flow processing"""
    await asyncio.sleep(15)  # Simulate processing time
    
    task_results[task_id] = {
        "task_id": task_id,
        "status": "completed",
        "result": {
            "deal_id": f"OM-{task_id}",
            "status": "confirmed",
            "processing_time": 15.0,
            "deal_value_usd": deal_data.dealBasics.quantity * deal_data.commercialTerms.tcUsdPerDmt,
            "compliance_status": "passed",
            "risk_score": "low"
        }
    }

@app.get("/bc-flow/task/{task_id}")
async def get_task_status(task_id: str):
    """Get BC Flow processing status"""
    logger.info(f"Checking task status: {task_id}")
    
    if task_id in task_results:
        return task_results[task_id]
    
    # Default processing status
    return {
        "task_id": task_id,
        "status": "processing",
        "progress": 75,
        "estimated_remaining": 5
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
