"""
Compare service for handling property comparison operations
"""
from typing import Dict, Any, Optional
from app.config.database_config import db_config


class CompareService:
    """Service class for property comparison operations"""
    
    def __init__(self):
        self.db = db_config
    
    async def get_property_comparison_data(self, property_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve property data optimized for comparison"""
        try:
            # Get basic property info
            property_doc = self.db.properties_list_collection.find_one({"id": property_id})
            if not property_doc:
                return None
            
            # Get detailed property info (may use different key names across datasets)
            property_info = self.db.properties_info_collection.find_one({"id": property_id})

            # Start with basic comparison fields from properties_list
            comparison_data = {
                "_id": str(property_doc.get('_id')),
                "id": property_doc.get('id'),
                "title": property_doc.get('title', 'Unknown Property'),
                "location": property_doc.get('location', 'Unknown Location'),
                "price": property_doc.get('price', 0),
                "bedrooms": property_info.get('bedrooms', 0) if property_info else 0,
                "bathrooms": property_info.get('bathrooms', 0) if property_info else 0,
                "size_sqft": property_info.get('size_sqft', 0) if property_info else 0,
                "amenities": property_info.get('amenities', []) if property_info else [],
                "school_rating": property_info.get('school_rating', 0) if property_info else 0,
                "commute_time": property_info.get('commute_time', 0) if property_info else 0,
                "has_garage": property_info.get('has_garage', False) if property_info else False,
                "has_garden": property_info.get('has_garden', False) if property_info else False,
                "has_pool": property_info.get('has_pool', False) if property_info else False,
                "year_built": property_info.get('year_built', 0) if property_info else 0
            }

            return comparison_data
        except Exception as e:
            raise Exception(f"Error retrieving property comparison data for {property_id}: {str(e)}")
    
    async def compare_properties(self, id1: int, id2: int) -> Dict[str, Any]:
        """Compare two properties and return detailed comparison"""
        try:
            # Get both properties
            property1 = await self.get_property_comparison_data(id1)
            property2 = await self.get_property_comparison_data(id2)
            
            if not property1:
                raise Exception(f"Property with ID {id1} not found")
            if not property2:
                raise Exception(f"Property with ID {id2} not found")
            
            # Calculate differences
            price_difference = property2.get('price', 0) - property1.get('price', 0)
            bedrooms_difference = property2.get('bedrooms', 0) - property1.get('bedrooms', 0)
            bathrooms_difference = property2.get('bathrooms', 0) - property1.get('bathrooms', 0)
            size_difference = property2.get('size_sqft', 0) - property1.get('size_sqft', 0)
            
            # Determine comparison notes
            comparison_notes = {
                "larger_property": id1 if property1.get('size_sqft', 0) > property2.get('size_sqft', 0) else id2,
                "more_expensive": id1 if property1.get('price', 0) > property2.get('price', 0) else id2,
                "more_bedrooms": id1 if property1.get('bedrooms', 0) > property2.get('bedrooms', 0) else id2,
                "more_bathrooms": id1 if property1.get('bathrooms', 0) > property2.get('bathrooms', 0) else id2
            }
            
            # Handle equal cases
            if property1.get('size_sqft', 0) == property2.get('size_sqft', 0):
                comparison_notes["larger_property"] = "equal"
            if property1.get('price', 0) == property2.get('price', 0):
                comparison_notes["more_expensive"] = "equal"
            if property1.get('bedrooms', 0) == property2.get('bedrooms', 0):
                comparison_notes["more_bedrooms"] = "equal"
            if property1.get('bathrooms', 0) == property2.get('bathrooms', 0):
                comparison_notes["more_bathrooms"] = "equal"
            
            # Create comparison summary
            comparison_summary = {
                "price_difference": price_difference,
                "bedrooms_difference": bedrooms_difference,
                "bathrooms_difference": bathrooms_difference,
                "size_difference": size_difference,
                "comparison_notes": comparison_notes
            }
            
            return {
                "status": "success",
                "property1": property1,
                "property2": property2,
                "comparison_summary": comparison_summary
            }
            
        except Exception as e:
            raise Exception(f"Error comparing properties: {str(e)}")