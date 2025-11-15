"""
Search models for property search operations
"""
from pydantic import BaseModel
from typing import List, Optional


class PropertyPreferences(BaseModel):
    """Model for property search preferences"""
    bedrooms: int
    bathrooms: int


class FindPropertiesRequest(BaseModel):
    """Model for find properties request"""
    location: str
    budget: int
    preferences: PropertyPreferences


class PropertySearchResult(BaseModel):
    """Model for individual property search result"""
    id: int
    title: str
    price: int
    location: str
    bedrooms: int
    bathrooms: int
    size_sqft: int
    amenities: List[str]


class FindPropertiesResponse(BaseModel):
    """Model for find properties response"""
    status: str
    total_found: int
    properties: List[PropertySearchResult]
    search_criteria: dict
    message: str