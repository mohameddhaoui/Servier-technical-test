from lib.modules.data_exposition.mentions_structuration import run_mentions_reduction,export_all_mentions
from lib.modules.data_exposition.mentions_indicators import get_journal_most_mentions

def run_data_exposition(data_transformation_output:dict):
    """
    Run Data exposition Pipeline :
        - Collect data transformation output file ,fuse them into one file and export to json
        - Compute indicators : journal with max mentions of different drugs

        Params:
        --------
             data_transformation_output (dict) : processed filepaths of data transformation

        Returns:
        ---------
             result_data_exposition (tuple(dict)) :
                - A dictionary containing the path of the final json of drugs mentions and relations
                - A dictionary containting the indicators to compute

    """
    logger.info(f"-:----------- Collect data transformation output file ,fuse them into one file and export to json -:-")
    json_drugs_relations_output_path = generate_json_drugs_relations(data_transformation_output)

    logger.info(f"-:----------- Compute indicators -:-")
    journal_max_mentions = compute_mentions_indicators(json_drugs_relations_output_path)

    return json_drugs_relations_output_path, journal_max_mentions

def generate_json_drugs_relations(data_transformation_output:dict)-> dict:
    """
    Generate a DF of drugs mentions in the different datasrc and export as a json
    """
    df_all_mentions = run_mentions_reduction(data_transformation_output)
    df_all_mentions_output_path = export_all_mentions(df_all_mentions)
    return  {"json_drugs_relations_path":df_all_mentions_output_path}

def compute_mentions_indicators(json_drugs_relations_path:str) -> dict:
    """
    Compute indicators on json output file : journal with most mentions
    """
    indicator_journal_max_mentions = get_journal_most_mentions(json_drugs_relations_path)
    return indicator_journal_max_mentions