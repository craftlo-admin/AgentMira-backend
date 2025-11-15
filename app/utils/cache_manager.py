"""
Simplified Cache Manager - Minimal implementation for compatibility
"""
from typing import Dict, Any, List, Optional


class PropertyScoreCache:
    """Minimal cache interface for backward compatibility"""
    
    def __init__(self, cache_size: int = 100, ttl_hours: int = 1):
        """Initialize minimal cache"""
        pass
    
    def get_property_scores(self, user_budget: float, user_min_bedrooms: int, 
                          properties_data: List[Dict[str, Any]]) -> Dict[int, Optional[Dict[str, Any]]]:
        """Return empty cache results (no caching)"""
        return {prop.get("id"): None for prop in properties_data}
    
    def cache_property_scores(self, user_budget: float, user_min_bedrooms: int, 
                            properties_scores: List[Dict[str, Any]]) -> None:
        """No-op caching method"""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Return empty stats"""
        return {"status": "disabled", "message": "Caching disabled for simplicity"}
    
    def clear(self) -> None:
        """No-op clear method"""
        pass


def get_cache_instance() -> PropertyScoreCache:
    """Get a minimal cache instance"""
    return PropertyScoreCache()