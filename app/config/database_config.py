"""
Database connection and configuration - Simplified for deployment
"""
import pymongo
import urllib.parse
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os

class DatabaseConfig:
    """MongoDB database configuration and connection manager"""
    
    def __init__(self):
        self.username = os.getenv("MONGODB_USERNAME", "himanshubarnwal1126")
        self.password = os.getenv("MONGODB_PASSWORD", "Hkb@8570890789")
        self.cluster_url = os.getenv("MONGODB_CLUSTER", "cluster0.q0dysfk.mongodb.net")
        self.database_name = os.getenv("MONGODB_DATABASE", "property_database")
        
        # URL encode the password to handle special characters
        encoded_password = urllib.parse.quote_plus(self.password)
        self.connection_string = f"mongodb+srv://{self.username}:{encoded_password}@{self.cluster_url}/"
        
        # Initialize client and database (synchronous)
        self.client = pymongo.MongoClient(
            self.connection_string,
            serverSelectionTimeoutMS=10000
        )
        self.database = self.client[self.database_name]
        
        # Collections
        self.properties_list_collection = self.database.get_collection("properties_list")
        self.properties_info_collection = self.database.get_collection("properties_info")
        self.properties_images_collection = self.database.get_collection("properties_images")
        
        # Thread pool for async simulation
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def ping_database(self) -> bool:
        """Test database connection by sending a ping."""
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor, 
                lambda: self.client.admin.command('ping')
            )
            return True
        except Exception as e:
            print(f"Database ping failed: {e}")
            return False
    
    async def get_collection_counts(self) -> dict:
        """Get document counts for all collections."""
        try:
            loop = asyncio.get_event_loop()
            
            # Run synchronous operations in thread pool
            properties_count = await loop.run_in_executor(
                self.executor,
                self.properties_list_collection.count_documents,
                {}
            )
            info_count = await loop.run_in_executor(
                self.executor,
                self.properties_info_collection.count_documents,
                {}
            )
            images_count = await loop.run_in_executor(
                self.executor,
                self.properties_images_collection.count_documents,
                {}
            )
            
            return {
                "properties_list": properties_count,
                "properties_info": info_count,
                "properties_images": images_count
            }
        except Exception as e:
            print(f"Error getting collection counts: {e}")
            return {"error": str(e)}
    
    async def clear_all_collections(self):
        """Clear all data from collections."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            self.executor,
            self.properties_list_collection.delete_many,
            {}
        )
        await loop.run_in_executor(
            self.executor,
            self.properties_info_collection.delete_many,
            {}
        )
        await loop.run_in_executor(
            self.executor,
            self.properties_images_collection.delete_many,
            {}
        )

# Create a single global instance of the database configuration
db_config = DatabaseConfig()