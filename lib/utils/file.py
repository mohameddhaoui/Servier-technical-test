import pandas as pd
import yaml
import os
import shutil
import json
from config import DATASRC_CONFIG_PATH


def load_data(file_path: str, file_type="csv") -> object:
    """
    Load data given its path and filetype
    """
    if file_type == "csv":
        df = pd.read_csv(file_path)
        return df
    if file_type == "json":
        raise NotImplementedError


def load_datasrc_config(datasrc_name="drugs"):
    """
    Load datasrc configuration given datasrc_name
    """
    drugs_config_file = DATASRC_CONFIG_PATH.format(datasrc_name)
    config_drugs = load_yaml(drugs_config_file)
    return config_drugs


def load_yaml(yaml_path):
    """
    load yaml file
    """
    with open(yaml_path) as f:
        yaml_file = yaml.load(f)
    return yaml_file


def load_json(filepath):
    """
    load json file
    """
    with open(filepath) as f:
        res_json = json.load(f)
    return res_json


def save_dict_to_json(dictionary, filepath):
    """
    save dictionary to json file
    """
    with open(filepath, "w") as fp:
        json.dump(dictionary, fp)


def save_df(df, ouput_file_path):
    """
    save pandas dataframe to csv
    """
    df.to_csv(ouput_file_path, index=False)
