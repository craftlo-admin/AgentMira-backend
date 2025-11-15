"""
Prediction Controller - Handles ML prediction HTTP requests
"""
from fastapi import APIRouter, HTTPException
from app.services.prediction_service import PredictionService
from app.models.property_models import PredictionRequest, PredictionResponse


class PredictionController:
    """Controller for ML prediction endpoints"""
    
    def __init__(self):
        self.router = APIRouter(tags=["prediction"])
        self.prediction_service = PredictionService()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all prediction routes"""
        
        @self.router.post("/predict", response_model=PredictionResponse)
        async def predict_price(request: PredictionRequest):
            """Predict property price using ML model"""
            try:
                return self.prediction_service.predict_price(request)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def get_router(self) -> APIRouter:
        """Get the FastAPI router for this controller"""
        return self.router