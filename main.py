"""
Property Management API with MVC Architecture
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add app directory to Python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import MVC controllers
from app.controllers.property_controller import PropertyController
from app.controllers.prediction_controller import PredictionController
from app.controllers.recommendation_controller import RecommendationController
from app.controllers.compare_controller import CompareController
from app.controllers.search_controller import SearchController

# Initialize FastAPI app
app = FastAPI(
    title="Property Management API",
    description="Complete MVC architecture with ML predictions and smart recommendations",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize and register MVC controllers
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

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Property Management API...")
    print("✅ All controllers loaded successfully")
    print("🎯 Server running at: http://127.0.0.1:8000")
    print("📚 API docs: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
