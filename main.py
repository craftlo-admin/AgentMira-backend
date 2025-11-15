"""
Minimal FastAPI app for Render deployment
Entry point for the Property Management API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="Property Management API",
    description="Minimal version for Render deployment",
    version="2.0.0"
)

# Configure CORS middleware - Allow all frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def root():
    """Basic root endpoint"""
    return {
        "message": "Property Management API - Production Ready",
        "status": "running",
        "version": "2.0.0",
        "deployment": "render",
        "architecture": "MVC Ready"
    }

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "property-management-api",
        "version": "2.0.0",
        "uptime": "operational"
    }

@app.get("/test")
def test_endpoint():
    """Test endpoint with sample property data"""
    return {
        "properties": [
            {"id": 1, "name": "Modern Apartment", "price": 250000, "location": "Downtown"},
            {"id": 2, "name": "Family House", "price": 350000, "location": "Suburbs"},
            {"id": 3, "name": "Luxury Condo", "price": 500000, "location": "Waterfront"}
        ],
        "message": "API is working correctly - Ready for MVC upgrade",
        "next_features": ["Database Integration", "ML Predictions", "Smart Recommendations"]
    }

@app.get("/cors-test")
def cors_test():
    """CORS test endpoint - should be accessible from any frontend"""
    return {
        "cors_status": "enabled",
        "message": "CORS is working! This API accepts requests from any frontend",
        "access_control": {
            "origins": "All (*)",
            "methods": "All (GET, POST, PUT, DELETE, etc.)",
            "headers": "All (*)",
            "credentials": "Allowed"
        },
        "test_instructions": [
            "Make a request from any frontend (React, Vue, Angular, etc.)",
            "Check browser network tab for CORS headers",
            "Verify no CORS errors in console"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
