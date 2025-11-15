# AgentMira Backend - Property Management API

## 🏗️ MVC Architecture

A FastAPI-based property management system with ML-powered price predictions and smart recommendations.

## ✨ Features

- 🏠 **Property Management**: CRUD operations for properties, info, and images
- 🤖 **ML Price Prediction**: Intelligent property price forecasting  
- 🎯 **Smart Recommendations**: Personalized property suggestions with weighted scoring
- 💾 **Performance Caching**: Thread-safe caching with TTL and LRU eviction
- 🏛️ **MVC Architecture**: Clean separation of concerns for maintainability

## 📁 Project Structure

```
app/
├── models/           # 🎯 Data Models & Validation
│   └── property_models.py
├── controllers/      # 🎮 HTTP Request Handlers
│   ├── property_controller.py
│   ├── prediction_controller.py
│   ├── recommendation_controller.py
│   └── admin_controller.py
├── services/        # 💼 Business Logic
│   ├── property_service.py
│   ├── prediction_service.py
│   └── recommendation_service.py
├── config/          # ⚙️ Configuration
│   └── database_config.py
└── utils/           # 🛠️ Utilities & Caching
    ├── cache_manager.py
    └── model_handler.py
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB Atlas account
- Git

### Local Installation
```bash
# Clone the repository
git clone https://github.com/craftlo-admin/AgentMira-backend.git
cd AgentMira-backend

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your MongoDB credentials

# Run the application
python main.py
```

### 🌐 Deployment on Render

#### Option 1: Automatic Deployment
1. Fork this repository
2. Connect your GitHub account to [Render](https://render.com)
3. Create a new **Web Service**
4. Select your forked repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Add your MongoDB credentials
6. Deploy!

#### Option 2: Using render.yaml
1. Push this repository to GitHub
2. In Render, select "New" → "Blueprint"
3. Connect your repository
4. Render will automatically detect `render.yaml`
5. Add environment variables:
   - `MONGODB_PASSWORD`: Your MongoDB password
   - `ALLOWED_ORIGINS`: Your frontend URLs (comma-separated)

#### Environment Variables for Deployment
```bash
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
MONGODB_CLUSTER=your_cluster_url
MONGODB_DATABASE=property_database
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
API_HOST=0.0.0.0
PORT=10000
DEBUG_MODE=False
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

## 🎯 Recommendation Algorithm

The system uses a **6-component weighted scoring** algorithm:

- **Price Match (30%)**: Budget compatibility
- **Bedrooms (20%)**: Minimum bedroom requirements  
- **School Rating (15%)**: Educational quality score
- **Commute Time (15%)**: Location convenience
- **Property Age (10%)**: Building condition factor
- **Amenities (10%)**: Additional features (pool, garage, garden)

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB Atlas
- **ML Framework**: Scikit-learn
- **Caching**: Custom thread-safe implementation
- **Architecture**: Model-View-Controller (MVC)

## 📚 Documentation

- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

Update database credentials in `app/config/database_config.py`:

```python
self.username = "your_username"
self.password = "your_password" 
self.cluster_url = "your_cluster_url"
```

## 🎉 Features in Detail

### Performance Caching
- Thread-safe operations with `threading.RLock`
- LRU eviction policy for memory management
- TTL-based expiration (2 hours default)
- Hash-based cache keys for consistency

### ML Price Prediction
- Pre-trained model: `complex_price_model_v2.pkl`
- 9 input features for accurate predictions
- Error handling and model validation

### Smart Recommendations
- Multi-criteria property scoring
- Configurable user preferences
- Real-time cache integration
- Top 10 results with detailed metrics

---

**Version**: 2.0.0  
**License**: MIT  
**Author**: AgentMira Team