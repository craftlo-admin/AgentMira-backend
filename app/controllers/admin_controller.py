"""
Admin Controller - Handles administrative HTTP requests
"""
from fastapi import APIRouter, HTTPException
from app.services.property_service import PropertyService
from app.utils.cache_manager import get_cache_instance


class AdminController:
    """Controller for admin endpoints"""
    
    def __init__(self):
        self.router = APIRouter(tags=["admin"])
        self.property_service = PropertyService()
        self.cache = get_cache_instance()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all admin routes"""
        
        @self.router.get("/database/status")
        async def get_database_status():
            """Check database connection status"""
            try:
                status = await self.property_service.get_database_status()
                return status
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/health")
        async def health_check():
            """Health check endpoint"""
            try:
                db_status = await self.property_service.get_database_status()
                cache_stats = self.cache.get_stats()
                
                return {
                    "status": "healthy",
                    "database": db_status,
                    "cache": cache_stats,
                    "timestamp": "2024-11-15T00:00:00Z"
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/cache/stats")
        async def get_cache_stats():
            """Get cache statistics"""
            try:
                stats = self.cache.get_stats()
                return {
                    "status": "success",
                    "cache_statistics": stats
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/cache/clear")
        async def clear_cache():
            """Clear all cached data"""
            try:
                self.cache.clear_all()
                return {
                    "status": "success",
                    "message": "Cache cleared successfully"
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/cache/cleanup")
        async def cleanup_expired_cache():
            """Clean up expired cache entries"""
            try:
                initial_stats = self.cache.get_stats()
                self.cache.cleanup_expired()
                final_stats = self.cache.get_stats()
                
                return {
                    "status": "success",
                    "message": "Expired cache entries cleaned up",
                    "before": initial_stats,
                    "after": final_stats
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def get_router(self) -> APIRouter:
        """Get the FastAPI router for this controller"""
        return self.router