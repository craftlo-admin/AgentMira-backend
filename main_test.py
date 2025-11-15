"""
Minimal FastAPI app for Render deployment test
"""
from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI(
    title="Property Management API - Test",
    description="Minimal version for Render deployment testing",
    version="1.0.0"
)

@app.get("/")
def root():
    """Basic root endpoint"""
    return {
        "message": "Property Management API - Minimal Test Version",
        "status": "running",
        "version": "1.0.0",
        "deployment": "render-test"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "property-api-minimal",
        "version": "1.0.0"
    }

@app.get("/test")
def test_endpoint():
    """Test endpoint with sample data"""
    return {
        "test_data": [
            {"id": 1, "name": "Test Property 1", "price": 250000},
            {"id": 2, "name": "Test Property 2", "price": 350000}
        ],
        "message": "This is test data to verify deployment works"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)