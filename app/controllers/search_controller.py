"""
Search controller for property search operations
"""
from fastapi import APIRouter, HTTPException
from app.services.search_service import SearchService
from app.models.search_models import FindPropertiesRequest, FindPropertiesResponse
import logging

logger = logging.getLogger(__name__)


class SearchController:
    """Controller class for property search operations"""
    
    def __init__(self):
        self.service = SearchService()
        self.router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all search-related routes"""
        
        @self.router.post("/findproperties", response_model=FindPropertiesResponse)
        async def find_properties(request: FindPropertiesRequest):
            """
            Find properties based on location, budget, and preferences
            
            - **location**: Location to search for properties
            - **budget**: Maximum budget (properties with price <= budget)
            - **preferences**: Property preferences (bedrooms, bathrooms minimum requirements)
            """
            try:
                logger.info(f"Finding properties for location: {request.location}, budget: {request.budget}")
                
                # Call the search service to find matching properties
                result = await self.service.find_properties(
                    location=request.location,
                    max_budget=request.budget,
                    min_bedrooms=request.preferences.bedrooms,
                    min_bathrooms=request.preferences.bathrooms
                )
                
                return FindPropertiesResponse(
                    status="success",
                    total_found=len(result["properties"]),
                    properties=result["properties"],
                    search_criteria=result["search_criteria"],
                    message=result.get("message", "Properties found successfully")
                )
                
            except Exception as e:
                logger.error(f"Error finding properties: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error finding properties: {str(e)}")
    
    def get_router(self) -> APIRouter:
        """Return the configured router"""
        return self.router