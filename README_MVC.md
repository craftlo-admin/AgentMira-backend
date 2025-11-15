# Property Management API - MVC Architecture

## 🏗️ Architecture Overview

The codebase has been restructured to follow the **Model-View-Controller (MVC)** pattern for better organization, maintainability, and scalability.

## 📁 Directory Structure

```
Propertyone code backend/
├── 📄 main.py                 # Original application entry point
├── 📄 main_mvc.py            # New MVC application entry point  
├── 📄 routes.py              # Legacy routes (transitional)
├── 📄 models.py              # Legacy models (transitional)
├── 📄 database.py            # Legacy database config (transitional)
├── 📄 model_handler.py       # Legacy ML handler (transitional) 
├── 📄 cache_manager.py       # Legacy cache manager (transitional)
├── 🤖 complex_price_model_v2.pkl  # ML model file
│
└── 📁 app/                   # MVC Application Package
    ├── 📄 __init__.py        # Package initialization
    ├── 📄 main.py            # Pure MVC entry point (future)
    │
    ├── 📁 models/            # 🎯 DATA MODELS
    │   ├── 📄 __init__.py
    │   └── 📄 property_models.py    # Pydantic models & validation
    │
    ├── 📁 controllers/       # 🎮 REQUEST HANDLERS  
    │   ├── 📄 __init__.py
    │   ├── 📄 property_controller.py      # Property endpoints
    │   ├── 📄 prediction_controller.py    # ML prediction endpoints
    │   ├── 📄 recommendation_controller.py # Recommendation endpoints
    │   └── 📄 admin_controller.py         # Admin/health endpoints
    │
    ├── 📁 services/          # 💼 BUSINESS LOGIC
    │   ├── 📄 __init__.py  
    │   ├── 📄 property_service.py         # Property operations
    │   ├── 📄 prediction_service.py       # ML predictions
    │   └── 📄 recommendation_service.py   # Recommendation logic
    │
    ├── 📁 config/            # ⚙️ CONFIGURATION
    │   ├── 📄 __init__.py
    │   └── 📄 database_config.py          # Database settings
    │
    └── 📁 utils/             # 🛠️ UTILITIES
        ├── 📄 __init__.py
        ├── 📄 cache_manager.py            # Performance caching
        └── 📄 model_handler.py            # ML model management
```

## 🏛️ MVC Pattern Implementation

### 🎯 **Models** (`app/models/`)
- **Purpose**: Data structure definition and validation
- **Responsibilities**:
  - Pydantic models for request/response validation
  - Data type definitions
  - Input/output schemas
- **Files**:
  - `property_models.py`: All property-related data models

### 🎮 **Controllers** (`app/controllers/`)
- **Purpose**: Handle HTTP requests and responses  
- **Responsibilities**:
  - Route definition and HTTP handling
  - Request validation and response formatting
  - Error handling for API endpoints
- **Files**:
  - `property_controller.py`: Property CRUD operations
  - `prediction_controller.py`: ML prediction endpoints
  - `recommendation_controller.py`: Recommendation endpoints
  - `admin_controller.py`: Health checks and admin tools

### 💼 **Services** (`app/services/`)
- **Purpose**: Business logic and data processing
- **Responsibilities**:
  - Core business logic implementation
  - Data transformation and calculations  
  - Integration with external services/databases
- **Files**:
  - `property_service.py`: Property business logic
  - `prediction_service.py`: ML prediction logic
  - `recommendation_service.py`: Recommendation algorithms

## 🚀 Running the Application

### Option 1: MVC Version (Recommended)
```bash
cd "C:\Users\Himanshu Barnawal\Desktop\Agent Mira AI\Project 1\Propertyone code backend"
python -m uvicorn main_mvc:app --host 127.0.0.1 --port 8000
```

### Option 2: Legacy Version
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

## 📋 API Endpoints

### 🏠 Property Management
- `GET /properties` - Get all properties
- `GET /properties/{id}` - Get specific property
- `GET /properties/{id}/info` - Get property details
- `GET /properties/{id}/images` - Get property images
- `GET /properties/details/all` - Get all properties with details

### 🤖 ML Predictions  
- `POST /predict` - Predict property price
- `GET /pricedata` - Get model information

### 🎯 Recommendations
- `POST /recommend` - Get property recommendations

### ⚙️ Admin & Health
- `GET /health` - Health check
- `GET /database/status` - Database status
- `GET /cache/stats` - Cache statistics
- `POST /cache/clear` - Clear cache
- `POST /cache/cleanup` - Cleanup expired cache

## 🔄 Migration Strategy

The restructure follows a **gradual migration approach**:

1. **Phase 1** ✅ (Current): 
   - Created MVC structure
   - Moved code to appropriate layers
   - Maintained legacy files for compatibility

2. **Phase 2** (Future):
   - Update import statements
   - Remove legacy files  
   - Full MVC implementation

3. **Phase 3** (Future):
   - Add unit tests for each layer
   - Implement dependency injection
   - Add logging and monitoring

## ✨ Benefits of MVC Structure

### 🧹 **Better Organization**
- Clear separation of concerns
- Easier to locate and modify code
- Standardized project structure

### 🔧 **Maintainability**  
- Modular design allows independent updates
- Easier debugging and testing
- Better code reusability

### 📈 **Scalability**
- Easy to add new features/endpoints
- Can scale individual components
- Team collaboration friendly

### 🧪 **Testability**
- Each layer can be tested independently
- Mock dependencies easily
- Better unit test coverage

## 🛠️ Development Guidelines

### Adding New Features
1. **Model**: Define data structure in `app/models/`
2. **Service**: Implement business logic in `app/services/`  
3. **Controller**: Create API endpoints in `app/controllers/`
4. **Register**: Add router to main application

### Code Organization Principles
- **Models**: Pure data, no business logic
- **Services**: Business logic, no HTTP handling
- **Controllers**: HTTP only, delegate to services
- **Utils**: Shared functionality across layers

## 🎯 Next Steps

1. **Test MVC Application**: Use `main_mvc.py` for testing
2. **Validate Endpoints**: Ensure all functionality works
3. **Remove Legacy Files**: After validation, clean up old files
4. **Add Tests**: Implement comprehensive testing
5. **Documentation**: Update API documentation

## 📚 Documentation

- **API Docs**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

---

**Version**: 2.0.0  
**Architecture**: Model-View-Controller (MVC)  
**Framework**: FastAPI with MongoDB Atlas  
**Features**: Property management, ML predictions, Smart recommendations, Performance caching