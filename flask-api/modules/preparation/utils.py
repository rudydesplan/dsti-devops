import uuid
from functools import lru_cache
from typing import Optional

from geopy import Nominatim


def get_season(date: str) -> Optional[str]:
    """
    This function returns the season for a date in the format: yyyy-mm-dd
    :param date:
    :return:
    """
    month = int(date[5:7])
    day = int(date[8:10])
    if (month == 12 and day >= 21) or (month <= 3 and day < 21):
        return "winter"
    elif (month == 3 and day >= 21) or (month == 4) or (month == 5) or (month == 6 and day < 21):
        return "spring"
    elif (month == 6 and day >= 21) or (month == 7) or (month == 8) or (month == 9 and day < 21):
        return "summer"
    else:
        return "fall"


@lru_cache(maxsize=100)
def get_state(region: str) -> Optional[str]:
    geolocator = Nominatim(user_agent="my_app_name")

    try:
        location = geolocator.geocode(query=f"{region} + USA", addressdetails=True)
    except Exception as e:
        print(f"Warning: Failed requesting 'geocode': region={region}. {e}")
        return None

    if location is not None:
        state = location.raw["address"]["state"]
        print(f"Region: {region}, State: {state}")  # Add this line for debugging
        return state
