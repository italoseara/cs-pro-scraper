import os
import requests
from PIL import Image
from io import BytesIO
from typing import Any, Union


def find_in_object(data: Union[dict, list], keys: list) -> Any:
    """Recursively finds a value in a nested dictionary or list using a list of keys."""
    
    if not keys:
        return None  # No keys to search for

    if isinstance(data, dict):
        current_key = keys[0]
        if current_key in data:
            return data[current_key] if len(keys) == 1 else find_in_object(data[current_key], keys[1:])
        
        # Search in all values of the dictionary
        for value in data.values():
            result = find_in_object(value, keys)
            if result is not None:  # Ensure None values are not treated as "not found"
                return result

    elif isinstance(data, list):
        # Search in all elements of the list
        for item in data:
            result = find_in_object(item, keys)
            if result is not None:
                return result

    return None


def download_image(url: str) -> Image:
    """Download an image from the given URL."""

    response = requests.get(url)
    response.raise_for_status()
    
    return Image.open(BytesIO(response.content))


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

# This is a hardcoded value for X, it's the same for everyone
X_API_KEY = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
