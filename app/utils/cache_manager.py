#!/usr/bin/env python3
"""
Cache Manager for Property Recommendations
Handles caching of property scores and predictions to improve performance
"""
import json
import hashlib
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import threading


class RecommendationCache:
    """Thread-safe cache for property recommendation scores"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        """
        Initialize cache with maximum size and TTL (Time To Live)
        
        Args:
            max_size: Maximum number of cached entries
            ttl_seconds: Time to live for cached entries in seconds (default: 1 hour)
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.access_times: Dict[str, float] = {}
        self.lock = threading.RLock()
        
    def _generate_cache_key(self, user_budget: float, user_min_bedrooms: int, 
                          property_data: Dict[str, Any]) -> str:
        """
        Generate a unique cache key based on user input and property data
        
        Args:
            user_budget: User's budget
            user_min_bedrooms: User's minimum bedroom requirement
            property_data: Property information
            
        Returns:
            Unique cache key string
        """
        # Create a deterministic key based on user preferences and property features
        key_data = {
            "user_budget": user_budget,
            "user_min_bedrooms": user_min_bedrooms,
            "property_id": property_data.get("id"),
            "bedrooms": property_data.get("bedrooms"),
            "bathrooms": property_data.get("bathrooms"),
            "school_rating": property_data.get("school_rating"),
            "commute_time": property_data.get("commute_time"),
            "year_built": property_data.get("year_built"),
            "has_pool": property_data.get("has_pool"),
            "has_garage": property_data.get("has_garage"),
            "has_garden": property_data.get("has_garden"),
            "size_sqft": property_data.get("size_sqft"),
            "price": property_data.get("price")
        }
        
        # Convert to JSON string and hash for consistent key
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_expired(self, timestamp: float) -> bool:
        """Check if a cache entry is expired"""
        return (time.time() - timestamp) > self.ttl_seconds
    
    def _cleanup_expired(self) -> None:
        """Remove expired entries from cache"""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self.access_times.items()
            if (current_time - timestamp) > self.ttl_seconds
        ]
        
        for key in expired_keys:
            self.cache.pop(key, None)
            self.access_times.pop(key, None)
    
    def _evict_lru(self) -> None:
        """Evict least recently used entries if cache is full"""
        if len(self.cache) >= self.max_size:
            # Find the least recently used key
            lru_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            self.cache.pop(lru_key, None)
            self.access_times.pop(lru_key, None)
    
    def get_cached_score(self, user_budget: float, user_min_bedrooms: int, 
                        property_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get cached score for a property given user preferences
        
        Args:
            user_budget: User's budget
            user_min_bedrooms: User's minimum bedroom requirement
            property_data: Property information
            
        Returns:
            Cached score data or None if not found/expired
        """
        with self.lock:
            cache_key = self._generate_cache_key(user_budget, user_min_bedrooms, property_data)
            
            if cache_key in self.cache:
                # Check if expired
                if self._is_expired(self.access_times[cache_key]):
                    self.cache.pop(cache_key, None)
                    self.access_times.pop(cache_key, None)
                    return None
                
                # Update access time and return cached data
                self.access_times[cache_key] = time.time()
                return self.cache[cache_key]
            
            return None
    
    def set_cached_score(self, user_budget: float, user_min_bedrooms: int, 
                        property_data: Dict[str, Any], score_data: Dict[str, Any]) -> None:
        """
        Cache score data for a property given user preferences
        
        Args:
            user_budget: User's budget
            user_min_bedrooms: User's minimum bedroom requirement
            property_data: Property information
            score_data: Calculated score data to cache
        """
        with self.lock:
            # Cleanup expired entries
            self._cleanup_expired()
            
            # Evict LRU if necessary
            self._evict_lru()
            
            cache_key = self._generate_cache_key(user_budget, user_min_bedrooms, property_data)
            
            # Store the score data with metadata
            cached_entry = {
                "scores": score_data,
                "cached_at": datetime.now().isoformat(),
                "user_budget": user_budget,
                "user_min_bedrooms": user_min_bedrooms,
                "property_id": property_data.get("id")
            }
            
            self.cache[cache_key] = cached_entry
            self.access_times[cache_key] = time.time()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self.lock:
            total_entries = len(self.cache)
            expired_count = sum(1 for timestamp in self.access_times.values() 
                              if self._is_expired(timestamp))
            
            return {
                "total_entries": total_entries,
                "expired_entries": expired_count,
                "active_entries": total_entries - expired_count,
                "max_size": self.max_size,
                "ttl_seconds": self.ttl_seconds,
                "cache_hit_potential": f"{((total_entries - expired_count) / max(total_entries, 1)) * 100:.1f}%"
            }
    
    def clear_cache(self) -> None:
        """Clear all cached entries"""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
    
    def clear_expired(self) -> int:
        """Clear only expired entries and return count of cleared entries"""
        with self.lock:
            initial_count = len(self.cache)
            self._cleanup_expired()
            return initial_count - len(self.cache)


class PropertyScoreCache:
    """High-level interface for property recommendation caching"""
    
    def __init__(self, cache_size: int = 1000, ttl_hours: int = 1):
        """
        Initialize property score cache
        
        Args:
            cache_size: Maximum number of cached entries
            ttl_hours: Time to live in hours
        """
        self.cache = RecommendationCache(
            max_size=cache_size, 
            ttl_seconds=ttl_hours * 3600
        )
    
    def get_property_scores(self, user_budget: float, user_min_bedrooms: int, 
                          properties_data: List[Dict[str, Any]]) -> Dict[int, Optional[Dict[str, Any]]]:
        """
        Get cached scores for multiple properties
        
        Args:
            user_budget: User's budget
            user_min_bedrooms: User's minimum bedroom requirement
            properties_data: List of property information
            
        Returns:
            Dictionary mapping property_id to cached score data (None if not cached)
        """
        results = {}
        cache_hits = 0
        
        for prop_data in properties_data:
            prop_id = prop_data.get("id")
            cached_score = self.cache.get_cached_score(user_budget, user_min_bedrooms, prop_data)
            results[prop_id] = cached_score
            
            if cached_score is not None:
                cache_hits += 1
        
        # Log cache performance
        total_properties = len(properties_data)
        hit_rate = (cache_hits / total_properties) * 100 if total_properties > 0 else 0
        
        print(f"🎯 Cache Performance: {cache_hits}/{total_properties} hits ({hit_rate:.1f}% hit rate)")
        
        return results
    
    def cache_property_scores(self, user_budget: float, user_min_bedrooms: int, 
                            properties_scores: List[Dict[str, Any]]) -> None:
        """
        Cache scores for multiple properties
        
        Args:
            user_budget: User's budget
            user_min_bedrooms: User's minimum bedroom requirement
            properties_scores: List of property data with calculated scores
        """
        cached_count = 0
        
        for prop_score in properties_scores:
            # Extract property data for key generation
            property_data = {
                "id": prop_score.get("id"),
                "bedrooms": prop_score.get("details", {}).get("bedrooms"),
                "bathrooms": prop_score.get("details", {}).get("bathrooms"),
                "school_rating": prop_score.get("details", {}).get("school_rating"),
                "commute_time": prop_score.get("details", {}).get("commute_time"),
                "year_built": prop_score.get("details", {}).get("year_built"),
                "has_pool": prop_score.get("details", {}).get("has_pool"),
                "has_garage": prop_score.get("details", {}).get("has_garage"),
                "has_garden": prop_score.get("details", {}).get("has_garden"),
                "size_sqft": prop_score.get("details", {}).get("size_sqft"),
                "price": prop_score.get("basic_info", {}).get("price")
            }
            
            # Cache the scores
            score_data = prop_score.get("scores", {})
            self.cache.set_cached_score(user_budget, user_min_bedrooms, property_data, score_data)
            cached_count += 1
        
        print(f"💾 Cached scores for {cached_count} properties")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.cache.get_cache_stats()
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear_cache()
    
    def cleanup_expired(self) -> int:
        """Clean up expired entries"""
        return self.cache.clear_expired()


# Global cache instance
property_cache = PropertyScoreCache(cache_size=2000, ttl_hours=2)


def get_cache_instance() -> PropertyScoreCache:
    """Get the global cache instance"""
    return property_cache