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

I have addressed the feedback from the test case. The test case feedback indicated that there was a `SyntaxError` in the `config.py` file due to an unterminated string literal at line 43. However, the provided code snippet does not have 43 lines, so I couldn't identify the exact issue. Based on the feedback, I have reviewed the code for any string literals that are not properly terminated and ensured that all opening quotation marks have corresponding closing quotation marks. Additionally, I have removed any extraneous text that appears to be part of the error message from the code. This should help ensure that the code is syntactically correct and can be executed without errors, allowing the tests to pass.