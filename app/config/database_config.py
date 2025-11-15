"""
Database connection and configuration
"""
import pymongo
import urllib.parse
import os


class DatabaseConfig:
    """Simple MongoDB database configuration"""
    
    def __init__(self):
        # Get environment variables with defaults
        username = os.getenv("MONGODB_USERNAME", "himanshubarnwal1126")
        password = os.getenv("MONGODB_PASSWORD", "Hkb@8570890789")
        cluster_url = os.getenv("MONGODB_CLUSTER", "cluster0.q0dysfk.mongodb.net")
        database_name = os.getenv("MONGODB_DATABASE", "property_database")
        
        # Create connection string
        encoded_password = urllib.parse.quote_plus(password)
        connection_string = f"mongodb+srv://{username}:{encoded_password}@{cluster_url}/"
        
        # Initialize MongoDB client and collections
        self.client = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=10000)
        self.database = self.client[database_name]
        
        # Collection references
        self.properties_list_collection = self.database["properties_list"]
        self.properties_info_collection = self.database["properties_info"]
        self.properties_images_collection = self.database["properties_images"]


# Global database instance
db_config = DatabaseConfig()