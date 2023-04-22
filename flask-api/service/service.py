import uuid
import pymongo
from pymongo import MongoClient

import pandas as pd
from flask import Flask, abort, jsonify, make_response, render_template, request

from modules.preparation import AvocadoPrep
from modules.preparation.conf import DATA_LOCATION

class MongoConnector:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.columns = ["unique_id", "average_size_bags", "date", "region", "season", "small_plu", "state"]
        
    def create_unique_index(self, collection_name):
        collection = self.db[collection_name]
        collection.create_index("unique_id", unique=True)    
        
    #1 Generates a unique ID for each avocado document
    def generate_unique_id(self):
        return str(uuid.uuid4())
    
    #2 Update or insert data into a specified collection
    def upsert_data(self, collection_name, data):
        collection = self.db[collection_name]
        for item in data:
            unique_id = self.generate_unique_id()
            item["unique_id"] = unique_id
            collection.update_one({"unique_id": unique_id}, {"$set": item}, upsert=True)
            
    #3 Delete a document from a specified collection using a unique ID       
    def delete_data(self, collection_name, unique_id):
        collection = self.db[collection_name]
        result = collection.delete_one({"unique_id": unique_id})
        return result.deleted_count
        
    #4 Update a document in a specified collection using a unique ID and new data
    def update_data(self, collection_name, unique_id, data):
        collection = self.db[collection_name]
        result = collection.update_one({"unique_id": unique_id}, {"$set": data})
        return result.modified_count
    
    #5 Get the total number of avocado documents in the collection
    def get_avocado_count(self):
        collection = self.db["avocados"]
        return collection.count_documents({})
    
    #6 Get all documents from a specified collection
    def get_table(self, collection_name):
        collection = self.db[collection_name]
        data = list(collection.find({}))
        for item in data:
            item["_id"] = str(item["_id"])
        return data
        
    #8 Insert a new row into the avocados collection
    def insert_row(self, row):
        avocados_collection = self.db["avocados"]
        num_docs = avocados_collection.count_documents({})
        for key in row.keys():
            if key not in self.columns:
                raise ValueError(f"{key} is not a valid column name")
        row["unique_id"] = num_docs
        avocados_collection.insert_one(row)
        return num_docs  # Return the unique_id after inserting the row

    #7 Get a single document by its unique index from a specified collection
    def get_row(self, index, collection_name):
        collection = self.db[collection_name]
        row = collection.find_one({"unique_id": int(index)})
        if row:
            row["_id"] = str(row["_id"])
            return row
        else:
            abort(404, description="Row not found")

    
    
    #9 Modify the region value for avocado documents within a given index range
    def modify_region_for_indexes(self, start_index, end_index, new_region):
        avocados_collection = self.db["avocados"]
        num_docs = avocados_collection.count_documents({})
        if start_index < 0 or end_index >= num_docs or start_index > end_index:
            raise ValueError("Invalid range for modification")
        avocados_collection.update_many(
            {"id": {"$gte": start_index, "$lte": end_index}},
            {"$set": {"region": new_region}}
        )
        
    #10 Delete avocado documents within a given index range
    def delete_rows_for_indexes(self, start_index, end_index):
        avocados_collection = self.db["avocados"]
        num_docs = avocados_collection.count_documents({})
        if start_index < 0 or end_index >= num_docs or start_index > end_index:
            raise ValueError("Invalid range for deletion")
        avocados_collection.delete_many(
            {"id": {"$gte": start_index, "$lte": end_index}}
        )
    
    #11 Get avocados from a specific region
    def get_avocados_by_region(self, region):
        collection = self.db["avocados"]
        data = list(collection.find({"region": region}))
        if data:
            for item in data:
                item["_id"] = str(item["_id"])
            return data
        else:
            return None
    
    #12 Get avocados for a specific season
    def get_avocados_by_season(self, season):
        collection = self.db["avocados"]
        data = list(collection.find({"season": season}))
        if data:
            for item in data:
                item["_id"] = str(item["_id"])
            return data
        else:
            return None
    
    #13 Get avocados within a specific date range
    def get_avocados_by_date_range(self, start_date, end_date):
        collection = self.db["avocados"]
        data = list(collection.find({"date": {"$gte": start_date, "$lte": end_date}}))
        if data:
            for item in data:
                item["_id"] = str(item["_id"])
            return data
        else:
            return None
    #14 Get the average size bags for a specific region
    def get_average_size_bags_by_region(self, region):
        collection = self.db["avocados"]
        result = collection.aggregate([
            {"$match": {"region": region}},
            {"$group": {"_id": None, "average": {"$avg": "$average_size_bags"}}}
        ])
        data = list(result)
        if data:
            return data[0]["average"]
        else:
            return None

    #15 Get the count of avocados with a specific small PLU code
    def get_avocados_count_by_small_plu(self, small_plu):
        collection = self.db["avocados"]
        count = collection.count_documents({"small_plu": small_plu})
        return count

    #16 Get avocado documents by state
    def get_avocados_by_state(self, state):
        collection = self.db["avocados"]
        data = list(collection.find({"state": state}))
        if data:
            for item in data:
                item["_id"] = str(item["_id"])
            return data
        else:
            return None

    #17 Get the count of avocado documents for a specific season and region
    def get_avocados_count_by_season_and_region(self, season, region):
        collection = self.db["avocados"]
        count = collection.count_documents({"season": season, "region": region})
        return count
    
    #18
    def search_avocados(self, filters):
        query = {}

        if 'date' in filters:
            query['date'] = {'$gte': filters['date'].get('start', ''), '$lte': filters['date'].get('end', '')}

        if 'region' in filters:
            query['region'] = filters['region']

        if 'season' in filters:
            query['season'] = filters['season']

        if 'small_plu' in filters:
            query['small_plu'] = filters['small_plu']

        if 'state' in filters:
            query['state'] = filters['state']

        collection = self.db['avocados']
        data = list(collection.find(query))
        if data:
            for item in data:
                item["_id"] = str(item["_id"])
            return data
        else:
            return None


