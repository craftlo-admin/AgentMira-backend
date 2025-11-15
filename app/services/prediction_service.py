"""
Prediction service for handling ML model operations
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from typing import Dict, Any, List
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
    
    def get_model_data(self) -> Dict[str, Any]:
        """Get model information and sample data"""
        try:
            if not self.model_handler.is_loaded:
                return {"status": "error", "message": "Model not loaded"}
            
            sample_input = self._get_sample_input()
            sample_prediction = self.predict_price(PredictionRequest(**sample_input))
            
            return {
                "status": "success",
                "sample_input": sample_input,
                "sample_prediction": sample_prediction.dict()
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _get_sample_input(self) -> Dict[str, Any]:
        """Get sample input data for demonstration"""
        return {
            "property_type": "SFH",
            "lot_area": 5000.0,
            "building_area": 1500.0,
            "bedrooms": 3,
            "bathrooms": 2,
            "year_built": 2015,
            "has_pool": False,
            "has_garage": True,
            "school_rating": 7
        }