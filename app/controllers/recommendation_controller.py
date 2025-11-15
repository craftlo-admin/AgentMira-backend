"""
Recommendation Controller - Handles recommendation HTTP requests
"""
from fastapi import APIRouter, HTTPException
from app.services.recommendation_service import RecommendationService
from app.models.property_models import RecommendationRequest, RecommendationResponse


class RecommendationController:
    """Controller for recommendation endpoints"""
    
    def __init__(self):
        self.router = APIRouter(tags=["recommendations"])
        self.recommendation_service = RecommendationService()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all recommendation routes"""
        
        @self.router.post("/recommend", response_model=RecommendationResponse)
        async def get_recommendations(request: RecommendationRequest):
            """Get property recommendations based on user criteria"""
            try:
                recommendations = await self.recommendation_service.get_recommendations(request)
                return recommendations
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def get_router(self) -> APIRouter:
        """Get the FastAPI router for this controller"""
        return self.router