# Remplacez <username> et <password> par vos informations d'identification
MONGODB_URI = "mongodb+srv://dsti-devops:dsti-devops@cluster0.piza0cu.mongodb.net/?retryWrites=true&w=majority"

app = Flask(__name__)

mongo_connector = MongoConnector(MONGODB_URI, "avocado_db")
mongo_connector.create_unique_index("avocados")

REQUIRED_AVOCADO_FIELDS = ["average_size_bags", "date", "region", "season", "small_plu", "state"]

@app.errorhandler(404)
def handle_not_found_error(error):
    return jsonify({
        "message": "Resource not found",
        "error": str(error)
    }), 404

# Health check and status endpoint
@app.route("/health", methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "message": "API is up and running"})

# Render the home page
@app.route("/", methods=['GET'])
def home():
    return render_template(template_name_or_list="index.html")

#2 Prepare the dataset and insert/update the data in the MongoDB database.
@app.route("/prepare", methods=['GET'])
def prepare():
    preparation = AvocadoPrep(dataset_location=DATA_LOCATION)
    prepared_json = preparation.prepare(Json=True)
    
    # Insérer ou mettre à jour les données JSON dans MongoDB
    mongo_connector.upsert_data("avocados", prepared_json)
    
    response = jsonify(prepared_json)
    return response.status

# Get the prepared avocado data for a specific index        
@app.route("/avocados/<index>", methods=['GET'])
def prepare_row(index):
    index = int(index)
    data = pd.read_csv(DATA_LOCATION)
    if index in range(data.shape[0]):
        row = data.iloc[index].to_frame().T
        preparation = AvocadoPrep(dataframe=row)
        prepared_row = preparation.prepare(Json=True)
        return jsonify(prepared_row)
    else:
        abort(404, description="Index out of range")

#3 Delete an avocado document using a unique ID    
@app.route("/avocados/<unique_id>", methods=["DELETE"])
def delete_avocado(unique_id):
    deleted_count = mongo_connector.delete_data("avocados", unique_id)
    if deleted_count > 0:
        return jsonify({"result": "success", "message": f"Avocado with unique_id {unique_id} deleted."}),204
    else:
        abort(404, description="Avocado with given unique_id not found.")

