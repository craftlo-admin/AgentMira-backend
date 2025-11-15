"""
Compare Controller - Handles property comparison HTTP requests
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.compare_service import CompareService


class CompareRequest(BaseModel):
    """Request model for property comparison"""
    id1: int
    id2: int


class CompareController:
    """Controller for property comparison endpoints"""
    
    def __init__(self):
        self.router = APIRouter(tags=["comparison"])
        self.compare_service = CompareService()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all comparison routes"""
        
        @self.router.post("/comparebyid")
        async def compare_properties_by_id(request: CompareRequest):
            """Compare two properties by their IDs"""
            try:
                comparison_result = await self.compare_service.compare_properties(
                    request.id1, 
                    request.id2
                )
                return comparison_result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def get_router(self) -> APIRouter:
        """Get the FastAPI router for this controller"""
        return self.router