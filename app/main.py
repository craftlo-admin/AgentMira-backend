"""
Main application entry point with MVC structure
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import controllers
from app.controllers.property_controller import PropertyController
from app.controllers.prediction_controller import PredictionController
from app.controllers.recommendation_controller import RecommendationController
from app.controllers.admin_controller import AdminController

# Import config for initial setup
from app.config.database_config import db_config
from app.utils.model_handler import model_handler

# Initialize FastAPI app
app = FastAPI(
    title="Property Management API",
    description="Backend API for property management with price prediction and recommendations",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize controllers
property_controller = PropertyController()
prediction_controller = PredictionController()
recommendation_controller = RecommendationController()
admin_controller = AdminController()

# Register all routers
app.include_router(property_controller.get_router())
app.include_router(prediction_controller.get_router())
app.include_router(recommendation_controller.get_router())
app.include_router(admin_controller.get_router())

# Root endpoint
@app.get("/")
async def root():
    """API root endpoint with basic information"""
    return {
        "message": "Property Management API v2.0",
        "version": "2.0.0",
        "architecture": "MVC Pattern",
        "status": "running",
        "endpoints": {
            "properties": "/properties",
            "property_details": "/properties/{id}",
            "property_info": "/properties/{id}/info",
            "property_images": "/properties/{id}/images",
            "all_details": "/properties/details/all",
            "prediction": "/predict",
            "recommendation": "/recommend",
            "model_data": "/pricedata", 
            "database_status": "/database/status",
            "health_check": "/health",
            "cache_stats": "/cache/stats",
            "cache_clear": "/cache/clear",
            "cache_cleanup": "/cache/cleanup",
            "documentation": "/docs"
        },
        "features": [
            "Property listing and details",
            "ML-based price prediction", 
            "Smart property recommendations",
            "Performance caching",
            "Database integration",
            "Admin endpoints"
        ]
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 Property Management API v2.0 Starting...")
    print("📁 Architecture: MVC Pattern")
    
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
    
    print("🎯 API ready at http://127.0.0.1:8000")
    print("📚 Documentation available at http://127.0.0.1:8000/docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Property Management API shutting down...")
    # Cleanup database connections if needed
    if hasattr(db_config, 'client'):
        db_config.client.close()
    print("✅ Shutdown complete")