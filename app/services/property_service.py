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
            async for property_doc in self.db.properties_list_collection.find():
                # Convert ObjectId to string for JSON serialization
                property_doc['_id'] = str(property_doc['_id'])
                properties.append(property_doc)
            return properties
        except Exception as e:
            raise Exception(f"Error retrieving properties: {str(e)}")
    
    async def get_property_by_id(self, property_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific property by ID"""
        try:
            property_doc = await self.db.properties_list_collection.find_one({"id": property_id})
            if property_doc:
                property_doc['_id'] = str(property_doc['_id'])
            return property_doc
        except Exception as e:
            raise Exception(f"Error retrieving property {property_id}: {str(e)}")
    
    async def get_property_info(self, property_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve detailed property information"""
        try:
            property_info = await self.db.properties_info_collection.find_one({"id": property_id})
            if property_info:
                property_info['_id'] = str(property_info['_id'])
            return property_info
        except Exception as e:
            raise Exception(f"Error retrieving property info for {property_id}: {str(e)}")
    
    async def get_property_images(self, property_id: int) -> List[Dict[str, Any]]:
        """Retrieve property images"""
        try:
            images = []
            async for image_doc in self.db.properties_images_collection.find({"id": property_id}):
                image_doc['_id'] = str(image_doc['_id'])
                images.append(image_doc)
            return images
        except Exception as e:
            raise Exception(f"Error retrieving images for property {property_id}: {str(e)}")
    
    async def get_all_property_details(self) -> List[Dict[str, Any]]:
        """Retrieve all properties with their detailed information"""
        try:
            properties_with_details = []
            
            # Get all basic property info
            async for property_doc in self.db.properties_list_collection.find():
                property_id = property_doc.get('id')
                
                # Get detailed info
                property_info = await self.get_property_info(property_id)
                
                # Combine basic info with detailed info
                if property_info:
                    combined_property = {
                        "basic_info": {
                            "_id": str(property_doc['_id']),
                            "id": property_doc.get('id'),
                            "title": property_doc.get('title'),
                            "price": property_doc.get('price'),
                            "location": property_doc.get('location')
                        },
                        "details": property_info
                    }
                    properties_with_details.append(combined_property)
            
            return properties_with_details
        except Exception as e:
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