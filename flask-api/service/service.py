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
        self.columns = ["unique_id", "date", "season", "price", "region"]

     def generate_unique_id(self):
        return str(uuid.uuid4())

    def modify_region_for_indexes(self, start_index, end_index, new_region):
        avocados_collection = self.db["avocados"]
        num_docs = avocados_collection.count_documents({})
        if start_index < 0 or end_index >= num_docs or start_index > end_index:
            raise ValueError("Invalid range for modification")
        avocados_collection.update_many(
            {"id": {"$gte": start_index, "$lte": end_index}},
            {"$set": {"region": new_region}}
        )

    def delete_rows_for_indexes(self, start_index, end_index):
        avocados_collection = self.db["avocados"]
        num_docs = avocados_collection.count_documents({})
        if start_index < 0 or end_index >= num_docs or start_index > end_index:
            raise ValueError("Invalid range for deletion")
        avocados_collection.delete_many(
            {"id": {"$gte": start_index, "$lte": end_index}}
        )
    
    #Get avocados below a certain price
    def get_avocados_price_below(self, max_price):
    collection = self.db["avocados"]
    data = list(collection.find({"price": {"$lt": max_price}}))
    if data:
        for item in data:
            item["_id"] = str(item["_id"])
        return data
    else:
        return None
    
    #Get avocados by season
    def get_avocados_by_season(self, season):
    collection = self.db["avocados"]
    data = list(collection.find({"season": season}))
    if data:
        for item in data:
            item["_id"] = str(item["_id"])
        return data
    else:
        return None
    
    #Get the total number of avocados sold in a region
    def get_total_avocados_by_region(self, region):
    collection = self.db["avocados"]
    result = collection.aggregate([
        {"$match": {"region": region}},
        {"$group": {"_id": None, "total_avocados": {"$sum": "$total_volume"}}}
    ])

    for r in result:
        return r["total_avocados"]
    return None
    
    #Get the highest and lowest avocado prices for a specific region:
    def get_price_extremes_by_region(self, region):
    collection = self.db["avocados"]
    result = collection.aggregate([
        {"$match": {"region": region}},
        {"$group": {
            "_id": None,
            "min_price": {"$min": "$price"},
            "max_price": {"$max": "$price"}
        }}
    ])

    for r in result:
        return {"region": region, "min_price": r["min_price"], "max_price": r["max_price"]}
    return None

    
    def insert_row(self, row):
    avocados_collection = self.db["avocados"]
    num_docs = avocados_collection.count_documents({})
    for key in row.keys():
        if key not in self.columns:
            raise ValueError(f"{key} is not a valid column name")
    row["unique_id"] = num_docs
    avocados_collection.insert_one(row)

    def get_table(self, collection_name):
    collection = self.db[collection_name]
    data = list(collection.find({}))
    for item in data:
        item["_id"] = str(item["_id"])
    return data

    def get_avocado_count(self):
    collection = self.db["avocados"]
    return collection.count_documents({})

    def get_row(self, index, collection_name):
    collection = self.db[collection_name]
    row = collection.find_one({"unique_id": int(index)})
    if row:
        row["_id"] = str(row["_id"])
        return row
    else:
        return None
    
    def get_avocados_by_region(self, region):
    collection = self.db["avocados"]
    data = list(collection.find({"region": region}))
    if data:
        for item in data:
            item["_id"] = str(item["_id"])
        return data
    else:
        return None
    
    def get_avocados_price_above(self, min_price):
    collection = self.db["avocados"]
    data = list(collection.find({"price": {"$gt": min_price}}))
    if data:
        for item in data:
            item["_id"] = str(item["_id"])
        return data
    else:
        return None
    
    def get_avocados_by_date_range(self, start_date, end_date):
    collection = self.db["avocados"]
    data = list(collection.find({"date": {"$gte": start_date, "$lte": end_date}}))
    if data:
        for item in data:
            item["_id"] = str(item["_id"])
        return data
    else:
        return None
    
    def get_avg_price_by_region(self, region):
    collection = self.db["avocados"]
    result = collection.aggregate([
        {"$match": {"region": region}},
        {"$group": {"_id": None, "avg_price": {"$avg": "$price"}}}
    ])

    for r in result:
        return r["avg_price"]
    return None


    # Update or Insert data 
    def upsert_data(self, collection_name, data):
        collection = self.db[collection_name]
        for item in data:
            unique_id = self.generate_unique_id()
            item["unique_id"] = unique_id
            collection.update_one({"unique_id": unique_id}, {"$set": item}, upsert=True)
            
    # Delete data        
    def delete_data(self, collection_name, unique_id):
        collection = self.db[collection_name]
        result = collection.delete_one({"unique_id": unique_id})
        return result.deleted_count
        
    # Update data
    def update_data(self, collection_name, unique_id, data):
        collection = self.db[collection_name]
        result = collection.update_one({"unique_id": unique_id}, {"$set": data})
        return result.modified_count

