import pymongo
from pymongo import MongoClient

import pandas as pd
from flask import Flask, abort, jsonify, make_response, render_template

from modules.preparation import AvocadoPrep
from modules.preparation.conf import DATA_LOCATION

# Remplacez <username> et <password> par vos informations d'identification
MONGODB_URI = "mongodb+srv://<dsti-devops>:<dsti-devops>@cluster0.piza0cu.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)
db = client["avocado_db"]

app = Flask(__name__)

def create_unique_id(item):
    unique_id = f'{item["date"]}-{item["small_plu"]}-{item["state"]}-{item["average_size_bags"]}-{item["region"]}-{item["season"]}'
    return unique_id

@app.route("/")
def home():
    return render_template(template_name_or_list="index.html")


@app.route("/avocados")
def get_avocados():
    preparation = AvocadoPrep(dataset_location=DATA_LOCATION)
    prepared_json = preparation.prepare(Json=True)

    # Créer un index unique pour éviter les doublons
    avocados_collection = mongo.db.avocados
    create_unique_index(avocados_collection)

    # Mettre à jour ou insérer les données JSON dans MongoDB
    for item in prepared_json:
        unique_id = create_unique_id(item)
        item["unique_id"] = unique_id
        avocados_collection.update_one({"unique_id": unique_id}, {"$set": item}, upsert=True)

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
