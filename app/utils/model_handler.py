"""
Machine Learning model handler for price prediction
Simplified version without external dependencies
"""
from typing import Dict, Any, List


class SimplePredictionModel:
    """Simple prediction model that works without scikit-learn"""
    
    def __init__(self):
        # Simple coefficients for property price prediction
        self.coefficients = {
            'property_type': {'SFH': 1.0, 'Condo': 0.8, 'Townhouse': 0.9},
            'lot_area': 0.02,
            'building_area': 150.0,
            'bedrooms': 25000.0,
            'bathrooms': 15000.0,
            'year_built': 500.0,
            'has_pool': 20000.0,
            'has_garage': 15000.0,
            'school_rating': 8000.0,
            'base_price': 200000.0
        }
    
    def predict(self, data: Dict[str, Any]) -> List[float]:
        """Simple prediction based on linear combination"""
        try:
            # Base price
            price = self.coefficients['base_price']
            
            # Property type multiplier
            prop_type = data.get('property_type', 'SFH')
            type_multiplier = self.coefficients['property_type'].get(prop_type, 1.0)
            
            # Add contributions from each feature
            price += data.get('lot_area', 5000) * self.coefficients['lot_area']
            price += data.get('building_area', 1500) * self.coefficients['building_area']
            price += data.get('bedrooms', 3) * self.coefficients['bedrooms']
            price += data.get('bathrooms', 2) * self.coefficients['bathrooms']
            price += (data.get('year_built', 2010) - 1990) * self.coefficients['year_built']
            
            # Boolean features
            if data.get('has_pool', False):
                price += self.coefficients['has_pool']
            if data.get('has_garage', False):
                price += self.coefficients['has_garage']
            
            # School rating
            price += data.get('school_rating', 7) * self.coefficients['school_rating']
            
            # Apply property type multiplier
            final_price = price * type_multiplier
            
            return [max(50000, final_price)]  # Minimum price of $50k
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return [300000.0]  # Default price



class ModelHandler:
    """Handles loading and managing the ML model"""
    
    def __init__(self, model_path: str = "complex_price_model_v2.pkl"):
        self.model_path = model_path
        self.model = None
        self.is_loaded = False
        self.load_model()
    
    def load_model(self):
        """Load the simple prediction model"""
        try:
            print("🤖 Using SimplePredictionModel for reliable deployment")
            self.model = SimplePredictionModel()
            self.is_loaded = True
            
            # Test the model
            test_data = {
                "property_type": "SFH", "lot_area": 5000, "building_area": 1500,
                "bedrooms": 3, "bathrooms": 2, "year_built": 2015,
                "has_pool": True, "has_garage": False, "school_rating": 9
            }
            test_result = self.model.predict(test_data)
            print(f"✅ Model test result: {test_result}")
            
        except Exception as e:
            print(f"❌ Model error: {e}")
            self.model = SimplePredictionModel()  # Always fallback to simple model
            self.is_loaded = True
    
    def predict(self, data: Dict[str, Any]) -> List[float]:
        """Make prediction using the loaded model"""
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        return self.model.predict(data)
    



# Create global model handler instance
model_handler = ModelHandler()