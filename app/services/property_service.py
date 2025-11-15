"""
Property service for handling basic property operations
"""
from typing import List, Dict, Any, Optional
from app.config.database_config import db_config
from app.models.property_models import PropertyList, PropertyInfo, PropertyImage


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
                
                # Use detailed info if available, otherwise use sensible defaults
                if property_info:
                    # Remove _id from property_info to avoid conflicts
                    details = {k: v for k, v in property_info.items() if k != '_id'}
                else:
                    # Provide default values when detailed info is missing
                    details = {
                        "id": property_id,
                        "bedrooms": 2,
                        "bathrooms": 1,
                        "size_sqft": 1200,
                        "amenities": [],
                        "school_rating": 5,
                        "commute_time": 30,
                        "has_garage": False,
                        "has_garden": False,
                        "has_pool": False,
                        "year_built": 2010
                    }
                
                combined_property = {
                    "basic_info": basic_info,
                    "details": details
                }
                properties_with_details.append(combined_property)
            
            print(f"DEBUG: PropertyService returning {len(properties_with_details)} properties")
            return properties_with_details
        except Exception as e:
            print(f"ERROR in get_all_property_details: {str(e)}")
            raise Exception(f"Error retrieving all property details: {str(e)}")
    
    async def get_database_status(self) -> Dict[str, Any]:
        """Get database connection status and collection counts"""
        try:
            is_connected = await self.db.ping_database()
            collection_counts = await self.db.get_collection_counts() if is_connected else {}
            
            return {
                "database_connected": is_connected,
                "collections": collection_counts,
                "database_name": self.db.database_name
            }
        except Exception as e:
            raise Exception(f"Error checking database status: {str(e)}")