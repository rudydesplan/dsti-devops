import json
import os

import pytest
from modules import MongoConnector
from pymongo import MongoClient

# Test data
DATA = [
    {
        "unique_id": "1",
        "average_size_bags": "small",
        "date": "2022-05-01",
        "region": "East",
        "season": "Spring",
        "small_plu": "4046",
        "state": "NY",
    },
    {
        "unique_id": "2",
        "average_size_bags": "large",
        "date": "2022-05-01",
        "region": "West",
        "season": "Summer",
        "small_plu": "4225",
        "state": "CA",
    },
]


@pytest.fixture(scope="module")
def connector():
    try:
        uri = os.environ.get("MONGODB_URI")
        print("MongoDB URI: ", uri)
    except Exception as e:
        raise Exception("MongoDB URI not found in env variables")

    # Remove comment for local testing with docker-compsose
    # uri = "mongodb://dsti-devops:dsti-devops@localhost:27017/avocado_db?retryWrites=true&w=majority"

    client = MongoClient(uri)
    db_name = "avocado_db"
    client.drop_database(db_name)  # Drop the database if it already exists
    yield MongoConnector(uri, db_name)
    client.drop_database(db_name)  # Drop the database after running the tests


@pytest.fixture
def cleanup(connector):
    # Delete the test collection created in each test
    yield
    connector.db["test_collection"].drop()


def test_upsert_data(connector, cleanup):
    # Test inserting new data into a collection
    connector.upsert_data("test_collection", json.dumps(DATA))
    assert connector.db["test_collection"].count_documents({}) == len(DATA)

    # Test updating existing data in a collection
    data = DATA[0]
    data["region"] = "West"
    connector.upsert_data("test_collection", json.dumps([data]))
    assert connector.db["test_collection"].count_documents({}) == len(DATA)
    assert connector.db["test_collection"].find_one({"region": "West"})["state"] == "NY"


def test_delete_data(connector, cleanup):
    connector.upsert_data("test_collection", json.dumps(DATA))

    # Test deleting an existing document
    unique_id = connector.db["test_collection"].find_one()["unique_id"]
    result = connector.delete_data("test_collection", unique_id)
    assert result == 1
    assert connector.db["test_collection"].count_documents({}) == len(DATA) - 1

    # Test deleting a non-existent document
    result = connector.delete_data("test_collection", "invalid_id")
    assert result == 0
    assert connector.db["test_collection"].count_documents({}) == len(DATA) - 1


def test_update_data(connector, cleanup):
    connector.upsert_data("test_collection", json.dumps(DATA))

    # Test updating an existing document
    unique_id = connector.db["test_collection"].find_one()["unique_id"]
    data = {"state": "TX"}
    result = connector.update_data("test_collection", unique_id, data)
    assert result == 1
    assert (
        connector.db["test_collection"].find_one({"unique_id": unique_id})["state"]
        == "TX"
    )

    # Test updating a non-existent document
    result = connector.update_data("test_collection", "invalid_id", data)
    assert result == 0


def test_get_avocado_count(connector, cleanup):
    connector.upsert_data("avocados", json.dumps(DATA))
    assert connector.get_avocado_count() == len(DATA)
