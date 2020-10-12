import warnings

warnings.simplefilter("ignore")


QUARANTINE_ZONE_DIRECTORY = "./data/quarantine/"
PREPROCESSED_ZONE_DIRECTORY = "./data/preprocessed/"
EXPOSITION_ZONE_DIRECTORY = "./data/exposition/"

LIST_DATASRC = ["drugs", "clinical_trials", "pubmed"]
MENTIONS_SOURCES = ["clinical_trials", "pubmed"]
TITLE_COLUMN_NAME = "title"

DATASRC_CONFIG_PATH = "configurations/{}_datasrc_config.yaml"
SUCCESS_STATUS = "success"

QUALITY_CHECK_MANADATORY_TASKS = ["min_num_row", "required_columns"]
OUTPUT_JSON_FILENAME = "drugs_all_mentions"

ID_RELATION = "id_mention_relation"