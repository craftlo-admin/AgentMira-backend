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
                    matching_properties.append(property_doc)
            
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