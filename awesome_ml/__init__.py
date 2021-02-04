from pathlib import Path
import logging.config
import yaml


def init_logging(default_level=logging.INFO):
    log_conf_file = Path(__file__).parent.joinpath('logging.yml')
    try:
        with open(log_conf_file) as fp:
            config = yaml.safe_load(fp)
        logging.config.dictConfig(config)
    except FileNotFoundError:
        logging.basicConfig(level=default_level)
        logging.getLogger(__name__).warning('Error configuring logging.')


init_logging()

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
