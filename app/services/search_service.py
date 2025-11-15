"""
Search service for handling property search operations
"""
from typing import List, Dict, Any, Optional
from app.config.database_config import db_config


class SearchService:
    """Service class for search-related operations"""
    
    def __init__(self):
        self.db = db_config
    
    async def search_properties(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search properties by query and filters"""
        try:
            # Basic search implementation
            search_filter = {}
            
            if query:
                # Simple text search in title and location
                search_filter["$or"] = [
                    {"title": {"$regex": query, "$options": "i"}},
                    {"location": {"$regex": query, "$options": "i"}}
                ]
            
            # Add additional filters if provided
            if filters:
                search_filter.update(filters)
            
            # Execute search using synchronous iteration
            properties = []
            for property_doc in self.db.properties_list_collection.find(search_filter):
                property_doc['_id'] = str(property_doc['_id'])
                properties.append(property_doc)
            
            return properties
        except Exception as e:
            raise Exception(f"Error searching properties: {str(e)}")
    
    async def get_search_suggestions(self, query: str) -> List[str]:
        """Get search suggestions based on query"""
        try:
            suggestions = []
            
            # Get unique locations and titles for suggestions using synchronous calls
            locations = self.db.properties_list_collection.distinct("location")
            titles = self.db.properties_list_collection.distinct("title")
            
            # Filter suggestions based on query
            query_lower = query.lower()
            for location in locations:
                if query_lower in location.lower():
                    suggestions.append(location)
            
            for title in titles:
                if query_lower in title.lower():
                    suggestions.append(title)
            
            return list(set(suggestions))[:10]  # Return unique suggestions, max 10
        except Exception as e:
            raise Exception(f"Error getting search suggestions: {str(e)}")