"""
Fetch businesses from BizBuySell API with caching.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import requests

# BizBuySell API Configuration
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJhOTg2YTIyYS1kN2Y0LTQ1MGQtODQ5ZS1hNjBiNzdkMjEwYWIiLCJqdGkiOiI5MzZkZjk2YS1iYzBhLTQ3MjUtYmZlMi02OWVjMjZkYzNlNDkiLCJlbnMiOiIyMCIsInN1aWQiOiIiLCJiZnNyIjoiMCIsImRpZCI6IjEwIiwidWFpZCI6IjY5Mjg4MTEiLCJ1aXAiOiIyNC42My4xMjYuNzQiLCJleHAiOjE3NjgxOTUzMTEsImlzcyI6Imh0dHBzOi8vYXBpLmJpemJ1eXNlbGwuY29tIiwiYXVkIjoiYml6YnV5c2VsbCJ9.lpha0dRiifa9V0mXRncBvcxD6iVeyICkjQSMjd4JZDo"


def get_cache_path():
    """Get the path to the cache file."""
    return Path(__file__).parent.parent / "data" / "businesses_cache.json"


def load_cached_data():
    """Load businesses from cache if available."""
    cache_path = get_cache_path()
    if cache_path.exists():
        with open(cache_path, 'r') as f:
            data = json.load(f)
            print(f"Loaded {len(data.get('businesses', []))} businesses from cache")
            return data
    return None


def save_cache(data):
    """Save businesses to cache file."""
    cache_path = get_cache_path()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Cached data saved to {cache_path}")


def fetch_businesses(use_cache=True):
    """
    Fetch businesses from BizBuySell API.
    
    Args:
        use_cache (bool): Whether to use cached data if available
        
    Returns:
        dict: API response with businesses data
    """
    # Try to load from cache first
    if use_cache:
        cached_data = load_cached_data()
        if cached_data:
            return cached_data
    
    print("Fetching businesses from API...")
    
    url = 'https://api.bizbuysell.com/bff/v2/BbsBfsSearchResults'
    
    headers = {
        'X-LANE': '',
        'Authorization': f'Bearer {API_TOKEN}',
        'sec-ch-ua-platform': 'macOS',
        'X-Correlation-ID': 'aae88eda-4b2c-4497-ab49-4761dc9f0a06',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'Referer': 'https://www.bizbuysell.com/',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "bfsSearchCriteria": {
            "siteId": 20,
            "languageId": 10,
            "categories": [],
            "locations": [
                {
                    "geoType": 20,
                    "regionId": "20",
                    "countryCode": "US",
                    "countryId": "US",
                    "stateCode": "MA",
                    "legacyRegionId": 33,
                    "legacyRegionCode": "MA",
                    "regionName": "Massachusetts",
                    "regionNameSeo": "massachusetts",
                    "displayName": "Massachusetts",
                    "geoPinCriteria": None
                }
            ],
            "excludeLocations": None,
            "askingPriceMax": 200000,
            "askingPriceMin": 50000,
            "pageNumber": 1,
            "daysListedAgo": 0,
            "brokerCertification": 0,
            "includeRealEstateForLease": 0,
            "brokerMembership": 0,
            "listingTypeIds": [40, 30, 20],
            "designationTypeIds": [],
            "sortList": None,
            "listingsWithPriceReduced": 0,
            "daysModifiedAgo": 0,
            "seoSearchType": None
        },
        "industriesHierarchy": 10,
        "industriesFlat": 10,
        "bfsSearchResultsCounts": 0,
        "cmsFilteredData": 0,
        "rightRailBrokers": 0,
        "statesRegions": 10,
        "languageTypeId": 10
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Add metadata to cached data
        data['_cached_at'] = datetime.now().isoformat()
        
        # Save to cache
        save_cache(data)
        
        print(f"Successfully fetched and cached data")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        raise


if __name__ == "__main__":
    # Fetch and cache businesses
    businesses = fetch_businesses()
    print(f"Total results: {len(businesses)}")
