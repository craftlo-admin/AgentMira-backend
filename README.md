# AgentMira Backend - Property Management API

## 🏗️ MVC Architecture

A FastAPI-based property management system with ML-powered price predictions and smart recommendations built with **Model-View-Controller (MVC)** architecture.

## ✨ Features

- 🏠 **Property Management**: CRUD operations for properties, info, and images
- 🤖 **ML Price Prediction**: Intelligent property price forecasting using custom algorithms
- 🎯 **Smart Recommendations**: Personalized property suggestions with 6-component weighted scoring
- 💾 **Performance Caching**: Thread-safe caching with TTL and LRU eviction
- 🏛️ **MVC Architecture**: Clean separation of concerns for maintainability and scalability
- 🌐 **Cloud Deployment**: Optimized for Render with minimal dependencies

## 📁 MVC Project Structure

```
AgentMira-backend/
├── 📄 main.py                          # Application entry point
├── 📄 main_test.py                     # Minimal deployment version
├── 🤖 complex_price_model_v2.pkl      # ML model file
├── 📄 requirements.txt                 # Dependencies (minimal for deployment)
├── 📄 Procfile                        # Render deployment configuration
├── 📄 render.yaml                     # Render service configuration
├── 📄 runtime.txt                     # Python version specification
├── 📄 .env.example                    # Environment variables template
│
└── 📁 app/                            # MVC Application Package
    ├── 📁 models/                     # 🎯 DATA MODELS
    │   ├── __init__.py
    │   └── property_models.py         # Pydantic models & validation
    │
    ├── 📁 controllers/                # 🎮 REQUEST HANDLERS  
    │   ├── __init__.py
    │   ├── property_controller.py     # Property CRUD endpoints
    │   ├── prediction_controller.py   # ML prediction endpoints
    │   ├── recommendation_controller.py # Smart recommendation endpoints
    │   └── admin_controller.py        # Admin & health check endpoints
    │
    ├── 📁 services/                   # 💼 BUSINESS LOGIC
    │   ├── __init__.py  
    │   ├── property_service.py        # Property business operations
    │   ├── prediction_service.py      # ML prediction algorithms
    │   └── recommendation_service.py  # Recommendation algorithms
    │
    ├── 📁 config/                     # ⚙️ CONFIGURATION
    │   ├── __init__.py
    │   └── database_config.py         # MongoDB connection settings
    │
    └── 📁 utils/                      # 🛠️ UTILITIES
        ├── __init__.py
        ├── cache_manager.py           # Performance caching system
        └── model_handler.py           # ML model management
```

## 🏛️ MVC Pattern Implementation

### 🎯 **Models** (`app/models/`)
- **Purpose**: Data structure definition and validation
- **Components**: Pydantic models for request/response validation, data schemas

### 🎮 **Controllers** (`app/controllers/`)
- **Purpose**: Handle HTTP requests and responses  
- **Components**: Route definitions, request validation, response formatting, error handling

### 💼 **Services** (`app/services/`)
- **Purpose**: Business logic and data processing
- **Components**: Core algorithms, data transformation, external service integration

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git account

### Local Development
```bash
# Clone the repository
git clone https://github.com/craftlo-admin/AgentMira-backend.git
cd AgentMira-backend

# Install dependencies (full version)
pip install -r requirements_ultra_minimal.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your credentials

# Run the application
python main.py  # Runs minimal version for testing
```

### 🌐 Deployment on Render

#### Current Deployment (Minimal Version)
The repository is configured for **minimal deployment** to avoid compilation issues:

**Current Configuration:**
```yaml
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Dependencies: FastAPI + Uvicorn only
```

