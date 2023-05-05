import uuid

from flask import abort
from pymongo import MongoClient


class MongoConnector:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.columns = ["unique_id", "average_size_bags", "date", "region", "season", "small_plu", "state"]

    # 2 Update or insert data into a specified collection
    def upsert_data(self, collection_name, data):
        collection = self.db[collection_name]
        for item in data:
            unique_id = str(uuid.uuid4())
            item["unique_id"] = unique_id
            collection.update_one({"unique_id": unique_id}, {"$set": item}, upsert=True)

    # 3 Delete a document from a specified collection using a unique ID
    def delete_data(self, collection_name, unique_id):
        collection = self.db[collection_name]
        result = collection.delete_one({"unique_id": unique_id})
        return result.deleted_count

    # 4 Update a document in a specified collection using a unique ID and new data
    def update_data(self, collection_name, unique_id, data):
        collection = self.db[collection_name]
        result = collection.update_one({"unique_id": unique_id}, {"$set": data})
        return result.modified_count

    # 5 Get the total number of avocado documents in the collection
    def get_avocado_count(self):
        collection = self.db["avocados"]
        return collection.count_documents({})

    # 6 Get all documents from a specified collection
    def get_table(self, collection_name):
        collection = self.db[collection_name]
        data = list(collection.find({}))
        for item in data:
            item["_id"] = str(item["_id"])
        return data

    # 8 Insert a new row into the avocados collection
    def insert_row(self, row):
        avocados_collection = self.db["avocados"]
        for key in row.keys():
            if key not in self.columns:
                raise ValueError(f"{key} is not a valid column name")

        unique_id = str(uuid.uuid4())
        row["unique_id"] = unique_id
        avocados_collection.insert_one(row)
        return unique_id

    # 7 Get a single document by its unique index from a specified collection
    def get_row(self, unique_id, collection_name):
        collection = self.db[collection_name]
        row = collection.find_one({"unique_id": unique_id})
        if row:
            row["_id"] = str(row["_id"])
            return row
        else:
            abort(404, description="Row not found")

    # 11 Get avocados from a specific region
    def get_avocados_by_region(self, region):
        collection = self.db["avocados"]
        data = list(collection.find({"region": region}))
        if data:
            for item in data:
                item["_id"] = str(item["_id"])
            return data
        else:
            return None

    # 12 Get avocados for a specific season
    def get_avocados_by_season(self, season):
        collection = self.db["avocados"]
        data = list(collection.find({"season": season}))
        if data:
            for item in data:
                item["_id"] = str(item["_id"])
            return data
        else:
            return None

    # 13 Get avocados within a specific date range
    def get_avocados_by_date_range(self, start_date, end_date):
        collection = self.db["avocados"]
        data = list(collection.find({"date": {"$gte": start_date, "$lte": end_date}}))
        if data:
            for item in data:
                item["_id"] = str(item["_id"])
            return data
        else:
            return None

    # 14 Get the average size bags for a specific region
    def get_average_size_bags_by_region(self, region):
        collection = self.db["avocados"]
        result = collection.aggregate(
            [{"$match": {"region": region}}, {"$group": {"_id": None, "average": {"$avg": "$average_size_bags"}}}]
        )
        data = list(result)
        if data:
            return data[0]["average"]
        else:
            return None

    # 15 Get the count of avocados with a specific small PLU code
    def get_avocados_count_by_small_plu(self, small_plu):
        collection = self.db["avocados"]
        count = collection.count_documents({"small_plu": small_plu})
        return count

    # 16 Get avocado documents by state
    def get_avocados_by_state(self, state):
        collection = self.db["avocados"]
        data = list(collection.find({"state": state}))
        if data:
            for item in data:
                item["_id"] = str(item["_id"])
            return data
        else:
            return None

    # 17 Get the count of avocado documents for a specific season and region
    def get_avocados_count_by_season_and_region(self, season, region):
        collection = self.db["avocados"]
        count = collection.count_documents({"season": season, "region": region})
        return count

    # 18
    def search_avocados(self, filters):
        query = {}

        if "date" in filters:
            query["date"] = {"$gte": filters["date"].get("start", ""), "$lte": filters["date"].get("end", "")}

        if "region" in filters:
            query["region"] = filters["region"]

        if "season" in filters:
            query["season"] = filters["season"]

        if "small_plu" in filters:
            query["small_plu"] = filters["small_plu"]

        if "state" in filters:
            query["state"] = filters["state"]

        collection = self.db["avocados"]
        data = list(collection.find(query))
        if data:
            for item in data:
                item["_id"] = str(item["_id"])
            return data
        else:
            return None
