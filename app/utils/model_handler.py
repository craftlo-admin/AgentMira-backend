"""
Machine Learning model handler for price prediction
"""
import pickle
import os
from typing import Dict, Any, List


class CustomUnpickler(pickle.Unpickler):
    """Custom unpickler to handle class loading issues"""
    
    def find_class(self, module, name):
        if name == 'ComplexTrapModelRenamed':
            return ComplexTrapModelRenamed
        return super().find_class(module, name)


class ComplexTrapModelRenamed:
    """Model class for handling the pickled model"""
    
    def __init__(self):
        pass
    
    def predict(self, data: Dict[str, Any]) -> List[float]:
        """Predict method - will be overridden by the actual model"""
        return [100000.0]


class ModelHandler:
    """Handles loading and managing the ML model"""
    
    def __init__(self, model_path: str = "complex_price_model_v2.pkl"):
        self.model_path = model_path
        self.model = None
        self.is_loaded = False
        self.load_model()
    
    def load_model(self):
        """Load the model from pickle file"""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file {self.model_path} not found")
            
            with open(self.model_path, 'rb') as f:
                self.model = CustomUnpickler(f).load()
                self.is_loaded = True
                
                print("✅ Successfully loaded model from pickle file")
                print(f"Model type: {type(self.model)}")
                
                # Test the model with the expected format
                test_data = {
                    "property_type": "SFH",
                    "lot_area": 5000,
                    "building_area": 1500,
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "year_built": 2015,
                    "has_pool": True,
                    "has_garage": False,
                    "school_rating": 9
                }
                test_result = self.model.predict(test_data)
                print(f"Model test result: {test_result}")
                
        except Exception as e:
            print(f"❌ Error loading model from pickle: {e}")
            print("Using fallback model")
            self.model = ComplexTrapModelRenamed()
            self.is_loaded = False
    
    def predict(self, data: Dict[str, Any]) -> List[float]:
        """Make prediction using the loaded model"""
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        return self.model.predict(data)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if self.model is None:
            return {"error": "Model not loaded"}
        
        return {
            "model_type": str(type(self.model)),
            "model_class": self.model.__class__.__name__,
            "model_module": getattr(self.model.__class__, '__module__', 'unknown'),
            "is_loaded": self.is_loaded,
            "model_path": self.model_path
        }
    
    def get_model_attributes(self) -> Dict[str, Any]:
        """Get all public attributes of the model"""
        if self.model is None:
            return {}
        
        model_attributes = {}
        for attr_name in dir(self.model):
            if not attr_name.startswith('_'):  # Skip private methods
                try:
                    attr_value = getattr(self.model, attr_name)
                    if callable(attr_value):
                        model_attributes[attr_name] = f"<method: {attr_name}>"
                    else:
                        try:
                            import json
                            json.dumps(attr_value)
                            model_attributes[attr_name] = attr_value
                        except (TypeError, ValueError):
                            model_attributes[attr_name] = str(attr_value)
                except Exception as e:
                    model_attributes[attr_name] = f"<error accessing: {str(e)}>"
        
        return model_attributes
    
    def get_sample_predictions(self) -> Dict[str, Any]:
        """Generate sample predictions for testing"""
        if self.model is None:
            return {}
        
        sample_predictions = {}
        test_cases = [
            {
                "property_type": "SFH",
                "lot_area": 4000,
                "building_area": 1200,
                "bedrooms": 2,
                "bathrooms": 1,
                "year_built": 2010,
                "has_pool": False,
                "has_garage": True,
                "school_rating": 6
            },
            {
                "property_type": "SFH",
                "lot_area": 5000,
                "building_area": 1500,
                "bedrooms": 3,
                "bathrooms": 2,
                "year_built": 2015,
                "has_pool": True,
                "has_garage": False,
                "school_rating": 9
            },
            {
                "property_type": "Condo",
                "lot_area": 0,
                "building_area": 1000,
                "bedrooms": 2,
                "bathrooms": 2,
                "year_built": 2020,
                "has_pool": True,
                "has_garage": True,
                "school_rating": 8
            },
            {
                "property_type": "SFH",
                "lot_area": 8000,
                "building_area": 2500,
                "bedrooms": 5,
                "bathrooms": 4,
                "year_built": 2022,
                "has_pool": True,
                "has_garage": True,
                "school_rating": 10
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            try:
                prediction = self.model.predict(test_case)
                sample_predictions[f"test_case_{i+1}"] = {
                    "input": test_case,
                    "prediction": prediction
                }
            except Exception as e:
                sample_predictions[f"test_case_{i+1}"] = {
                    "input": test_case,
                    "error": str(e)
                }
        
        return sample_predictions


# Create global model handler instance
model_handler = ModelHandler()