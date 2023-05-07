import os

import pytest
import json
from pymongo.errors import DuplicateKeyError
from modules import MongoConnector

# Test data
DATA = [
    {
        "average_size_bags": "small",
        "date": "2022-05-01",
        "region": "East",
        "season": "Spring",
        "small_plu": "4046",
        "state": "NY",
    },
    {
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
    uri = os.environ.get("MONGODB_URI")
    return MongoConnector(uri, "test_db")


def test_upsert_data(connector):
    # Test inserting new data into a collection
    connector.upsert_data("test_collection", json.dumps(DATA))
    assert connector.db["test_collection"].count_documents({}) == len(DATA)

    # Test updating existing data in a collection
    data = DATA[0]
    data["region"] = "West"
    connector.upsert_data("test_collection", json.dumps([data]))
    assert connector.db["test_collection"].count_documents({}) == len(DATA)
    assert connector.db["test_collection"].find_one({"region": "West"})["state"] == "NY"

    # Test handling of duplicate unique IDs
    with pytest.raises(DuplicateKeyError):
        connector.upsert_data("test_collection", json.dumps([data]))


def test_delete_data(connector):
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


def test_update_data(connector):
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


def test_get_avocado_count(connector):
    connector.upsert_data("avocados", json.dumps(DATA))
    assert connector.get_avocado_count() == len(DATA)
