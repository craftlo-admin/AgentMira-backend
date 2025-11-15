"""
Prediction service for handling ML model operations
"""
from typing import Dict, Any
from app.utils.model_handler import model_handler
from app.models.property_models import PredictionRequest, PredictionResponse


class PredictionService:
    """Service class for ML prediction operations"""
    
    def __init__(self):
        self.model_handler = model_handler
    
    def predict_price(self, request_data: PredictionRequest) -> PredictionResponse:
        """Predict property price using ML model"""
        try:
            # Convert request to model input format
            model_input = self._prepare_model_input(request_data)
            
            # Get prediction from model
            if not self.model_handler.is_loaded:
                raise Exception("ML model is not loaded")
            
            prediction = self.model_handler.predict(model_input)
            predicted_price = float(prediction[0]) if isinstance(prediction, list) else float(prediction)
            
            return PredictionResponse(
                status="success",
                predicted_price=predicted_price,
                input_data=request_data.dict()
            )
            
        except Exception as e:
            return PredictionResponse(
                status="error",
                predicted_price=0.0,
                input_data=request_data.dict()
            )
    
    def _prepare_model_input(self, request: PredictionRequest) -> Dict[str, Any]:
        """Prepare input data for the ML model"""
        return {
            'property_type': request.property_type,
            'lot_area': request.lot_area,
            'building_area': request.building_area,
            'bedrooms': request.bedrooms,
            'bathrooms': request.bathrooms,
            'year_built': request.year_built,
            'has_pool': request.has_pool,
            'has_garage': request.has_garage,
            'school_rating': request.school_rating
        }