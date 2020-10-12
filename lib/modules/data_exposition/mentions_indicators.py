
import pandas as pd
from lib.utils.file import load_json
def get_journal_most_mentions(all_mentions_filepath:str)-> dict:

    """
    Return the journal having the most number of article mentions
        Params:
        --------
             all_mentions_filepath (str) : filepath containing the json of articles mentions

        Returns:
        ---------
             journal_max_mentions (dict) : The name of the journal having the most number of mentions

    """
    dict_all_mentions=load_json(all_mentions_filepath['json_drugs_relations_path'])
    df_all_mentions = pd.DataFrame.from_dict(dict_all_mentions, orient='index').reset_index()
    df_count_mentions_per_journal = pd.DataFrame(df_all_mentions.groupby('journal')["drug_atccode"].nunique()).reset_index()
    row_max_mentions = df_count_mentions_per_journal["drug_atccode"].argmax()
    journal_max_mentions = df_count_mentions_per_journal["journal"][row_max_mentions]
    return {"journal_max_mentions": journal_max_mentions}
