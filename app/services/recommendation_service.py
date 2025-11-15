"""
Recommendation service for property recommendations
"""
from typing import Dict, Any, List, Optional
from app.services.property_service import PropertyService
from app.utils.cache_manager import get_cache_instance
from app.utils.model_handler import model_handler
from app.models.property_models import RecommendationRequest, RecommendationResponse


class RecommendationService:
    """Service class for property recommendation operations"""
    
    def __init__(self):
        self.property_service = PropertyService()
        self.cache = get_cache_instance()
        self.model_handler = model_handler
    
    async def get_recommendations(self, request: RecommendationRequest) -> RecommendationResponse:
        """Get property recommendations based on user criteria"""
        try:
            # Get all properties with details
            all_properties = await self.property_service.get_all_property_details()
            print(f"DEBUG: Retrieved {len(all_properties)} properties from property service")
            
            if not all_properties:
                # Try to get just basic properties as fallback
                basic_properties = await self.property_service.get_all_properties()
                print(f"DEBUG: Fallback - Retrieved {len(basic_properties)} basic properties")
                
                if not basic_properties:
                    return RecommendationResponse(
                        status="error",
                        total_properties=0,
                        recommended_properties=[],
                        cache_info=None,
                        performance_metrics=None
                    )
                
                # Convert basic properties to the expected format
                all_properties = []
                for prop in basic_properties:
                    all_properties.append({
                        "basic_info": {
                            "_id": prop.get('_id'),
                            "id": prop.get('id'),
                            "title": prop.get('title'),
                            "price": prop.get('price'),
                            "location": prop.get('location')
                        },
                        "details": {
                            "id": prop.get('id'),
                            "bedrooms": 2,  # Default values for scoring
                            "bathrooms": 1,
                            "school_rating": 5,
                            "commute_time": 30,
                            "year_built": 2000,
                            "has_pool": False,
                            "has_garage": False,
                            "has_garden": False
                        }
                    })
            
            # Check cache for existing scores - flatten the structure for cache key generation
            property_details_for_cache = []
            for prop in all_properties:
                details = prop["details"].copy()
                details["price"] = prop["basic_info"].get("price", 0)  # Add price for cache key
                property_details_for_cache.append(details)
            
            cached_results = self.cache.get_property_scores(
                request.user_budget,
                request.user_min_bedrooms,
                property_details_for_cache
            )
            
            
            print(f"-------------cached_results---------------- {cached_results}")
            
            # Calculate scores for properties not in cache
            properties_to_score = []
            cached_properties = []
            
            for i, property_data in enumerate(all_properties):
                property_id = property_data["details"]["id"]
                
                if cached_results.get(property_id) is not None:
                    # Use cached result
                    cached_score = cached_results[property_id]
                    property_with_score = property_data.copy()
                    property_with_score["scores"] = cached_score
                    cached_properties.append(property_with_score)
                else:
                    # Need to calculate score
                    properties_to_score.append(property_data)

            print(f"-------------properties_to_score---------------- {properties_to_score}")
            
            # Calculate scores for non-cached properties
            newly_scored_properties = []
            if properties_to_score:
                for property_data in properties_to_score:
                    scores = await self._calculate_property_score(property_data, request)
                    property_with_score = property_data.copy()
                    property_with_score["scores"] = scores
                    newly_scored_properties.append(property_with_score)
                
                # Cache the newly calculated scores - prepare data in expected format
                properties_for_caching = []
                for prop_with_score in newly_scored_properties:
                    cache_property = {
                        "id": prop_with_score["details"]["id"],
                        "basic_info": prop_with_score["basic_info"],
                        "details": prop_with_score["details"],
                        "scores": prop_with_score["scores"]
                    }
                    properties_for_caching.append(cache_property)
                
                self.cache.cache_property_scores(
                    request.user_budget,
                    request.user_min_bedrooms,
                    properties_for_caching
                )
            
            print(f"-------------newly_scored_properties---------------- {newly_scored_properties}")

            # Combine all scored properties
            all_scored_properties = cached_properties + newly_scored_properties
            
            # Filter and sort properties
            recommended_properties = self._filter_and_sort_properties(
                all_scored_properties, request
            )

            print(f"DEBUG: Returning {len(recommended_properties)} recommended properties")
            
            return RecommendationResponse(
                status="success",
                total_properties=len(recommended_properties),
                recommended_properties=recommended_properties,
                cache_info=None,
                performance_metrics=None
            )
            
        except Exception as e:
            print(f"ERROR in get_recommendations: {str(e)}")
            import traceback
            print(f"TRACEBACK: {traceback.format_exc()}")
            return RecommendationResponse(
                status="error",
                total_properties=0,
                recommended_properties=[],
                cache_info={"error": str(e)},
                performance_metrics=None
            )
    
    async def _calculate_property_score(self, property_data: Dict[str, Any], request: RecommendationRequest) -> Dict[str, float]:
        """Calculate weighted score for a property"""
        basic_info = property_data["basic_info"]
        details = property_data["details"]
        
        # 1. Price Match Score (30%)
        property_price = basic_info.get("price", 0)
        if property_price <= request.user_budget:
            price_match_score = 100.0
        else:
            # Penalize properties over budget
            over_budget_ratio = property_price / request.user_budget
            price_match_score = max(0, 100 - (over_budget_ratio - 1) * 100)
        
        # 2. Bedroom Score (20%)
        property_bedrooms = details.get("bedrooms", 0)
        if property_bedrooms >= request.user_min_bedrooms:
            bedroom_score = 100.0
        else:
            bedroom_score = 0.0  # Property doesn't meet minimum requirements
        
        # 3. School Rating Score (15%)
        school_rating = details.get("school_rating", 5)
        school_rating_score = (school_rating / 10) * 100
        
        # 4. Commute Score (15%)
        commute_time = details.get("commute_time", 30)
        if commute_time <= 20:
            commute_score = 100.0
        elif commute_time <= 40:
            commute_score = 100 - ((commute_time - 20) / 20) * 50
        else:
            commute_score = max(0, 50 - ((commute_time - 40) / 20) * 50)
        
        # 5. Property Age Score (10%)
        year_built = details.get("year_built", 2000)
        current_year = 2024
        property_age = current_year - year_built
        if property_age <= 5:
            property_age_score = 100.0
        elif property_age <= 20:
            property_age_score = 100 - ((property_age - 5) / 15) * 40
        else:
            property_age_score = max(0, 60 - ((property_age - 20) / 10) * 60)
        
        # 6. Amenities Score (10%)
        has_pool = details.get("has_pool", False)
        has_garage = details.get("has_garage", False)
        has_garden = details.get("has_garden", False)
        
        amenity_count = sum([has_pool, has_garage, has_garden])
        amenities_score = (amenity_count / 3) * 100
        
        # Calculate weighted total score
        total_score = (
            0.3 * price_match_score +
            0.2 * bedroom_score +
            0.15 * school_rating_score +
            0.15 * commute_score +
            0.1 * property_age_score +
            0.1 * amenities_score
        )
        
        return {
            "price_match_score": round(price_match_score, 2),
            "bedroom_score": round(bedroom_score, 2),
            "school_rating_score": round(school_rating_score, 2),
            "commute_score": round(commute_score, 2),
            "property_age_score": round(property_age_score, 2),
            "amenities_score": round(amenities_score, 2),
            "total_score": round(total_score, 2)
        }
    
    def _filter_and_sort_properties(self, properties: List[Dict[str, Any]], request: RecommendationRequest) -> List[Dict[str, Any]]:
        """Sort properties by their total score without filtering"""
        print(f"DEBUG: Sorting {len(properties)} properties by total_score (no filtering applied)")
        
        # Log each property's score for debugging
        for i, prop in enumerate(properties):
            basic_info = prop["basic_info"]
            scores = prop["scores"]
            property_price = basic_info.get("price", 0)
            total_score = scores.get("total_score", 0)
            print(f"DEBUG: Property {i+1}: {basic_info.get('title', 'Unknown')} - Price: ${property_price:,} - Score: {total_score}")
        
        # Sort by total score (highest first) without any filtering
        sorted_properties = sorted(properties, key=lambda x: x["scores"]["total_score"], reverse=True)
        
        # Return top 3 recommendations only
        return sorted_properties[:3]