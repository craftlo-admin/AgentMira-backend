"""
Property Management Backend API - MVC Version
FastAPI application with MVC architecture
"""
import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed, using system environment variables")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import MVC components
from app.controllers.property_controller import PropertyController
from app.controllers.prediction_controller import PredictionController
from app.controllers.recommendation_controller import RecommendationController
from app.controllers.admin_controller import AdminController
from app.config.database_config import db_config
from app.utils.model_handler import model_handler

# Initialize FastAPI app
app = FastAPI(
    title="Property Management API - MVC",
    description="Backend API for property management with MVC architecture",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize controllers
property_controller = PropertyController()
prediction_controller = PredictionController()
recommendation_controller = RecommendationController()
admin_controller = AdminController()

# Register all routers from MVC controllers
app.include_router(property_controller.get_router())
app.include_router(prediction_controller.get_router())
app.include_router(recommendation_controller.get_router())
app.include_router(admin_controller.get_router())

# Root endpoint
@app.get("/")
async def root():
    """API root endpoint with basic information"""
    return {
        "message": "Property Management API - Clean MVC Architecture",
        "version": "2.0.0", 
        "architecture": "Model-View-Controller (MVC)",
        "status": "running",
        "migration_status": "✅ Complete - Pure MVC Implementation",
        "structure": {
            "models": "app/models/ - Data models and validation",
            "controllers": "app/controllers/ - HTTP request handling", 
            "services": "app/services/ - Business logic",
            "config": "app/config/ - Configuration management",
            "utils": "app/utils/ - Utility functions and caching"
        },
        "endpoints": {
            "properties": "/properties",
            "prediction": "/predict",
            "recommendation": "/recommend", 
            "model_data": "/pricedata",
            "database_status": "/database/status",
            "health_check": "/health",
            "cache_management": "/cache/*",
            "documentation": "/docs"
        }
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 Property Management API v2.0 (Clean MVC) Starting...")
    print("🏗️  Architecture: Model-View-Controller Pattern")
    print("📁 Clean Structure:")
    print("   ├── app/")
    print("   │   ├── models/      # 🎯 Data models & validation")
    print("   │   ├── controllers/ # 🎮 Request handlers & routing") 
    print("   │   ├── services/    # 💼 Business logic & algorithms")
    print("   │   ├── config/      # ⚙️  Configuration management")
    print("   │   └── utils/       # 🛠️  Utilities & performance cache")
    print("   ├── main.py          # 🚀 Application entry point")
    print("   ├── complex_price_model_v2.pkl  # 🤖 ML model")
    print("   └── README_MVC.md    # 📚 Documentation")
    
    # Test database connection
    try:
        db_connected = await db_config.ping_database()
        if db_connected:
            print("✅ Database connection established")
            collection_counts = await db_config.get_collection_counts()
            print(f"📊 Collection counts: {collection_counts}")
        else:
            print("❌ Database connection failed")
    except Exception as e:
        print(f"⚠️  Database error: {e}")
    
    # Check model status
    if model_handler.is_loaded:
        print("🤖 ML model loaded successfully")
    else:
        print("⚠️  ML model not loaded")
    
    port = os.getenv("PORT", "8000")
    host = os.getenv("API_HOST", "127.0.0.1")
    print(f"🎯 API ready at http://{host}:{port}")
    print(f"📚 Documentation available at http://{host}:{port}/docs")

# Health check endpoint for deployment
@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms"""
    try:
        db_status = await db_config.ping_database()
        return {
            "status": "healthy",
            "database": "connected" if db_status else "disconnected", 
            "model": "loaded" if model_handler.is_loaded else "not_loaded",
            "version": "2.0.0",
            "architecture": "MVC"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "version": "2.0.0"
        }

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    uvicorn.run(
        app, 
        host=host, 
        port=port,
        reload=debug,
        log_level="info"
    )