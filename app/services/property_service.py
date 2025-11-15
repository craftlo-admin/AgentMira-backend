"""
Property service for handling basic property operations
"""
from typing import List, Dict, Any, Optional
from app.config.database_config import db_config


class PropertyService:
    """Service class for property-related operations"""
    
    def __init__(self):
        self.db = db_config
    
    async def get_all_properties(self) -> List[Dict[str, Any]]:
        """Retrieve all properties from the database"""
        try:
            properties = []
            # Use synchronous iteration since we're using pymongo (not motor)
            for property_doc in self.db.properties_list_collection.find():
                # Convert ObjectId to string for JSON serialization
                property_doc['_id'] = str(property_doc['_id'])
                properties.append(property_doc)
            return properties
        except Exception as e:
            raise Exception(f"Error retrieving properties: {str(e)}")
    
    async def get_property_by_id(self, property_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific property by ID"""
        try:
            # Use synchronous call since we're using pymongo (not motor)
            property_doc = self.db.properties_list_collection.find_one({"id": property_id})
            if property_doc:
                property_doc['_id'] = str(property_doc['_id'])
            return property_doc
        except Exception as e:
            raise Exception(f"Error retrieving property {property_id}: {str(e)}")
    
    async def get_property_info(self, property_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve detailed property information"""
        try:
            # Use synchronous call since we're using pymongo (not motor)
            property_info = self.db.properties_info_collection.find_one({"id": property_id})
            if property_info:
                property_info['_id'] = str(property_info['_id'])
            return property_info
        except Exception as e:
            raise Exception(f"Error retrieving property info for {property_id}: {str(e)}")
    
    async def get_property_images(self, property_id: int) -> List[Dict[str, Any]]:
        """Retrieve property images"""
        try:
            images = []
            # Use synchronous iteration since we're using pymongo (not motor)
            for image_doc in self.db.properties_images_collection.find({"id": property_id}):
                image_doc['_id'] = str(image_doc['_id'])
                images.append(image_doc)
            return images
        except Exception as e:
            raise Exception(f"Error retrieving images for property {property_id}: {str(e)}")
    
    async def get_all_property_details(self) -> List[Dict[str, Any]]:
        """Retrieve all properties with their detailed information"""
        try:
            properties_with_details = []
            
            # Get all basic property info using synchronous iteration
            for property_doc in self.db.properties_list_collection.find():
                property_id = property_doc.get('id')
                
                # Get detailed info (optional)
                property_info = await self.get_property_info(property_id)
                
                # Always include the property, even if detailed info is missing
                basic_info = {
                    "_id": str(property_doc['_id']),
                    "id": property_doc.get('id'),
                    "title": property_doc.get('title'),
                    "price": property_doc.get('price'),
                    "location": property_doc.get('location')
                }
                
                # Use detailed info if available, otherwise use defaults
                details = {}
                if property_info:
                    details = {k: v for k, v in property_info.items() if k != '_id'}
                
                # Set defaults for missing fields
                defaults = {
                    "id": property_id, "bedrooms": 2, "bathrooms": 1, "size_sqft": 1200,
                    "amenities": [], "school_rating": 5, "commute_time": 30,
                    "has_garage": False, "has_garden": False, "has_pool": False, "year_built": 2010
                }
                
                for key, default_value in defaults.items():
                    if key not in details:
                        details[key] = default_value
                
                combined_property = {
                    "basic_info": basic_info,
                    "details": details
                }
                properties_with_details.append(combined_property)
            
            return properties_with_details
        except Exception as e:
            raise Exception(f"Error retrieving all property details: {str(e)}")