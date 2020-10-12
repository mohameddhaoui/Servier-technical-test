import os
from lib.utils.file import load_data, save_df
from lib.utils.dataframe import rename_one_column,cast_one_column,remove_nans, remove_special_char, remove_str_special_char
from lib.utils.tasks import generate_task_result, is_success
from config import SUCCESS_STATUS


def run_data_preprocessing_pipeline(df_filepath:str, datasrc_name:str, data_preprocessing_config:dict, output_directory:str, dependency:dict)-> dict:

    """
    Run Data preprocessing Pipeline : clean and structure columns

        Params:
        --------
             df_file_path (str) : filepath to check
             datasrc_name (str) : name of datasource
             data_preprocessing_config (dict) : preprocessing dictionary
             dependency (dict) : dependant task result

        Returns:
        ---------
             result_quality_checks (dict) : A dictionary containing the quality check operations result

    """
    if is_success(dependency) :
        try:
            df_data_transformation= transform_data(df_filepath, datasrc_name, data_preprocessing_config)
            output_preprocessed_filepath = f"{output_directory}{os.path.basename(df_filepath)}"
            save_df(df_data_transformation, output_preprocessed_filepath)
            task_result = output_preprocessed_filepath
            task_status = SUCCESS_STATUS
        except Exception as e :
            task_result = e
        return generate_task_result(task_id="data_preprocessing",task_status=task_status, task_result=task_result)



def transform_data(df_filepath, datasrc_name, data_preprocessing_config):
    df_data_transformation= load_data(df_filepath)
    if "column_transformation" in data_preprocessing_config.keys():
        df_data_transformation=transform_columns(df_data_transformation,
                                                data_preprocessing_config=data_preprocessing_config["column_transformation"])
    df_data_transformation["type"] = datasrc_name
    return df_data_transformation


def transform_columns(df, data_preprocessing_config):
    if "remove_nans" in data_preprocessing_config.keys():
        df = remove_nans(df, data_preprocessing_config["remove_nans"]["columns"])
    if "remove_special_char" in data_preprocessing_config.keys():
        df = remove_special_char(df, data_preprocessing_config["remove_special_char"]["columns"])
    if "column_types" in data_preprocessing_config.keys():
        for column_name, column_type in data_preprocessing_config["column_types"].items():
            df = cast_one_column(df, column_name,column_type)
    if "column_rename" in data_preprocessing_config.keys():
        for column_init_name, column_new_name in data_preprocessing_config["column_rename"].items():
            df = rename_one_column(df, column_init_name,column_new_name)
    return df
