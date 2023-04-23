import requests


#1a Test GET endpoint with an invalid ID
def test_get_endpoint_with_invalid_id_returns_404():
    # Define the endpoint URL with an invalid ID
    invalid_id = -1
    endpoint_url = f"http://localhost:5000/avocados/{invalid_id}"

    # Make a GET request to the endpoint
    response = requests.get(endpoint_url)

    # Check that the response status code is 404 Not Found
    assert response.status_code == 404

#1c Test GET endpoint with a non-existent document ID
def test_get_endpoint_with_non_existent_document_returns_404():
    # Define the endpoint URL with a non-existent document ID
    non_existent_id = 99999999
    endpoint_url = f"http://localhost:5000/avocados/row/{non_existent_id}"

    # Make a GET request to the endpoint
    response = requests.get(endpoint_url)

    # Check that the response status code is 404 Not Found
    assert response.status_code == 404
    
#2a Test POST endpoint for creating a new avocado document
def test_post_endpoint_creates_new_avocado_document():
    # Define the endpoint URL
    endpoint_url = "http://localhost:5000/avocados"

    # Define the data to be sent in the POST request
    avocado_data = {
        "average_size_bags": 5.2,
        "date": "2023-01-01",
        "region": "West",
        "season": "spring",
        "small_plu": 12345.6,
        "state": "California",
    }

    # Make a POST request to the endpoint
    response = requests.post(endpoint_url, json=avocado_data)
    
    # Make a GET request to retrieve the new document
    response = requests.get(endpoint_url)

    # Check that the response body is a valid JSON object and contains the created document's ID
    try:
        json_data = response.json()
        print(json_data)
        
        # Check if "California" is in any of the "state" keys in the dictionaries
        california_found = any(entry.get("state") == "California" for entry in json_data)
        assert california_found, "California not found in the returned documents"
    except ValueError:
        assert False, "Response body is not valid JSON"

#2b Test POST endpoint with missing required fields
def test_post_endpoint_with_missing_fields_returns_400():
    # Define the endpoint URL
    endpoint_url = "http://localhost:5000/avocados"

    # Define the data to be sent in the POST request with missing required fields
    avocado_data = {
        "date": "2023-01-01",
        "season": "spring",
        "state": "California"
    }

    # Make a POST request to the endpoint
    response = requests.post(endpoint_url, json=avocado_data)

    # Check that the response status code is 400 Bad Request
    assert response.status_code == 400

        
#3a Test PUT endpoint for updating an existing avocado document
def test_put_endpoint_updates_existing_avocado_document():
    # Define the endpoint URL
    endpoint_url = "http://localhost:5000/avocados"
    
    # Define the avocado document data
    avocado_data = {
        "average_size_bags": 5.2,
        "date": "2023-01-01",
        "region": "West",
        "season": "spring",
        "small_plu": 12345.6,
        "state": "California",
    }
    
    # Make a POST request to the endpoint
    response = requests.post(endpoint_url, json=avocado_data)
    assert response.status_code == 201  # Check if the POST request was successful
   
    unique_id = created_avocado["unique_id"]
    endpoint_url_with_id = f"{endpoint_url}/{unique_id}"

    # Define the data to be sent in the PUT request
    updated_data = {
        "state": "Florida"
    }

    # Make a PUT request to the endpoint
    response = requests.put(endpoint_url_with_id, json=updated_data)

    # Check that the response status code is 200 OK
    assert response.status_code == 200
    
    # Make a GET request to retrieve the new document
    response = requests.get(endpoint_url_with_id)

    # Check that the response body is a valid JSON object and contains the created document's ID
    try:
        json_data = response.json()
        print(json_data)
        
        # Check if "Florida" is in any of the "state" keys in the dictionaries
        florida_found = any(entry.get("state") == "Florida" for entry in json_data)
        assert florida_found, "Florida not found in the returned documents"
    except ValueError:
        assert False, "Response body is not valid JSON"

#3b Test PUT endpoint with invalid data
def test_put_endpoint_with_invalid_data_returns_400():
    # Define the endpoint URL
    unique_id = 1
    endpoint_url = f"http://localhost:5000/avocados/{unique_id}"

    # Define the data to be sent in the PUT request with invalid data
    updated_data = {
        "average_size_bags": "invalid_data"
    }

    # Make a PUT request to the endpoint
    response = requests.put(endpoint_url, json=updated_data)

    # Check that the response status code is 400 Bad Request
    assert response.status_code == 400

#3c Test PUT endpoint with a non-existent document ID
def test_put_endpoint_with_non_existent_document_returns_404():
    # Define the endpoint URL with a non-existent document ID
    non_existent_id = 9999
    endpoint_url = f"http://localhost:5000/avocados/{non_existent_id}"

    # Define the data to be sent in the PUT request
    updated_data = {
        "average_size_bags": 10
    }

    # Make a PUT request to the endpoint
    response = requests.put(endpoint_url, json=updated_data)

    # Check that the response status code is 404 Not Found
    assert response.status_code == 404

#4a Test DELETE endpoint for deleting an existing avocado document
def test_delete_endpoint_deletes_existing_avocado_document():
    # Define the endpoint URL
    endpoint_url = "http://localhost:5000/avocados"
    
    # Define the avocado document data
    avocado_data = {
        "average_size_bags": 5.2,
        "date": "2023-01-01",
        "region": "West",
        "season": "spring",
        "small_plu": 12345.6,
        "state": "California",
    }
    
    # Make a POST request to the endpoint
    response = requests.post(endpoint_url, json=avocado_data)
    assert response.status_code == 201  # Check if the POST request was successful
   
    created_avocado = response.json()
    unique_id = created_avocado["unique_id"]
    endpoint_url_with_id = f"{endpoint_url}/{unique_id}"
    
    # Make a GET request to retrieve the new document
    response = requests.get(endpoint_url_with_id)

    # Check that the response body is a valid JSON object and contains the created document's ID
    print(response)

    # Make a DELETE request to the endpoint
    response = requests.delete(endpoint_url_with_id)

    # Test GET endpoint to confirm that the avocado document has been deleted
    response = requests.get(endpoint_url_with_id)
    print(response)

    # Check that the response status code is 404 Not Found
    assert response.status_code == 404

#4b Test DELETE endpoint with a non-existent document
def test_delete_endpoint_with_non_existent_document_returns_404():
    # Define the endpoint URL with a non-existent document ID
    non_existent_id = 9999
    endpoint_url = f"http://localhost:5000/avocados/{non_existent_id}"

    # Make a DELETE request to the endpoint
    response = requests.delete(endpoint_url)

    # Check that the response status code is 404 Not Found
    assert response.status_code == 404

#4c Test DELETE endpoint with a non-existent document ID
def test_delete_endpoint_with_non_existent_document_returns_404():
    # Define the endpoint URL with a non-existent document ID
    non_existent_id = 9999
    endpoint_url = f"http://localhost:5000/avocados/{non_existent_id}"

    # Make a DELETE request to the endpoint
    response = requests.delete(endpoint_url)

    # Check that the response status code is 404 Not Found
    assert response.status_code == 404
