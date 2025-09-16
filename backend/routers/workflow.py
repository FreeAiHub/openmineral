from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel
from datetime import datetime

from routers.auth import get_current_active_user
from models.user import User

router = APIRouter()

# Data models
class WorkflowStep(BaseModel):
    id: int
    name: str
    description: str
    assigned_to: str
    status: str  # pending, in_progress, completed
    deadline: datetime | None = None

class Workflow(BaseModel):
    id: int
    name: str
    description: str
    deal_id: int | None = None
    steps: List[WorkflowStep]
    created_at: datetime
    updated_at: datetime
    created_by: str

class WorkflowExecution(BaseModel):
    workflow_id: int
    current_step: int
    status: str  # active, paused, completed, failed
    started_at: datetime
    completed_at: datetime | None = None

# Mock data
workflows_db = [
    {
        "id": 1,
        "name": "Deal Approval Process",
        "description": "Standard workflow for approving new deals",
        "deal_id": 1,
        "steps": [
            {
                "id": 1,
                "name": "Market Analysis",
                "description": "Analyze market conditions for the commodity",
                "assigned_to": "analyst@openmineral.com",
                "status": "completed",
                "deadline": datetime(2025, 9, 14, 17, 0, 0)
            },
            {
                "id": 2,
                "name": "Risk Assessment",
                "description": "Evaluate risks associated with the deal",
                "assigned_to": "risk@openmineral.com",
                "status": "completed",
                "deadline": datetime(2025, 9, 15, 17, 0, 0)
            },
            {
                "id": 3,
                "name": "Legal Review",
                "description": "Review contract terms and conditions",
                "assigned_to": "legal@openmineral.com",
                "status": "in_progress",
                "deadline": datetime(2025, 9, 17, 17, 0, 0)
            },
            {
                "id": 4,
                "name": "Final Approval",
                "description": "Obtain final approval from authorized personnel",
                "assigned_to": "director@openmineral.com",
                "status": "pending",
                "deadline": datetime(2025, 9, 18, 17, 0, 0)
            }
        ],
        "created_at": datetime(2025, 9, 14, 9, 0, 0),
        "updated_at": datetime(2025, 9, 15, 14, 30, 0),
        "created_by": "system"
    }
]

workflow_executions_db = [
    {
        "workflow_id": 1,
        "current_step": 3,
        "status": "active",
        "started_at": datetime(2025, 9, 14, 9, 15, 0),
        "completed_at": None
    }
]

# Endpoints
@router.get("/", response_model=List[Workflow])
async def get_workflows(current_user: User = Depends(get_current_active_user)):
    """Get all workflows"""
    return workflows_db

@router.get("/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: int, current_user: User = Depends(get_current_active_user)):
    """Get a specific workflow by ID"""
    for workflow in workflows_db:
        if workflow["id"] == workflow_id:
            return workflow
    return {"error": "Workflow not found"}

@router.post("/")
async def create_workflow(workflow: Workflow, current_user: User = Depends(get_current_active_user)):
    """Create a new workflow"""
    # In a real implementation, this would be stored in a database
    workflows_db.append(workflow.dict())
    return {"message": "Workflow created successfully", "workflow_id": workflow.id}

@router.post("/execute")
async def execute_workflow(workflow_id: int, current_user: User = Depends(get_current_active_user)):
    """Start execution of a workflow"""
    # In a real implementation, this would trigger the workflow execution engine
    execution = {
        "workflow_id": workflow_id,
        "current_step": 1,
        "status": "active",
        "started_at": datetime.now(),
        "completed_at": None
    }
    workflow_executions_db.append(execution)
    return {"message": "Workflow execution started", "execution": execution}

@router.post("/step/complete")
async def complete_workflow_step(workflow_id: int, step_id: int, current_user: User = Depends(get_current_active_user)):
    """Mark a workflow step as completed"""
    # In a real implementation, this would update the workflow state
    for workflow in workflows_db:
        if workflow["id"] == workflow_id:
            for step in workflow["steps"]:
                if step["id"] == step_id:
                    step["status"] = "completed"
                    step["completed_at"] = datetime.now()
                    return {"message": f"Step {step_id} marked as completed", "workflow": workflow}
    return {"error": "Workflow or step not found"}

@router.get("/execution/{workflow_id}", response_model=WorkflowExecution)
async def get_workflow_execution(workflow_id: int, current_user: User = Depends(get_current_active_user)):
    """Get execution status of a workflow"""
    for execution in workflow_executions_db:
        if execution["workflow_id"] == workflow_id:
            return execution
    return {"error": "Workflow execution not found"}
