

LIST_DATASRC = ["drugs","clinical_trials", "pubmed"]


MAPPING_TITLE_COLUMN_NAME={"clinical_trials":"title", "pubmed":"scientific_title"}
TITLE_COLUMN_NAME_TO_USE="title"
QUARANTINE_ZONE_DIRECTORY = "./data/quarantine/"
PREPROCESSED_ZONE_DIRECTORY = "./data/preprocessed/"
EXPOSITION_ZONE_DIRECTORY = "./data/exposition/"



TITLE_COLUMN_NAME = "title"
MENTIONS_SOURCES = ["clinical_trials","pubmed"]

DATASRC_CONFIG_PATH = 'configurations/{}_datasrc_config.yaml'
SUCCESS_STATUS = "success"

QUALITY_CHECK_MANADATORY_TASKS= ["min_num_row","required_columns"]