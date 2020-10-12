
import pandas as pd
import json
from lib.utils.file import load_json, save_dict_to_json
from config import EXPOSITION_ZONE_DIRECTORY, OUTPUT_JSON_FILENAME

def run_mentions_reduction(data_transformation_output:dict):
    """
    Collect the ouptut of mentions in pubmed and clinical_trials
    Reduce the result into one datframe
    """
    df_all_mentions=pd.DataFrame()
    for collection_path in data_transformation_output.values():
        json_collection = load_json(collection_path)
        df_collection = pd.DataFrame(json_collection["data"])
        df_all_mentions = pd.concat([df_all_mentions,df_collection], axis=0)
    return df_all_mentions

def export_all_mentions(df_all_mentions):
    """
    Export the dataframe of all mentions into json
    """
    df_mentions_todict = df_all_mentions.set_index('id_mention_relation').to_dict(orient='index')
    output_path= f"{EXPOSITION_ZONE_DIRECTORY}/{OUTPUT_JSON_FILENAME}.json"
    save_dict_to_json(df_mentions_todict,output_path)
    return output_path
