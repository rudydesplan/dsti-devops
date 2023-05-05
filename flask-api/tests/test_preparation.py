import json
import logging.config

import pandas as pd
import pytest
from modules.preparation import AvocadoPrep
from modules.preparation.conf import (
    AVOCADO_INPUT_COLUMNS,
    DATA_LOCATION,
    OUTPUT_COLUMN_NAMES,
)

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "stream": "ext://sys.stdout",
                "formatter": "simple",
            }
        },
        "loggers": {"": {"handlers": ["console"], "level": "INFO"}},
        "formatters": {"simple": {"format": "%(message)s"}},
    }
)


@pytest.fixture(scope="session")
def sample_input():
    df = pd.DataFrame(
        {
            "date": ["2015-12-28", "2015-04-28", "2015-08-28"],
            "average_price": [1.33, 1.35, 0.93],
            "total_volume": [64236.62, 54876.98, 118220.22],
            "4046": [1036.74, 674.28, 794.70],
            "4225": [54454.85, 44638.81, 109149.67],
            "4770": [48.16, 58.33, 130.50],
            "total_bags": [8696.87, 9505.56, 8145.35],
            "small_bags": [8603.62, 9408.07, 8042.21],
            "large_bags": [93.25, 97.49, 103.14],
            "x_large_bags": [0.0, 0.0, 0.0],
            "type": ["conventional", "conventional", "conventional"],
            "year": [2015, 2015, 2015],
            "region": ["Albany", "Sacramento", "ChicagoWashignton"],
        }
    )
    return df


@pytest.fixture(scope="session")
def sample_output():
    df_output = pd.DataFrame(
        {
            "date": ["12-28-2015", "04-28-2015", "08-28-2015"],
            "season": ["winter", "spring", "summer"],
            "small_plu": [48.16, 58.33, 130.5],
            "average_size_bags": [2898.96, 3168.52, 2715.12],
            "region": ["Albany", "Sacramento", "ChicagoWashignton"],
            "state": ["New York", "California", None],
        }
    )
    json_output = df_output.to_json(index=False, orient="table")
    json_output = json.loads(json_output)

    return {"df": df_output, "json": json_output}


def test_preparation_init(sample_input):
    prep = AvocadoPrep(dataframe=sample_input)
    assert prep.df is not None
    assert prep.dataset is not None
    assert prep.dataset.columns.names.difference(AVOCADO_INPUT_COLUMNS) == [None]

    prep2 = AvocadoPrep(dataset_location=DATA_LOCATION)
    assert prep2.df is not None
    assert prep2.dataset is not None
    assert prep2.dataset.columns.names.difference(AVOCADO_INPUT_COLUMNS) == [None]


def test_add_date_and_season(sample_input):
    # expected format is mm-dd-yyyy
    expected_date = ["12-28-2015", "04-28-2015", "08-28-2015"]
    expected_season = ["winter", "spring", "summer"]
    prep = AvocadoPrep(dataframe=sample_input)
    prep.add_date_and_season()

    result = prep.df
    assert result is not None
    for i in range(len(expected_date)):
        assert result.at[i, "date"] == expected_date[i]
        assert result.at[i, "season"] == expected_season[i]


def test_small_plu(sample_input):
    prep = AvocadoPrep(dataframe=sample_input)

    prep.add_small_plu()

    result = prep.df

    assert len(result["small_plu"]) == sample_input.shape[0]
    for i in range(len(sample_input)):
        assert result.at[i, "small_plu"] == min(
            sample_input.at[i, "4046"], sample_input.at[i, "4225"], sample_input.at[i, "4770"]
        )


def test_add_average_size_bags(sample_input):
    prep = AvocadoPrep(dataframe=sample_input)
    prep.add_average_size_bags()
    result = prep.df
    for i in range(len(sample_input)):
        assert result.at[i, "average_size_bags"] == round(float(sample_input.at[i, "total_bags"] / 3), 2)


def test_prepare_csv(tmp_path, sample_input, sample_output):
    # Save the sample_input DataFrame to a temporary CSV file
    temp_csv = tmp_path / "temp_data.csv"
    sample_input.to_csv(temp_csv, index=False)

    preparation = AvocadoPrep(dataset_location=temp_csv)
    prepared_json = preparation.prepare(Json=True)

    assert list(prepared_json["data"][0].keys()) == OUTPUT_COLUMN_NAMES
