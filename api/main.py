from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv
import os
import json

app = FastAPI()
load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def search_by_name(name: str, limit: int = 1):
    """
    Search for a restaurant by name
    :param name: The name of the restaurant
    :param limit: The number of results to return
    :return: A list of restaurant IDs
    """
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': GOOGLE_MAPS_API_KEY,
        'X-Goog-FieldMask': 'places.id',
    }
    data = {
        "textQuery": name
    }
    url = 'https://places.googleapis.com/v1/places:searchText'
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        return_data = [d['id'] for d in data['places']]
        return return_data[:limit]
    else:
        raise HTTPException(status_code=400, detail="Error in Google Maps API call")

def get_restaurant(restaurant_id: str):
    """
    Get information about a restaurant by its ID
    :param restaurant_id: The ID of the restaurant
    :return: A dictionary containing the restaurant information
    """
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': GOOGLE_MAPS_API_KEY,
        'X-Goog-FieldMask': 'displayName,primaryType,googleMapsUri,businessStatus',
    }
    url = f'https://places.googleapis.com/v1/places/{restaurant_id}'
    response = requests.get(url, headers=headers)
    print(response.json())

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise HTTPException(status_code=400, detail="Error in Google Maps API call")

@app.get("/heartbeat")
async def heartbeat():
    return {"message": "Hello World"}

@app.get("/api/v1/search_restaurant")
async def search_restaurant(name: str):
    try:
        restaurant_id = search_by_name(name)
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    
    try:
        restaurant = get_restaurant(restaurant_id[0])
        return restaurant
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=e.detail)


        
