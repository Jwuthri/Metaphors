import os


# ROOT PATH
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PROJECT_PATH)

# REPORTS PATH
REPORTS_PATH = os.path.join(PROJECT_ROOT, "reports")
PLOT_PATH = os.path.join(REPORTS_PATH, "figures")

# DATA PATH
DATASET_PATH = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_PATH = os.path.join(DATASET_PATH, "raw_data")
PROCESSED_DATA_PATH = os.path.join(DATASET_PATH, "processed_data")
EXTERNAL_DATA_PATH = os.path.join(DATASET_PATH, "external_data")
INTERIM_DATA_PATH = os.path.join(DATASET_PATH, "interim_data")
ASSETS_DATA_PATH = os.path.join(DATASET_PATH, "assets_data")

# ASSETS PATH
VERY_LIGHT_STOPWORDS_PATH = os.path.join(ASSETS_DATA_PATH, "VERY_LIGHT_STOPWORDS.json")
LIGHT_STOPWORDS_PATH = os.path.join(ASSETS_DATA_PATH, "LIGHT_STOPWORDS.json")
NORMAL_STOPWORDS_PATH = os.path.join(ASSETS_DATA_PATH, "NORMAL_STOPWORDS.json")
STRONG_STOPWORDS_PATH = os.path.join(ASSETS_DATA_PATH, "STRONG_STOPWORDS.json")
