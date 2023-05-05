import re

import pandas as pd
import pytest
from modules.preparation import AvocadoPrep


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
            "region": ["Albany", "Sacramento", "Chicago"],
        }
    )
    return df


def test_init_wrong_number_params(sample_input):
    with pytest.raises(Exception, match=re.escape("Must specify exactly one of: `dataset_path` or `dataset`.")):
        AvocadoPrep(dataframe=sample_input, dataset_location="")

    with pytest.raises(Exception, match=re.escape("Must specify exactly one of: `dataset_path` or `dataset`.")):
        AvocadoPrep()


def test_init_wrong_dataset_location():
    with pytest.raises(Exception) as e:
        AvocadoPrep(dataset_location="")
        assert "Failed reading csv file, make sure the path is correct." in e


def test_init_wrong_column_names(sample_input):
    # rename column in the dataframe
    wrong_sample = sample_input.rename(columns={"date": "Date"})

    with pytest.raises(Exception) as e:
        AvocadoPrep(dataframe=wrong_sample)
        assert "Error reading dataframe. Input schema must be same as" in e
