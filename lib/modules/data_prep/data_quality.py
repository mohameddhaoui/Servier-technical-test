
import pandas as pd
from lib.utils.file import load_data
from config import SUCCESS_STATUS
from config import QUALITY_CHECK_MANADATORY_TASKS
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
             result_quality_checks (dict) : A dictionary containing the quality check operations result

    """
    task_status = None
    task_result = None
    result_quality_checks = None
    if is_success(dependency):
        df_raw = load_data(df_file_path)
        result_quality_checks = perform_df_quality_checks(df_raw, dataquality_config)
        if all(res_quality_checks.values()):
            task_status = SUCCESS_STATUS

    return generate_task_result(task_id="data_quality",task_status=task_status, task_result=res_quality_checks)


def perform_df_quality_checks(df, dataquality_config:dict) -> dict:
    """
    Run a list of check operation on a dataframe
    """
    quality_check_res = {}
    for check_op in dataquality_config.keys() :
        res_qualiy_check = _data_quality_task(df, check_op)
        quality_check_res[check_op] = res_qualiy_check
    return quality_check_res

def _data_quality_task(df, quality_check_op) -> bool:
    """
    Run a check operation on a dataframe
    """
    if quality_check_op in QUALITY_CHECK_MANADATORY_TASKS :
        if quality_check_op == "min_num_row" :
            res_quality_check_op = check_min_row(df, dataquality_config["min_num_row"] )
        if quality_check_op == "required_columns" :
            res_quality_check_op = check_required_columns(df, dataquality_config["required_columns"])
        return res_quality_check_op
    else:
        raise ValueError(f"{quality_check_op} is not in quality check implemented operation")


def check_min_row(df, min_num_row) -> bool:
    """
    Check if a dataframe has at least min_num_row observations
    """
    return df.shape[0]>= min_num_row

def check_required_columns(df, required_columns) --> bool:
    """
    Check if all required columns exist in a dataframe
    """
    return set(df.columns).issubset(set(required_columns))