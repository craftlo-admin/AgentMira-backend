"""
Database connection and configuration
"""
import motor.motor_asyncio
import urllib.parse
from typing import Optional

class DatabaseConfig:
    """MongoDB database configuration and connection manager"""
    
    def __init__(self):
        self.username = "himanshubarnwal1126"
        self.password = "Hkb@8570890789"
        self.cluster_url = "cluster0.q0dysfk.mongodb.net"
        self.database_name = "property_database"
        
        # URL encode the password to handle special characters
        encoded_password = urllib.parse.quote_plus(self.password)
        self.connection_string = f"mongodb+srv://{self.username}:{encoded_password}@{self.cluster_url}/"
        
        # Initialize client and database
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            self.connection_string,
            serverSelectionTimeoutMS=10000  # Set a timeout for server selection
        )
        self.database = self.client[self.database_name]
        
        # Collections
        self.properties_list_collection = self.database.get_collection("properties_list")
        self.properties_info_collection = self.database.get_collection("properties_info")
        self.properties_images_collection = self.database.get_collection("properties_images")
    
    async def ping_database(self) -> bool:
        """Test database connection by sending a ping."""
        try:
            await self.client.admin.command('ping')
            return True
        except Exception:
            return False
    
    async def get_collection_counts(self) -> dict:
        """Get document counts for all collections."""
        properties_count = await self.properties_list_collection.count_documents({})
        info_count = await self.properties_info_collection.count_documents({})
        images_count = await self.properties_images_collection.count_documents({})
        
        return {
            "properties_list": properties_count,
            "properties_info": info_count,
            "properties_images": images_count
        }
    
    async def clear_all_collections(self):
        """Clear all data from collections."""
        await self.properties_list_collection.delete_many({})
        await self.properties_info_collection.delete_many({})
        await self.properties_images_collection.delete_many({})

# Create a single global instance of the database configuration
db_config = DatabaseConfig()