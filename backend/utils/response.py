"""
API Response Utilities for OpenMineral
Standardized response format for all endpoints
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel
from fastapi import status

class APIResponse(BaseModel):
    """Standard API Response Model"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    message: Optional[str] = None
    code: int = status.HTTP_200_OK
    
    class Config:
        from_attributes = True

def success_response(data: Any = None, message: str = "Success") -> APIResponse:
    """Create successful response"""
    return APIResponse(
        success=True,
        data=data,
        message=message
    )

def error_response(
    error: str, 
    code: int = status.HTTP_400_BAD_REQUEST,
    message: Optional[str] = None
) -> APIResponse:
    """Create error response"""
    return APIResponse(
        success=False,
        error=error,
        message=message or "Request failed",
        code=code
    )

def validation_error(field_errors: Dict[str, Any]) -> APIResponse:
    """Create validation error response"""
    return error_response(
        error="Validation Error",
        message="Invalid input data",
        code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

# Global response helpers
def api_success(data: Any = None, message: str = "Success"):
    return success_response(data, message)

def api_error(error: str, code: int = 400, message: Optional[str] = None):
    return error_response(error, code, message)
