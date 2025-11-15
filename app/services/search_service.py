"""
Search service for handling property search operations
"""
from typing import List, Dict, Any, Optional
from app.config.database_config import db_config
from app.models.property_models import SearchRequest, SearchResponse


class SearchService:
    """Service class for search-related operations"""
    
    def __init__(self):
        self.db = db_config
    
    async def find_properties(self, request: SearchRequest) -> SearchResponse:
        """Find properties based on location, budget, and preferences"""
        try:
            matching_properties = []
            
            # Get all properties from properties_list collection
            for property_doc in self.db.properties_list_collection.find():
                property_doc['_id'] = str(property_doc['_id'])
                
                # Check location match (case-insensitive)
                property_location = property_doc.get('location', '').lower()
                if request.location.lower() not in property_location:
                    continue
                
                # Check budget constraint
                property_price = property_doc.get('price', 0)
                if property_price > request.budget:
                    continue
                
                # If no preferences, add the property (location and budget match)
                if not request.preferences:
                    matching_properties.append(property_doc)
                    continue
                
                # Check detailed preferences from properties_info collection
                property_id = property_doc.get('id')
                property_info = self.db.properties_info_collection.find_one({"id": property_id})
                
                if not property_info:
                    # If no detailed info but basic criteria match, still include
                    matching_properties.append(property_doc)
                    continue
                
                # Check preferences against property_info
                if self._matches_preferences(property_info, request.preferences):
                    # Combine basic info with detailed info for response
                    combined_property = {
                        **property_doc,
                        "details": {
                            "_id": str(property_info.get('_id')),
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
                        }
                    }
                    matching_properties.append(combined_property)
            
            return SearchResponse(
                status="success",
                total_properties=len(matching_properties),
                properties=matching_properties
            )
            
        except Exception as e:
            return SearchResponse(
                status="error",
                total_properties=0,
                properties=[]
            )
    
    def _matches_preferences(self, property_info: Dict[str, Any], preferences) -> bool:
        """Check if property matches all user preferences"""
        # Check bedrooms (property should have >= requested bedrooms)
        if preferences.bedrooms is not None:
            property_bedrooms = property_info.get('bedrooms', 0)
            if property_bedrooms < preferences.bedrooms:
                return False
        
        # Check bathrooms (property should have >= requested bathrooms)
        if preferences.bathrooms is not None:
            property_bathrooms = property_info.get('bathrooms', 0)
            if property_bathrooms < preferences.bathrooms:
                return False
        
        # Check minimum size (property should be >= requested size)
        if preferences.min_size_sqft is not None:
            property_size = property_info.get('size_sqft', 0)
            if property_size < preferences.min_size_sqft:
                return False
        
        # Check amenities (property should have ALL requested amenities)
        if preferences.amenities:
            property_amenities = property_info.get('amenities', [])
            # Convert to lowercase for case-insensitive comparison
            property_amenities_lower = [amenity.lower() for amenity in property_amenities]
            
            for required_amenity in preferences.amenities:
                if required_amenity.lower() not in property_amenities_lower:
                    return False
        
        return True
    
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