
import pandas as pd
from lib.utils.file import load_data
from config import SUCCESS_STATUS
from lib.utils.tasks import is_success, generate_task_result

def run_data_quality_pipeline(df_file_path:str, dataquality_config:dict, dependency:dict) -> dict:
   """
    Run Data quality Pipeline : basic quality check on data

        Params:
        --------
             df_file_path (str) : filepath to check
             dataquality_config (dict) : quality check dictionary
             dependency (dict) : dependant task result

        Returns:
        ---------
             data_retrieval_result (dict) : A dictionary containing the retreved filepaths

    """
    task_status = None
    task_result = None
    if is_success(dependency):
        result_check_row = True
        result_required_columns= True
        df = load_data(df_file_path)
        if dataquality_config["min_num_row"]:
            result_check_row = check_min_row(df, dataquality_config["min_num_row"] )
        if dataquality_config["required_columns"]:
            result_required_columns = check_required_columns(df, dataquality_config["required_columns"])

        if result_check_row and result_required_columns :
            task_status = SUCCESS_STATUS

    return generate_task_result(task_id="data_quality",task_status=task_status, task_result={"min_num_row_result":result_check_row,
            "required_columns_result":result_required_columns})

def check_min_row(df, min_num_row):
    return df.shape[0]>= min_num_row

def check_required_columns(df, required_columns):
    return set(df.columns).issubset(set(required_columns))