import os
from typing import cast

import toml
from box import Box


DEFAULT_CONFIG = os.path.join(os.path.dirname(__file__), "config.toml")


def load_toml(path: str) -> dict:
    """
    Loads a config dictionary from TOML
    """
    return {key: value for key, value in toml.load(cast(str, path)).items()}


config = load_toml(path=DEFAULT_CONFIG)
