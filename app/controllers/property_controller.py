"""
Property Controller - Handles property-related HTTP requests
"""
from fastapi import APIRouter, HTTPException
from app.services.property_service import PropertyService


class PropertyController:
    """Controller for property-related endpoints"""
    
    def __init__(self):
        self.router = APIRouter(tags=["properties"])  # Remove prefix since main.py handles routing
        self.property_service = PropertyService()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all property routes"""
        
        @self.router.get("/properties")
        async def get_all_properties():
            """Get all properties"""
            try:
                properties = await self.property_service.get_all_properties()
                return {
                    "status": "success",
                    "total_properties": len(properties),
                    "properties": properties
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/properties/{property_id}")
        async def get_property_by_id(property_id: int):
            """Get a specific property by ID"""
            try:
                # Get base listing doc
                property_doc = await self.property_service.get_property_by_id(property_id)
                if not property_doc:
                    raise HTTPException(status_code=404, detail="Property not found")

                # Get detailed info and images
                property_info = await self.property_service.get_property_info(property_id)
                images = await self.property_service.get_property_images(property_id)

                # Build aggregated response
                combined = {
                    "_id": str(property_doc.get('_id')),
                    "id": property_doc.get('id'),
                    "title": property_doc.get('title'),
                    "price": property_doc.get('price'),
                    "location": property_doc.get('location'),
                    "images": images or [],
                }

                # Add property details with defaults
                details = {
                    "bedrooms": 0, "bathrooms": 0, "size_sqft": 0, "amenities": [],
                    "school_rating": 0, "commute_time": 0, "has_garage": False,
                    "has_garden": False, "has_pool": False, "year_built": 0
                }
                
                if property_info:
                    details.update({
                        "bedrooms": property_info.get('bedrooms', 0),
                        "bathrooms": property_info.get('bathrooms', 0),
                        "size_sqft": property_info.get('size_sqft', 0),
                        "amenities": property_info.get('amenities', []),
                        "school_rating": property_info.get('school_rating', 0),
                        "commute_time": property_info.get('commute_time', 0),
                        "has_garage": property_info.get('has_garage', False),
                        "has_garden": property_info.get('has_garden', False),
                        "has_pool": property_info.get('has_pool', False),
                        "year_built": property_info.get('year_built', 0)
                    })
                
                combined.update(details)

                return {
                    "status": "success",
                    "property": combined
                }
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def get_router(self) -> APIRouter:
        """Get the FastAPI router for this controller"""
        return self.router