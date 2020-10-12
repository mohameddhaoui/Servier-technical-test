
import pandas as pd
import json
from config import EXPOSITION_ZONE_DIRECTORY

def run_mentions_reduction(mentions_collection_output):
    df_all_mentions=pd.DataFrame()
    for collection_path in mentions_collection_output.values():
        json_collection = load_json(collection_path)
        df_collection = pd.DataFrame(json_collection["data"])
        df_all_mentions = pd.concat([df_all_mentions,df_collection], axis=0)
    return df_all_mentions

def export_all_mentions(df_all_mentions):
    df_mentions_todict = df_all_mentions.set_index('id_mention_relation').to_dict(orient='index')
    output_path= f"{EXPOSITION_ZONE_DIRECTORY}/drugs_all_mentions.json"
    save_dict_to_json(df_mentions_todict,output_path)
    return output_path

def load_json(filepath):
    with open(filepath) as f :
        res_json=json.load(f)
    return res_json
def save_dict_to_json(dictionary, filepath):
    with open(filepath, 'w') as fp:
        json.dump(dictionary, fp)