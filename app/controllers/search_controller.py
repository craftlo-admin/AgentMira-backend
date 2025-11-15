"""
Search controller for property search operations
"""
from fastapi import APIRouter, HTTPException
from app.services.search_service import SearchService
from app.models.property_models import SearchRequest, SearchResponse


class SearchController:
    """Controller class for property search operations"""
    
    def __init__(self):
        self.search_service = SearchService()
        self.router = APIRouter(tags=["search"])
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all search-related routes"""
        
        @self.router.post("/findproperties", response_model=SearchResponse)
        async def find_properties(request: SearchRequest):
            """Find properties based on location, budget, and preferences"""
            try:
                return await self.search_service.find_properties(request)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def get_router(self) -> APIRouter:
        """Return the configured router"""
        return self.router