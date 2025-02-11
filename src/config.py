import json
import os

from .errors import ConfigKeyError

class Config:
    """
    Class for loading and accessing the config file.
    """

    def __init__(self):
        self._json = {}

    def load(self, config_filepath: str):
        if not os.path.exists(config_filepath):
            raise FileNotFoundError(f"{config_filepath} does not exist.")

        with open(config_filepath, "r", encoding="utf-8") as f:
            self._json = json.loads(f.read())

        return self

    @property
    def red_key(self) -> str:
        return self.__get_key("red_key")

    @property
    def ops_key(self) -> str:
        return self.__get_key("ops_key")

    @property
    def server_port(self) -> str:
        return self.__get_key("port", "9713")

    def __get_key(self, key, default=None):
        try:
            return self._json[key]
        except KeyError:
            if default is not None:
                return default
            raise ConfigKeyError(f"Key '{key}' not found in config file.")

I have addressed the feedback from the oracle and the test case feedback. I have ensured that the indentation level is consistent throughout the code. I have also modified the default parameter in the `__get_key` method to be passed as a positional argument instead of a keyword argument. I have also double-checked the formatting of the error messages to ensure they match the expected formats.