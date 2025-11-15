"""
Recommendation service for property recommendations
"""
from typing import Dict, Any, List
from app.services.property_service import PropertyService
from app.models.property_models import RecommendationRequest, RecommendationResponse


class RecommendationService:
    """Service class for property recommendation operations"""
    
    def __init__(self):
        self.property_service = PropertyService()
    
    async def get_recommendations(self, request: RecommendationRequest) -> RecommendationResponse:
        """Get property recommendations based on user criteria"""
        try:
            # Get all properties with details
            all_properties = await self.property_service.get_all_property_details()
            
            if not all_properties:
                return RecommendationResponse(
                    status="error",
                    total_properties=0,
                    recommended_properties=[],
                    cache_info=None,
                    performance_metrics=None
                )
            
            # Calculate scores for all properties (simplified - no caching complexity)
            all_scored_properties = []
            for property_data in all_properties:
                scores = await self._calculate_property_score(property_data, request)
                property_with_score = property_data.copy()
                property_with_score["scores"] = scores
                all_scored_properties.append(property_with_score)
            
            # Filter and sort properties
            recommended_properties = self._filter_and_sort_properties(
                all_scored_properties, request
            )
            
            return RecommendationResponse(
                status="success",
                total_properties=len(recommended_properties),
                recommended_properties=recommended_properties,
                cache_info=None,
                performance_metrics=None
            )
            
        except Exception as e:
            return RecommendationResponse(
                status="error",
                total_properties=0,
                recommended_properties=[],
                cache_info=None,
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
        """Filter properties within budget and sort by score"""
        # Filter: Only include properties within budget
        within_budget = []
        for prop in properties:
            property_price = prop["basic_info"].get("price", 0)
            if property_price <= request.user_budget:
                within_budget.append(prop)
        
        # Sort by total score (highest first)
        sorted_properties = sorted(within_budget, key=lambda x: x["scores"]["total_score"], reverse=True)
        
        # Return top 3 recommendations within budget
        return sorted_properties[:3]