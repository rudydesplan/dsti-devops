from unittest.mock import patch

from modules.preparation.utils import generate_uuid, get_season, get_state


def test_get_season():
    assert get_season("2023-01-01") == "winter"
    assert get_season("2023-04-01") == "spring"
    assert get_season("2023-07-01") == "summer"
    assert get_season("2023-10-01") == "fall"


def test_get_state_with_successful_request():
    with patch("geopy.geocoders.Nominatim.geocode") as mock_geocode:
        # Set up the mock to return a mock location object with a state value when called
        mock_location = mock_geocode.return_value
        mock_location.raw = {"address": {"state": "New York"}}
        mock_location.address = "New York, USA"

        # Call the function with a region that should trigger a geocode request
        result = get_state("New York")

        # Verify that the result is "New York"
        assert result == "New York"

        # Verify that the geocode method was called with the expected arguments
        mock_geocode.assert_called_once_with(query="New York + USA", addressdetails=True)

        # Verify that the state value was cached by calling the function again with the same argument
        with patch("geopy.geocoders.Nominatim.geocode") as mock_geocode_cached:
            # Call the function again with the same argument
            result_cached = get_state("New York")

            # Verify that the result is "New York"
            assert result_cached == "New York"

            # Verify that the geocode method was not called the second time (since the value was cached)
            mock_geocode_cached.assert_not_called()
