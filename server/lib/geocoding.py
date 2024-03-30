import os
from typing import Tuple

from dotenv import load_dotenv
from geopy import GoogleV3

load_dotenv()

GOOGLE_GEOCODING_API_KEY = os.getenv("GOOGLE_GEOCODING_API_KEY") or ""

geolocator = GoogleV3(api_key=GOOGLE_GEOCODING_API_KEY)


def geocoding_and_insert_coordinates(
    address: str,
) -> Tuple[float, float]:
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude  # type: ignore
        raise Exception("location not found")
    except:
        return 0, 0
