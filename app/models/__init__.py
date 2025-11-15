"""
Models package for the property management application
"""
from .property_models import (
    PredictionRequest, 
    PredictionResponse,
    RecommendationRequest,
    RecommendationResponse,
    SearchPreferences,
    SearchRequest,
    SearchResponse
)

__all__ = [
    'PredictionRequest',
    'PredictionResponse',
    'RecommendationRequest',
    'RecommendationResponse',
    'SearchPreferences',
    'SearchRequest',
    'SearchResponse'
]