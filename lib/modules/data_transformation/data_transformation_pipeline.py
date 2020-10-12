from lib.modules.data_transformation.data_processing import (
    run_mentions_collection_pipeline,
)


def run_data_transformation(data_prep_output: dict) -> dict:
    """
    Run data transformation pipeline
        Params:
        --------
             data_prep_output (dict) : preprocessed files paths

        Returns:
        ---------
             data_processing_output (dict) : A dictionary containing the quality check operations result

    """
    data_transformation_output = run_mentions_collection_pipeline(data_prep_output)

    return data_transformation_output
