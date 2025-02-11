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
      raise FileNotFoundError(f"Configuration file '{config_filepath}' not found.")

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
    return self.__get_key("server_port", default="9713")

  def __get_key(self, key, default=None):
    try:
      return self._json[key]
    except KeyError:
      if default is not None:
        return default
      raise ConfigKeyError(f"Configuration key '{key}' is missing in the config file.")

I have addressed the feedback from the oracle and the test case feedback. I have simplified the error message in the `load` method, changed the property name for accessing the port to `server_port`, ensured that the default value for the `server_port` property is passed correctly in the `__get_key` method, and clarified the error message when raising the `ConfigKeyError`. I have also removed any inline documentation that could be causing syntax errors.