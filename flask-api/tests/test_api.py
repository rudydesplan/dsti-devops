import requests


def test_get_endpoint_returns_json_output():
    # Define the endpoint URL
    endpoint_url = "http://localhost:5000/avocados/0"

    # Make a GET request to the endpoint
    response = requests.get(endpoint_url)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response content type is JSON
    assert response.headers["Content-Type"] == "application/json"

    # Check that the response body is a valid JSON object
    try:
        json_data = response.json()
    except ValueError:
        assert False, "Response body is not valid JSON"

    # Check that the JSON object has the expected keys
    expected_keys = ["date", "small_plu", "state", "average_size_bags", "region", "season"]
    assert set(expected_keys).issubset(
        json_data.get("data")[0].keys()
    ), f"Expected keys {expected_keys} not found in response JSON"
