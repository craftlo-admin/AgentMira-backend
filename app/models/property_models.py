"""
Database models using Pydantic for data validation
"""
from pydantic import BaseModel
from typing import List, Optional


class PropertyList(BaseModel):
    """Model for basic property listing information"""
    id: int
    title: str
    price: int
    location: str


class PropertyInfo(BaseModel):
    """Model for detailed property information"""
    id: int
    bedrooms: int
    bathrooms: int
    size_sqft: int
    amenities: List[str]


class PropertyImage(BaseModel):
    """Model for property image information"""
    id: int
    image_url: str


class PredictionRequest(BaseModel):
    """Model for price prediction requests"""
    property_type: str = "SFH"  # Single Family Home, Condo, etc.
    lot_area: float = 5000      # Lot area in sqft
    building_area: float = 1500 # Building area in sqft
    bedrooms: int = 3           # Number of bedrooms
    bathrooms: int = 2          # Number of bathrooms
    year_built: int = 2015      # Year property was built
    has_pool: bool = False      # Whether property has a pool
    has_garage: bool = True     # Whether property has a garage
    school_rating: int = 7      # School district rating (1-10)


class PredictionResponse(BaseModel):
    """Model for price prediction responses"""
    status: str
    predicted_price: float
    input_data: dict
    model_info: Optional[dict] = None


class RecommendationRequest(BaseModel):
    """Model for property recommendation requests"""
    user_budget: int
    user_min_bedrooms: int
    user_max_commute: Optional[int] = None
    user_min_school_rating: Optional[int] = None
    preferred_amenities: Optional[List[str]] = None


class RecommendationResponse(BaseModel):
    """Model for property recommendation responses"""
    status: str
    total_properties: int
    recommended_properties: List[dict]
    cache_info: Optional[dict] = None
    performance_metrics: Optional[dict] = None