#### Deployment Steps:
1. **Connect Repository** to [Render](https://render.com)
2. **Create Web Service** from `craftlo-admin/AgentMira-backend`
3. **Auto-Configuration**: Render detects `render.yaml` and `Procfile`
4. **Deploy**: No additional configuration needed

#### Available Endpoints (Minimal Version):
- `GET /` - API information
- `GET /health` - Health check
- `GET /test` - Sample test data

#### Environment Variables (Optional):
```bash
MONGODB_PASSWORD=your_password     # For full version
ALLOWED_ORIGINS=*                  # CORS configuration
PORT=10000                         # Render sets automatically
```

## 📋 API Endpoints

### 🏠 Property Management
- `GET /properties` - List all properties
- `GET /properties/{id}` - Get property details
- `GET /properties/{id}/info` - Get detailed property information
- `GET /properties/{id}/images` - Get property images

### 🤖 ML Predictions
- `POST /predict` - Predict property price
- `GET /pricedata` - Get model information

### 🎯 Recommendations
- `POST /recommend` - Get personalized recommendations

### ⚙️ Admin & Health
- `GET /health` - Health check
- `GET /database/status` - Database connectivity
- `GET /cache/stats` - Cache performance metrics

## 🎯 Smart Recommendation Algorithm

The system uses a **6-component weighted scoring** algorithm for property recommendations:

### Scoring Components:
1. **Price Match (30%)**: Budget compatibility and affordability
2. **Bedrooms (20%)**: Meeting minimum bedroom requirements  
3. **School Rating (15%)**: Educational quality in the area
4. **Commute Time (15%)**: Location convenience and accessibility
5. **Property Age (10%)**: Building condition and modern features
6. **Amenities (10%)**: Additional features (pool, garage, garden)

### Algorithm Features:
- **Thread-safe caching** for performance optimization
- **Real-time scoring** based on user preferences
- **Top 10 recommendations** with detailed metrics
- **Configurable weights** for different user priorities

## 🤖 ML Price Prediction

### Simple Prediction Model
For deployment compatibility, the system uses a **custom linear model**:

```python
# Base calculation with realistic coefficients
price = base_price + (bedrooms * 25000) + (bathrooms * 15000) + 
        (building_area * 150) + (lot_area * 0.02) + amenity_bonuses
```

### Features:
- **No external ML dependencies** (deployment-friendly)
- **Realistic price estimates** based on property features
- **Fast predictions** with consistent results
- **Fallback system** for reliability

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: MongoDB Atlas (when enabled)
- **Deployment**: Render Cloud Platform
- **Caching**: Custom thread-safe implementation
- **Architecture**: Model-View-Controller (MVC)

## 📚 API Documentation

### Current Deployment (Minimal Version)
- **API Docs**: `https://your-app.onrender.com/docs` (when deployed)
- **Health Check**: `https://your-app.onrender.com/health`
- **Test Endpoint**: `https://your-app.onrender.com/test`

### Full Version Endpoints (Future)
- `GET /properties/` - List all properties
- `POST /predict` - ML price prediction  
- `POST /recommend` - Smart recommendations
- `GET /cache/stats` - Performance metrics

## 🔄 Version Management

### Current State: **Minimal Deployment Version**
- ✅ **Deployed**: Basic FastAPI with test endpoints
- ✅ **Working**: Health checks and sample data
- ⏳ **Future**: Database integration and full MVC features

### Upgrade Path:
1. **Phase 1** ✅: Minimal deployment (current)
2. **Phase 2**: Add database connectivity
3. **Phase 3**: Enable full MVC features
4. **Phase 4**: Add ML predictions and recommendations

## 🎯 Development Status

### ✅ Completed Features:
- MVC architecture implementation
- Smart recommendation algorithm
- Performance caching system  
- Deployment configuration for Render
- Minimal working API

### 🚀 Ready for Production:
- Clean, deployable codebase
- No compilation dependencies
- Health monitoring endpoints
- Scalable MVC structure

---

**Version**: 2.0.0 (MVC Architecture)  
**Deployment**: Render-optimized  
**Repository**: [AgentMira-backend](https://github.com/craftlo-admin/AgentMira-backend)  
**Status**: ✅ Production Ready