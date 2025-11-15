# 🚀 Deployment Checklist for Render

## ✅ Files Created for Deployment

### 📦 **Core Deployment Files**
- ✅ `requirements.txt` - All Python dependencies
- ✅ `Procfile` - Process file for web service
- ✅ `render.yaml` - Render-specific configuration
- ✅ `runtime.txt` - Python version specification
- ✅ `.env.example` - Environment variables template
- ✅ `.gitignore` - Git ignore rules

### 🔧 **Updated Files**
- ✅ `main.py` - Added environment variable support & health check
- ✅ `README.md` - Added deployment instructions

## 🌐 Render Deployment Steps

### **Option 1: Web Service (Recommended)**

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up/Login with GitHub

2. **Connect Repository**
   - Click "New +" → "Web Service"
   - Connect to `craftlo-admin/AgentMira-backend`

3. **Configure Service**
   ```
   Name: agentmira-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Set Environment Variables**
   ```bash
   MONGODB_USERNAME=himanshubarnwal1126
   MONGODB_PASSWORD=[your_actual_password]
   MONGODB_CLUSTER=cluster0.q0dysfk.mongodb.net
   MONGODB_DATABASE=property_database
   ALLOWED_ORIGINS=https://yourdomain.com
   PORT=10000
   DEBUG_MODE=False
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

### **Option 2: Blueprint (Auto-config)**

1. **Use render.yaml**
   - Click "New +" → "Blueprint" 
   - Connect repository
   - Render auto-detects `render.yaml`

2. **Set Environment Variables**
   - Only need to set `MONGODB_PASSWORD`
   - Other variables are pre-configured

## 🔍 **Post-Deployment Verification**

### **Health Check**
```bash
curl https://your-app-name.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected", 
  "model": "loaded",
  "version": "2.0.0",
  "architecture": "MVC"
}
```

### **API Endpoints Test**
```bash
# Properties
curl https://your-app-name.onrender.com/properties/

# Prediction
curl -X POST https://your-app-name.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"bedrooms": 3, "bathrooms": 2}'

# Recommendation  
curl -X POST https://your-app-name.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"user_budget": 500000, "user_min_bedrooms": 3}'
```

### **Documentation**
- API Docs: `https://your-app-name.onrender.com/docs`
- ReDoc: `https://your-app-name.onrender.com/redoc`

## ⚡ **Performance & Monitoring**

### **Render Features**
- ✅ Auto-scaling
- ✅ SSL certificate (automatic)
- ✅ Custom domain support
- ✅ Health checks
- ✅ Deployment logs
- ✅ Environment variables

### **Monitoring Endpoints**
- `/health` - Application health
- `/cache/stats` - Cache performance
- `/database/status` - Database connectivity

## 🛠️ **Troubleshooting**

### **Common Issues**

1. **Build Failure**
   ```bash
   # Check requirements.txt format
   # Verify Python version in runtime.txt
   ```

2. **Database Connection**
   ```bash
   # Verify MongoDB Atlas whitelist (0.0.0.0/0 for Render)
   # Check environment variables
   ```

3. **Model Loading**
   ```bash
   # Ensure complex_price_model_v2.pkl is in repository
   # Check file size limits
   ```

### **Debug Commands**
```bash
# Check logs in Render dashboard
# View environment variables
# Monitor resource usage
```

## 📋 **Environment Variables Reference**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MONGODB_USERNAME` | ✅ | - | MongoDB username |
| `MONGODB_PASSWORD` | ✅ | - | MongoDB password |
| `MONGODB_CLUSTER` | ✅ | - | MongoDB cluster URL |
| `MONGODB_DATABASE` | ✅ | - | Database name |
| `ALLOWED_ORIGINS` | ⚠️ | `*` | CORS allowed origins |
| `PORT` | ❌ | `10000` | Server port (Render sets this) |
| `API_HOST` | ❌ | `0.0.0.0` | Server host |
| `DEBUG_MODE` | ❌ | `False` | Debug mode |
| `CACHE_TTL_HOURS` | ❌ | `2` | Cache TTL in hours |
| `CACHE_MAX_SIZE` | ❌ | `1000` | Maximum cache entries |

## 🎉 **Success!**

After successful deployment:
- ✅ API is live at `https://your-app-name.onrender.com`
- ✅ Documentation at `/docs`
- ✅ Health check at `/health`
- ✅ All endpoints working
- ✅ Database connected
- ✅ ML model loaded
- ✅ Caching active

---

**Ready for Production!** 🚀