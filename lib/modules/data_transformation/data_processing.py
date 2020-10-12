
import pandas as pd
import json
import re
from config import TITLE_COLUMN_NAME, MENTIONS_SOURCES, PREPROCESSED_ZONE_DIRECTORY
from lib.utils.file import load_json, save_dict_to_json

def run_mentions_collection_pipeline(data_prep_output:dict, dependecy:dict="") -> dict:
    """
    Run mentions collections for each drug from pubmed and clinical_trials
    """
    list_drugs = get_drugs_list(data_prep_output["drugs"])
    data_collection_output = {}
    for mentions_datasrc in MENTIONS_SOURCES:
        df_drug_mentions=run_drugs_mentions_collection_persource(data_prep_output, list_drugs,
                                                                 mentions_source=mentions_datasrc)
        output_collection_filepath = save_drugs_mentions(df_drug_mentions,mentions_datasrc )
        data_collection_output[mentions_datasrc] = output_collection_filepath

    return data_collection_output

def run_drugs_mentions_collection_persource(data_prep_output,list_drugs, mentions_source="pubmed"):
    df_mentions_source=pd.read_csv(data_prep_output[mentions_source])
    df_mentions_drugs=get_drugs_mentions(df_mentions_source,list_drugs)
    return df_mentions_drugs


def get_drugs_list(drugs_file_path):
    print(drugs_file_path)
    df_drugs=pd.read_csv(drugs_file_path, index_col=0).reset_index()
    list_drugs = list(df_drugs[["atccode","drug"]].T.to_dict().values())
    return list_drugs


def get_drugs_mentions(df_mentions, list_drugs):
    all_drugs_mentions= pd.DataFrame()
    for drug in list_drugs:
        drug_mentions = get_drug_mentioned_article(df_mentions,drug)
        all_drugs_mentions=pd.concat([all_drugs_mentions,drug_mentions], axis=0)
    all_drugs_mentions["id_mention_relation"] = all_drugs_mentions[['id','drug_atccode']].apply(lambda x : '{}-{}'.format(x[0],x[1]), axis=1)
    return all_drugs_mentions

def get_drug_mentioned_article(df_mentions, drug):
    df_res=df_mentions[df_mentions[TITLE_COLUMN_NAME].str.contains(re.compile(drug["drug"], re.I))]
    df_res["drug_name"]=drug["drug"]
    df_res["drug_atccode"]=drug["atccode"]
    df_res.drop("title", inplace=True, axis=1)
    return df_res

def save_drugs_mentions(df_mentions_drugs, datasrc_titles) :
    output_path = f"{PREPROCESSED_ZONE_DIRECTORY}drugs_{datasrc_titles}.json"
    df_mentions_drugs= df_mentions_drugs.T
    df_mentions_drugs.columns=[f"col{i}" for i in range(len(df_mentions_drugs.columns))]
    save_dict_to_json({"relation":f"drugs_{datasrc_titles}", "data": list(df_mentions_drugs.to_dict().values())}, output_path)
    return output_path
