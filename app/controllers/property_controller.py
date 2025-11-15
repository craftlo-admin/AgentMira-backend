"""
Property Controller - Handles property-related HTTP requests
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.services.property_service import PropertyService
from app.models.property_models import PropertyList, PropertyInfo, PropertyImage


class PropertyController:
    """Controller for property-related endpoints"""
    
    def __init__(self):
        self.router = APIRouter(prefix="/properties", tags=["properties"])
        self.property_service = PropertyService()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all property routes"""
        
        @self.router.get("/", response_model=List[Dict[str, Any]])
        async def get_all_properties():
            """Get all properties"""
            try:
                properties = await self.property_service.get_all_properties()
                return properties
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/{property_id}")
        async def get_property_by_id(property_id: int):
            """Get a specific property by ID"""
            try:
                property_data = await self.property_service.get_property_by_id(property_id)
                if not property_data:
                    raise HTTPException(status_code=404, detail="Property not found")
                return property_data
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/{property_id}/info")
        async def get_property_info(property_id: int):
            """Get detailed property information"""
            try:
                property_info = await self.property_service.get_property_info(property_id)
                if not property_info:
                    raise HTTPException(status_code=404, detail="Property info not found")
                return property_info
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/{property_id}/images")
        async def get_property_images(property_id: int):
            """Get property images"""
            try:
                images = await self.property_service.get_property_images(property_id)
                return images
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/details/all")
        async def get_all_property_details():
            """Get all properties with their detailed information"""
            try:
                properties_with_details = await self.property_service.get_all_property_details()
                return {
                    "status": "success",
                    "total_properties": len(properties_with_details),
                    "properties": properties_with_details
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def get_router(self) -> APIRouter:
        """Get the FastAPI router for this controller"""
        return self.router