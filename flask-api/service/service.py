import pymongo
from pymongo import MongoClient

import pandas as pd
from flask import Flask, abort, jsonify, make_response, render_template

from modules.preparation import AvocadoPrep
from modules.preparation.conf import DATA_LOCATION

class MongoConnector:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

     # Créer un index unique pour éviter les doublons
    def create_unique_index(self, collection_name):
        try:
            self.db[collection_name].create_index("unique_id", unique=True)
        except pymongo.errors.OperationFailure as e:
            print(f"Erreur lors de la création de l'index unique : {e}")

    def upsert_data(self, collection_name, data):
        collection = self.db[collection_name]
        for item in data:
            unique_id = create_unique_id(item)
            item["unique_id"] = unique_id
            collection.update_one({"unique_id": unique_id}, {"$set": item}, upsert=True)

# Remplacez <username> et <password> par vos informations d'identification
MONGODB_URI = "mongodb+srv://<dsti-devops>:<dsti-devops>@cluster0.piza0cu.mongodb.net/?retryWrites=true&w=majority"

app = Flask(__name__)

mongo_connector = MongoConnector(MONGODB_URI, "avocado_db")
mongo_connector.create_unique_index("avocados")

@app.route("/")
def home():
    return render_template(template_name_or_list="index.html")


@app.route("/avocados")
def get_avocados():
    preparation = AvocadoPrep(dataset_location=DATA_LOCATION)
    prepared_json = preparation.prepare(Json=True)

    # Insérer ou mettre à jour les données JSON dans MongoDB
    mongo_connector.upsert_data("avocados", prepared_json)

    response = jsonify(prepared_json)
    return response

@app.route("/avocados/<index>")
def get_by_id(index):
    index = int(index)
    data = pd.read_csv(DATA_LOCATION)
    if index in range(data.shape[0]):
        row = data.iloc[index].to_frame().T
        preparation = AvocadoPrep(dataframe=row)
        prepared_row = preparation.prepare(Json=True)
        return jsonify(prepared_row)
    else:
        abort(404, description="Index out of range")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
