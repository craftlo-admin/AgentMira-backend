"""
Models package for the property management application
"""
from .property_models import (
    PropertyList, 
    PropertyInfo, 
    PropertyImage, 
    PredictionRequest, 
    PredictionResponse,
    RecommendationRequest,
    RecommendationResponse
)

__all__ = [
    'PropertyList',
    'PropertyInfo', 
    'PropertyImage',
    'PredictionRequest',
    'PredictionResponse',
    'RecommendationRequest',
    'RecommendationResponse'
]