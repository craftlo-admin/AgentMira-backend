"""
Property Management API with MVC Architecture
Using actual controllers from app/ folder - Production ready with all endpoints
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import sys
import os

# Add app directory to Python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Try to import MVC controllers (optional for deployment compatibility)
try:
    from app.controllers.property_controller import PropertyController
    from app.controllers.prediction_controller import PredictionController
    from app.controllers.recommendation_controller import RecommendationController
    from app.controllers.compare_controller import CompareController
    from app.controllers.search_controller import SearchController
    from app.models.property_models import PredictionRequest, RecommendationRequest
    MVC_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ MVC Controllers not available: {e}")
    print("📝 Using fallback implementations for Render deployment")
    PropertyController = None
    PredictionController = None
    RecommendationController = None
    CompareController = None
    SearchController = None
    PredictionRequest = None
    RecommendationRequest = None
    MVC_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(
    title="Property Management API",
    description="Complete MVC architecture with ML predictions and smart recommendations",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware - Allow all frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Initialize MVC Controllers if available
if MVC_AVAILABLE:
    try:
        property_controller = PropertyController()
        prediction_controller = PredictionController()
        recommendation_controller = RecommendationController()
        compare_controller = CompareController()
        search_controller = SearchController()
        
        # Register all controller routers
        app.include_router(property_controller.get_router())
        app.include_router(prediction_controller.get_router())
        app.include_router(recommendation_controller.get_router())
        app.include_router(compare_controller.get_router())
        app.include_router(search_controller.get_router())
        
        print("✅ MVC Controllers loaded successfully")
        
    except Exception as e:
        print(f"⚠️ MVC Controllers failed to initialize: {e}")
        print("📝 Using fallback simple implementations")
        MVC_AVAILABLE = False
        property_controller = None
        prediction_controller = None
        recommendation_controller = None
        compare_controller = None
        search_controller = None
else:
    property_controller = None
    prediction_controller = None
    recommendation_controller = None
    compare_controller = None
    search_controller = None

# ==================== SIMPLE MODELS FOR DEPLOYMENT ====================

# Removed fallback models - using full MVC implementation only

# ==================== API ENDPOINTS ====================

@app.get("/")
def root():
    """API root endpoint with all available endpoints"""
    return {
        "message": "Property Management API - " + ("MVC Controllers Active" if MVC_AVAILABLE else "Controllers Not Available"),
        "status": "running",
        "version": "2.0.0",
        "deployment": "render",
        "architecture": "Full MVC Controllers Integration" if MVC_AVAILABLE else "Requires MVC Controllers",
        "cors_enabled": True,
        "available_endpoints": {
            "properties": {
                "GET /properties": "List all properties",
                "GET /properties/{id}": "Get specific property with complete details"
            },
            "ml_prediction": {
                "POST /predict": "ML-based price prediction"
            },
            "recommendations": {
                "POST /recommend": "Smart property recommendations"
            },
            "comparison": {
                "POST /comparebyid": "Compare two properties by ID"
            },
            "search": {
                "POST /findproperties": "Advanced property search with filters"
            },
            "documentation": {
                "GET /docs": "Interactive API documentation (Swagger UI)",
                "GET /redoc": "Alternative API documentation (ReDoc)"
            }
        },
        "features": [
            "✅ Property Management " + ("via PropertyController" if MVC_AVAILABLE else "❌ Not Available"),
            "✅ ML Price Predictions " + ("via PredictionController" if MVC_AVAILABLE else "❌ Not Available"), 
            "✅ Smart Recommendations " + ("via RecommendationController" if MVC_AVAILABLE else "❌ Not Available"),
            "✅ Property Comparison " + ("via CompareController" if MVC_AVAILABLE else "❌ Not Available"),
            "✅ Advanced Property Search " + ("via SearchController" if MVC_AVAILABLE else "❌ Not Available"),
            "✅ CORS Enabled for All Frontends",
            "✅ " + ("MVC Architecture with Database Integration" if MVC_AVAILABLE else "Requires MVC Controllers")
        ],
        "mvc_controllers": {
            "mvc_available": MVC_AVAILABLE,
            "PropertyController": "Active" if property_controller else "Not Available",
            "PredictionController": "Active" if prediction_controller else "Not Available", 
            "RecommendationController": "Active" if recommendation_controller else "Not Available",
            "CompareController": "Active" if compare_controller else "Not Available",
            "SearchController": "Active" if search_controller else "Not Available"
        },
        "sample_usage": {
            "get_properties": "GET /properties",
            "predict_price": "POST /predict with property details",
            "get_recommendations": "POST /recommend with budget & preferences",
            "compare_properties": "POST /comparebyid with {\"id1\": 1, \"id2\": 2}"
        }
    }

# ==================== STARTUP MESSAGE ====================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Property Management API...")
    
    if MVC_AVAILABLE:
        print("📁 Architecture: Full MVC Controllers Integration")
        print("✅ PropertyController: Active (handles /properties endpoints)")
        print("✅ PredictionController: Active (handles /predict, /pricedata endpoints)")  
        print("✅ RecommendationController: Active (handles /recommend endpoint)")
        print("✅ CompareController: Active (handles /comparebyid endpoint)")
        print("✅ SearchController: Active (handles /findproperties endpoint)")
    else:
        print("❌ MVC Controllers not available - API will not function properly")
        print("� Please ensure app/ directory structure is correct")
    
    print("🌐 CORS: Enabled for all frontends")
    print("🎯 Ready at: http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print("🔗 Properties: http://127.0.0.1:8000/properties")
    uvicorn.run(app, host="0.0.0.0", port=8000)
