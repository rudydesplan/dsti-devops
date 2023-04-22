import json
import logging
from typing import Union

import pandas as pd
from pandas import DataFrame

from modules.preparation.conf import AVOCADO_INPUT_COLUMNS, OUTPUT_COLUMN_NAMES
from modules.preparation.utils import get_season, get_state

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class AvocadoPrep:
    def __init__(self, dataset_location: str = None, dataframe: DataFrame = None):
        """
        Prepares the avocado data as a json object, can take only one of parameters
        :param dataset_location: string value, path to dataset
        :param dataframe: a Pandas DataFrame object
        """
        logging.info("Initializing Data Preparation ...")
        # A single dataset for a preparation
        if (dataset_location is not None and dataframe is not None) or (dataset_location is None and dataframe is None):
            raise Exception("Must specify exactly one of: `dataset_path` or `dataset`.")

        if dataset_location is not None:
            try:
                self.dataset = pd.read_csv(dataset_location)
            except Exception as e:
                raise Exception(f"Failed reading csv file, make sure the path is correct. {e}")
            logging.info("Dataset successfully read from file.")
        elif dataframe.columns.names.difference(AVOCADO_INPUT_COLUMNS) == [None]:
            self.dataset = dataframe
            # Reset index of dataset
            self.dataset = self.dataset.reset_index()
            logging.info("Dataset successfully read from pandas DataFrame.")
        else:
            raise Exception(f"Error reading dataframe. Input schema must be same as: {AVOCADO_INPUT_COLUMNS}")

        # Initialize the preparation dataframe with specific column names
        self.df = pd.DataFrame(columns=OUTPUT_COLUMN_NAMES)

    def prepare(self, Json: bool = False) -> Union[DataFrame, str]:
        logging.info("Preparing Data ...")
        self.add_date_and_season()
        self.add_small_plu()
        self.add_average_size_bags()
        self.add_region_and_state()
        if Json is True:
            try:
                result = self.df.to_json(index=False, orient="table")
                parsed = json.loads(result)
            except Exception as e:
                raise Exception(f"Failed converting dataframe to JSON. {e}")
            logging.info("Data successfully prepared in JSON format !")
            return parsed
        else:
            logging.info("Data successfully prepared !")
            return self.df

    def add_date_and_season(self):
        # assign the column 'date' to df from original dataset
        self.df["date"] = self.dataset["date"]
        self.df["date"] = pd.to_datetime(self.df["date"], format="%Y-%m-%d")
        # format the 'date' column as "mm-dd-yyyy"
        self.df["date"] = self.df["date"].dt.strftime("%m-%d-%Y")

        # add 'season' column
        self.df["season"] = self.dataset["date"].apply(get_season)

    def add_small_plu(self):
        # small_plu is minimum of '4046', '4225', '4770' PLUs
        self.df["small_plu"] = self.dataset.apply(lambda row: min(row["4046"], row["4225"], row["4770"]), axis=1)

    def add_average_size_bags(self):
        self.df["average_size_bags"] = self.dataset.apply(lambda row: round(float(row["total_bags"]) / 3, 2), axis=1)

    def add_region_and_state(self):
        # copy the 'region' column
        self.df["region"] = self.dataset["region"]

        # add the 'state' column
        self.df["state"] = self.df["region"].apply(get_state)
