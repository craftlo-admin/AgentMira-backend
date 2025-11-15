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

            # Helper to try multiple possible keys for a value
            def _get_from_info(info: Optional[Dict[str, Any]], candidates, default=None):
                if not info:
                    return default
                for key in candidates:
                    if key in info and info.get(key) is not None:
                        return info.get(key)
                return default

            # Start with basic comparison fields from properties_list
            comparison_data = {
                "_id": str(property_doc.get('_id')),
                "id": property_doc.get('id'),
                "title": property_doc.get('title', 'Unknown Property'),
                "location": property_doc.get('location', 'Unknown Location'),
                "price": property_doc.get('price', 0)
            }

            # Normalize and prefer detailed info when available. Support multiple possible keys.
            bedrooms = _get_from_info(property_info, ['bedrooms', 'num_bedrooms', 'beds'], 0)
            bathrooms = _get_from_info(property_info, ['bathrooms', 'baths', 'num_bathrooms'], 0)
            size_sqft = _get_from_info(property_info, ['size_sqft', 'size', 'area', 'living_area'], 0)
            amenities = _get_from_info(property_info, ['amenities', 'features', 'amenity_list'], [])
            school_rating = _get_from_info(property_info, ['school_rating', 'schoolScore', 'school_rating_score'], 0)
            commute_time = _get_from_info(property_info, ['commute_time', 'commute_minutes'], 0)
            has_garage = _get_from_info(property_info, ['has_garage', 'garage', 'garage_available'], False)
            has_garden = _get_from_info(property_info, ['has_garden', 'garden', 'garden_available'], False)
            has_pool = _get_from_info(property_info, ['has_pool', 'pool', 'pool_available'], False)
            year_built = _get_from_info(property_info, ['year_built', 'built_year', 'construction_year'], 0)

            comparison_data.update({
                "bedrooms": bedrooms if bedrooms is not None else 0,
                "bathrooms": bathrooms if bathrooms is not None else 0,
                "size_sqft": size_sqft if size_sqft is not None else 0,
                "amenities": amenities if amenities is not None else [],
                "school_rating": school_rating if school_rating is not None else 0,
                "commute_time": commute_time if commute_time is not None else 0,
                "has_garage": bool(has_garage),
                "has_garden": bool(has_garden),
                "has_pool": bool(has_pool),
                "year_built": year_built if year_built is not None else 0
            })

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
    
    async def get_comparison_stats(self) -> Dict[str, Any]:
        """Get statistics about property comparisons"""
        try:
            total_properties = self.db.properties_list_collection.count_documents({})
            
            return {
                "total_properties_available": total_properties,
                "comparison_features": [
                    "price",
                    "bedrooms", 
                    "bathrooms",
                    "size_sqft",
                    "amenities",
                    "school_rating",
                    "commute_time",
                    "garage_availability",
                    "garden_availability", 
                    "pool_availability",
                    "year_built"
                ]
            }
        except Exception as e:
            raise Exception(f"Error getting comparison stats: {str(e)}")