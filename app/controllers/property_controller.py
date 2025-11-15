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

                # Merge details if present, normalizing some common fields
                if property_info:
                    combined.update({
                        "bedrooms": property_info.get('bedrooms') if property_info.get('bedrooms') is not None else property_info.get('num_bedrooms', 0),
                        "bathrooms": property_info.get('bathrooms') if property_info.get('bathrooms') is not None else property_info.get('baths', 0),
                        "size_sqft": property_info.get('size_sqft') or property_info.get('area') or property_info.get('living_area') or 0,
                        "amenities": property_info.get('amenities', []),
                        "school_rating": property_info.get('school_rating', 0),
                        "commute_time": property_info.get('commute_time', 0),
                        "has_garage": property_info.get('has_garage', False),
                        "has_garden": property_info.get('has_garden', False),
                        "has_pool": property_info.get('has_pool', False),
                        "year_built": property_info.get('year_built', 0)
                    })
                else:
                    # Defaults when no detailed info
                    combined.update({
                        "bedrooms": 0,
                        "bathrooms": 0,
                        "size_sqft": 0,
                        "amenities": [],
                        "school_rating": 0,
                        "commute_time": 0,
                        "has_garage": False,
                        "has_garden": False,
                        "has_pool": False,
                        "year_built": 0
                    })

                return {
                    "status": "success",
                    "property": combined
                }
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/properties/{property_id}/info")
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
        
        @self.router.get("/properties/{property_id}/images")
        async def get_property_images(property_id: int):
            """Get property images"""
            try:
                images = await self.property_service.get_property_images(property_id)
                return images
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/properties/details/all")
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