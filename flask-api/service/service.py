import os

import pandas as pd
from flask import Flask, abort, jsonify, render_template, request
from modules import MongoConnector
from modules.preparation import AvocadoPrep

DATA_LOCATION = os.environ.get("DATASET_LOCATION")

MONGODB_URI = os.environ.get("MONGODB_URI")

app = Flask(__name__)

mongo_connector = MongoConnector(MONGODB_URI, "avocado_db")

REQUIRED_AVOCADO_FIELDS = [
    "average_size_bags",
    "date",
    "region",
    "season",
    "small_plu",
    "state",
]


@app.errorhandler(404)
def handle_not_found_error(error):
    return jsonify({"message": "Resource not found", "error": str(error)}), 404


# Health check and status endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK", "message": "API is up and running"})


# Render the home page
@app.route("/", methods=["GET"])
def home():
    return render_template(template_name_or_list="index.html")


# 2 Prepare the dataset and insert/update the data in the MongoDB database.
@app.route("/prepare", methods=["GET"])
def prepare():
    preparation = AvocadoPrep(dataset_location=DATA_LOCATION)
    prepared_json = preparation.prepare(Json=True)

    # Insérer ou mettre à jour les données JSON dans MongoDB
    mongo_connector.upsert_data("avocados", prepared_json.get("data", []))

    response = jsonify(prepared_json)
    return response.status


# Get the prepared avocado data for a specific unique_id
@app.route("/avocados/<index>", methods=["GET"])
def prepare_row(index):
    data = pd.read_csv(DATA_LOCATION)
    row = data.iloc[index]
    if not row.empty:
        prepared_row = AvocadoPrep(dataframe=pd.DataFrame(row).T).prepare(Json=True)
        mongo_connector.upsert_data("avocados", prepared_row.get("data", []))
        return jsonify(prepared_row)
    else:
        abort(404, description="Avocado with given unique_id not found")


# 3 Delete an avocado document using a unique ID
@app.route("/avocados/<unique_id>", methods=["DELETE"])
def delete_avocado(unique_id):
    deleted_count = mongo_connector.delete_data("avocados", unique_id)
    if deleted_count > 0:
        return (
            jsonify(
                {
                    "result": "success",
                    "message": f"Avocado with unique_id {unique_id} deleted.",
                }
            ),
            204,
        )
    else:
        abort(404, description="Avocado with given unique_id not found.")


# 5 Get the total number of avocado documents in the collection
@app.route("/avocados/count", methods=["GET"])
def get_avocado_count():
    count = mongo_connector.get_avocado_count()
    return jsonify({"count": count})


# 6 Get all avocado documents from the 'avocados' collection
@app.route("/avocados", methods=["GET"])
def get_avocados():
    avocados_data = mongo_connector.get_table("avocados")
    return jsonify(avocados_data)


# 7 Get a single document by its unique index from the avocados collection
@app.route("/avocados/row/<index>", methods=["GET"])
def get_row(index):
    row = mongo_connector.get_row(index, "avocados")
    if row:
        return jsonify(row)
    else:
        abort(404, description="Row not found")

        # A checker plus tard


# 8 Add a new avocado entry with a POST request
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
        unique_id = mongo_connector.insert_row(data)
        inserted_row = mongo_connector.get_row(unique_id, "avocados")
        return jsonify(inserted_row), 201
    except ValueError as e:
        abort(400, description=str(e))


# 11 Get avocado entries by region
@app.route("/avocados/region/<region>", methods=["GET"])
def get_avocados_by_region(region):
    avocados_data = mongo_connector.get_avocados_by_region(region)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found for the specified region.")


# 12 Get avocados for a specific season
@app.route("/avocados/season/<season>", methods=["GET"])
def get_avocados_by_season(season):
    avocados_data = mongo_connector.get_avocados_by_season(season)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found for the specified season.")


# 13 Get avocado entries within a specific date range
@app.route("/avocados/date-range/<start_date>/<end_date>", methods=["GET"])
def get_avocados_by_date_range(start_date, end_date):
    avocados_data = mongo_connector.get_avocados_by_date_range(start_date, end_date)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found within the specified date range.")


# 14 Get the average size bags for a specific region
@app.route("/avocados/average-size-bags/<region>", methods=["GET"])
def get_average_size_bags_by_region(region):
    avg_size_bags = mongo_connector.get_average_size_bags_by_region(region)
    if avg_size_bags is not None:
        return jsonify({"average_size_bags": avg_size_bags})
    else:
        abort(404, description="No data found for the specified region.")


# 15 Get the count of avocados with a specific small PLU code
@app.route("/avocados/small-plu/<small_plu>/count", methods=["GET"])
def get_avocados_count_by_small_plu(small_plu):
    count = mongo_connector.get_avocados_count_by_small_plu(small_plu)
    return jsonify({"count": count})


# 16 Get avocado documents by state
@app.route("/avocados/state/<state>", methods=["GET"])
def get_avocados_by_state(state):
    avocados_data = mongo_connector.get_avocados_by_state(state)
    if avocados_data:
        return jsonify(avocados_data)
    else:
        abort(404, description="No avocados found for the specified state.")


# 17 Get the count of avocado documents for a specific season and region
@app.route("/avocados/season/<season>/region/<region>/count", methods=["GET"])
def get_avocados_count_by_season_and_region(season, region):
    count = mongo_connector.get_avocados_count_by_season_and_region(season, region)
    return jsonify({"count": count})


# 18
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
    app.run(debug=False, host="0.0.0.0")
