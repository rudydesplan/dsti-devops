import pandas as pd
from flask import Flask, abort, jsonify, make_response, render_template

from modules.preparation import AvocadoPrep
from modules.preparation.conf import DATA_LOCATION

app = Flask(__name__)


@app.route("/")
def home():
    return render_template(template_name_or_list="index.html")


@app.route("/avocados")
def get_avocados():
    preparation = AvocadoPrep(dataset_location=DATA_LOCATION)
    prepared_json = preparation.prepare(Json=True)
    response = make_response(jsonify(prepared_json))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
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
