import os
from pathlib import Path
import pandas as pd

DEBUG = True

# ROOT = Path(__file__).parents[3].joinpath('root_dir')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    '..', '..', 'root_dir'))

# If set controller will use it to map code into the containers
HOST_ROOT = os.environ.get('HOST_ROOT', ROOT)

FS_OPTS = {}
CONTAINER_TASK_ENV = {
    'DRTOOLS_SETTINGS_MODULE': 'awesome_ml.settings.default'
}
CONTAINER_TASK_VOLUMES = {
    HOST_ROOT: {'bind': '/home/drtools/awesome_ml/root_dir'}
}
CONTAINER_TASK_IMAGE = 'drtools/awesome_ml:latest'
CONTAINER_TASK_NET = 'awesome_ml_dev'

# ---------------------- Data Processing --------------------

ID_COL = "id"
DATE_COL = "ts"
TARGET_COL = "target"

# Slicing
DEFAULT_N_AGG_DAYS = 90
LEAD_WINDOW_SIZE = 3


DEFAULT_TRAIN_DATES = pd.date_range("2016-10-01", "2016-10-31").date
DEFAULT_N_TEST_DAYS = 6

DEFAULT_TRAIN_SAMPLE = 10
DEFAULT_TEST_SAMPLE = 1

TIME_BINS = [
    (0, DEFAULT_N_AGG_DAYS)
]


# ---------------------- Evaluation --------------------

PRECISION_CUTOFFS = [4, 8, 16, 24]
CV_SPLIT_EVERY = 31
DAYS_BACK = 21
DAYS_FORWARD = 7
DATA_DELAY = 4


# ---------------------- LightFM --------------------

LFM_NTHREADS = 4

# ---------------------- XGBoost --------------------

XGB_NTHREADS = -1

# ----------------------- Plotting -------------------

FIGSIZE = (15, 5)