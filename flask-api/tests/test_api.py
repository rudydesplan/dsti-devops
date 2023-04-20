import requests

#1 Test GET endpoint
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
    expected_keys = ["average_size_bags","date","region", "season", "small_plu", "state"]
    assert set(expected_keys).issubset(
        json_data.get("data")[0].keys()
    ), f"Expected keys {expected_keys} not found in response JSON"

#2 Test POST endpoint for creating a new avocado document
def test_post_endpoint_creates_new_avocado_document():
    # Define the endpoint URL
    endpoint_url = "http://localhost:5000/avocados"

    # Define the data to be sent in the POST request
    avocado_data = {
        "average_size_bags": 5,
        "date": "2023-01-01",
        "region": "West",
        "season": "spring"
        "small_plu": 12345,
        "state": "California",
    }

    # Make a POST request to the endpoint
    response = requests.post(endpoint_url, json=avocado_data)

    # Check that the response status code is 201 Created
    assert response.status_code == 201

    # Check that the response body is a valid JSON object and contains the created document's ID
    try:
        json_data = response.json()
        assert "id" in json_data
    except ValueError:
        assert False, "Response body is not valid JSON"

#3 Test PUT endpoint for updating an existing avocado document
def test_put_endpoint_updates_existing_avocado_document():
    # Define the endpoint URL
    unique_id = 1
    endpoint_url = f"http://localhost:5000/avocados/{unique_id}"

    # Define the data to be sent in the PUT request
    updated_data = {
        "average_size_bags": 10
    }

    # Make a PUT request to the endpoint
    response = requests.put(endpoint_url, json=updated_data)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is a valid JSON object and contains the updated document
    try:
        json_data = response.json()
        assert json_data["data"]["average_size_bags"] == updated_data["average_size_bags"]
    except ValueError:
        assert False, "Response body is not valid JSON"

#4 Test DELETE endpoint for deleting an existing avocado document
def test_delete_endpoint_deletes_existing_avocado_document():
    # Define the endpoint URL
    unique_id = 2
    endpoint_url = f"http://localhost:5000/avocados/{unique_id}"

    # Make a DELETE request to the endpoint
    response = requests.delete(endpoint_url)

    # Check that the response status code is 204 No Content
    assert response.status_code == 204
