import re
import os
from config import SUCCESS_STATUS
from lib.utils.tasks import generate_task_result


def run_data_retrieval(config_data_retrieval: dict) -> dict:
    """
    Run Data Retrieval Pipeline : retrieve all files for a given datasrc config

        Params:
        --------
             config_data_retrieval (dict) : A  data retreiva config dictionary for a given data source

        Returns:
        ---------
             data_retrieval_result (dict) : A dictionary containing the retreved filepaths

    """
    task_status = None
    task_result = None
    try:
        datasrc_files_directory = config_data_retrieval["file_path"]
        regex_filename = config_data_retrieval["filename"]
        list_datasrc_files_path = _get_data_source_files_path(
            datasrc_files_directory, regex_filename
        )
        retrieved_paths = list_datasrc_files_path[
            0
        ]  # here we suppose we have only one file for each datasrc
        task_status = SUCCESS_STATUS
    except Exception as e:
        task_status = e
    return generate_task_result(
        task_id="data_retrieval", task_status=task_status, task_result=retrieved_paths
    )


def _get_data_source_files_path(datasrc_directory: str, regex_filename: str) -> list:
    """
    Return list of files in a directory corresponding to a regex
        Params:
        --------
             datasrc_directory (str) : A directory to look for files into
             regex_filename (str) : regex to retrieve files

        Returns:
        ---------
             datasrc_regex_files (dict) : List of retrieved files
    """
    list_all_files_directory = os.listdir(datasrc_directory)
    datasrc_regex_files = [
        f"{datasrc_directory}{file_name}"
        for file_name in list_all_files_directory
        if re.match(regex_filename, file_name)
    ]
    return datasrc_regex_files