#4 Update an avocado document using a unique ID and new data        
@app.route("/avocados/<unique_id>", methods=["PUT"])
def update_avocado(unique_id):
    data = request.get_json()
    if data is None:
        abort(400, description="No data provided for update.")
    
    modified_count = mongo_connector.update_data("avocados", unique_id, data)
    if modified_count > 0:
        return jsonify({"result": "success", "message": f"Avocado with unique_id {unique_id} updated."})
    else:
        abort(404, description="Avocado with given unique_id not found.")
        
#5 Get the total number of avocado documents in the collection
@app.route("/avocados/count", methods=['GET'])
def get_avocado_count():
    count = mongo_connector.get_avocado_count()
    return jsonify({"count": count})        
        
#6 Get all avocado documents from the 'avocados' collection
@app.route("/avocados")
def get_avocados():
    return mongo_connector.get_table('avocados')

#7 Get a single document by its unique index from the avocados collection
@app.route("/avocados/row/<index>", methods=['GET'])
def get_row(index):
    row = mongo_connector.get_row(index, 'avocados')
    if row:
        return jsonify(row)
    else:
        abort(404, description="Row not found")

        #A checker plus tard
#8 Add a new avocado entry with a POST request
@app.route("/avocados", methods=["POST"])
def add_avocado():
    data = request.get_json()
    if data is None:
        abort(400, description="No data provided for insertion.")

    # Check for missing required fields
    missing_fields = [field for field in REQUIRED_AVOCADO_FIELDS if field not in data]
    if missing_fields:
        abort(400, description=f"Missing required fields: {', '.join(missing_fields)}")

    try:
        inserted_id = mongo_connector.insert_row(data)
        inserted_row = mongo_connector.get_row(inserted_id, 'avocados')
        return jsonify(inserted_row), 201
    except ValueError as e:
        abort(400, description=str(e))



#11 Get avocado entries by region
@app.route("/avocados/region/<region>", methods=['GET'])
def get_avocados_by_region(region):
    avocados_data = mongo_connector.get_avocados_by_region(region)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found for the specified region.")

#12 Get avocados for a specific season        
@app.route("/avocados/season/<season>", methods=['GET'])
def get_avocados_by_season(season):
    avocados_data = mongo_connector.get_avocados_by_season(season)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found for the specified season.")        
        
#13 Get avocado entries within a specific date range
@app.route("/avocados/date-range/<start_date>/<end_date>", methods=['GET'])
def get_avocados_by_date_range(start_date, end_date):
    avocados_data = mongo_connector.get_avocados_by_date_range(start_date, end_date)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found within the specified date range.")   

#14 Get the average size bags for a specific region      
@app.route("/avocados/average-size-bags/<region>", methods=['GET'])
def get_average_size_bags_by_region(region):
    avg_size_bags = mongo_connector.get_average_size_bags_by_region(region)
    if avg_size_bags is not None:
        return jsonify({"average_size_bags": avg_size_bags})
    else:
        abort(404, description="No data found for the specified region.")       

#15 Get the count of avocados with a specific small PLU code
@app.route("/avocados/small-plu/<small_plu>/count", methods=['GET'])
def get_avocados_count_by_small_plu(small_plu):
    count = mongo_connector.get_avocados_count_by_small_plu(small_plu)
    return jsonify({"count": count})

#16 Get avocado documents by state
@app.route("/avocados/state/<state>", methods=['GET'])
def get_avocados_by_state(state):
    avocados_data = mongo_connector.get_avocados_by_state(state)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found for the specified state.")
        
#17 Get the count of avocado documents for a specific season and region
@app.route("/avocados/season/<season>/region/<region>/count", methods=['GET'])
def get_avocados_count_by_season_and_region(season, region):
    count = mongo_connector.get_avocados_count_by_season_and_region(season, region)
    return jsonify({"count": count})

#18
@app.route("/avocados/search", methods=["POST"])
def search_avocados():
    filters = request.get_json()
    if filters is None:
        abort(400, description="No filters provided for search.")
    # Implement a function in the MongoConnector class to search based on filters
    avocados_data = mongo_connector.search_avocados(filters)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found matching the specified filters.")
        
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