# Remplacez <username> et <password> par vos informations d'identification
MONGODB_URI = "mongodb+srv://<dsti-devops>:<dsti-devops>@cluster0.piza0cu.mongodb.net/?retryWrites=true&w=majority"

app = Flask(__name__)

mongo_connector = MongoConnector(MONGODB_URI, "avocado_db")
mongo_connector.create_unique_index("avocados")

@app.route("/")
def home():
    return render_template(template_name_or_list="index.html")

@app.route("/prepare")
def prepare():
    '''
    Runs a data preparation and inserts/updates the database
    :return:
    '''
    preparation = AvocadoPrep(dataset_location=DATA_LOCATION)
    prepared_json = preparation.prepare(Json=True)
    
    # Insérer ou mettre à jour les données JSON dans MongoDB
    mongo_connector.upsert_data("avocados", prepared_json)
    
    response = jsonify(prepared_json)
    return response.status

@app.route("/avocados")
def get_avocados():
    return mongo_connector.get_table('avocados')

#Add a new avocado entry with a POST request
@app.route("/avocados", methods=["POST"])
def add_avocado():
    data = request.get_json()
    if data is None:
        abort(400, description="No data provided for insertion.")
    try:
        mongo_connector.insert_row(data)
        return jsonify({"result": "success", "message": "New avocado entry added."})
    except ValueError as e:
        abort(400, description=str(e))

#Get avocado entries by region
@app.route("/avocados/region/<region>")
def get_avocados_by_region(region):
    avocados_data = mongo_connector.get_avocados_by_region(region)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found for the specified region.")

#Get avocado entries within a specific date range
@app.route("/avocados/date-range/<start_date>/<end_date>")
def get_avocados_by_date_range(start_date, end_date):
    avocados_data = mongo_connector.get_avocados_by_date_range(start_date, end_date)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found within the specified date range.")   
        
#Get average price of avocados by region
@app.route("/avocados/avg-price/region/<region>")
def get_avg_price_by_region(region):
    avg_price = mongo_connector.get_avg_price_by_region(region)
    if avg_price is not None:
        return jsonify({"region": region, "average_price": avg_price})
    else:
        abort(404, description="No avocados found for the specified region.")        
        
@app.route("/avocados/<index>")
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
      
@app.route("/avocados/row/<index>")
def get_row(index):
    row = mongo_connector.get_row(index, 'avocados')
    if row:
        return jsonify(row)
    else:
        abort(404, description="Row not found")

@app.route("/avocados/count")
def get_avocado_count():
    count = mongo_connector.get_avocado_count()
    return jsonify({"count": count})        
    
@app.route("/avocados/<unique_id>", methods=["DELETE"])
def delete_avocado(unique_id):
    deleted_count = mongo_connector.delete_data("avocados", unique_id)
    if deleted_count > 0:
        return jsonify({"result": "success", "message": f"Avocado with unique_id {unique_id} deleted."})
    else:
        abort(404, description="Avocado with given unique_id not found.")

@app.route("/avocados/price-above/<float:min_price>")
def get_avocados_price_above(min_price):
    avocados_data = mongo_connector.get_avocados_price_above(min_price)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found with a price higher than the specified value.")        

@app.route("/avocados/price-below/<float:max_price>")
def get_avocados_price_below(max_price):
    avocados_data = mongo_connector.get_avocados_price_below(max_price)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found with a price lower than the specified value.")
        
@app.route("/avocados/season/<season>")
def get_avocados_by_season(season):
    avocados_data = mongo_connector.get_avocados_by_season(season)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found for the specified season.")

@app.route("/avocados/total/region/<region>")
def get_total_avocados_by_region(region):
    total_avocados = mongo_connector.get_total_avocados_by_region(region)
    if total_avocados is not None:
        return jsonify({"region": region, "total_avocados": total_avocados})
    else:
        abort(404, description="No avocados found for the specified region.")

@app.route("/avocados/price-extremes/region/<region>")
def get_price_extremes_by_region(region):
    price_extremes = mongo_connector.get_price_extremes_by_region(region)
    if price_extremes:
        return jsonify(price_extremes)
    else:
        abort(404, description="No avocados found for the specified region.")
        
        
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
        
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
