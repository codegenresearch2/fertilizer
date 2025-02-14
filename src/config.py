import json
import os

from .errors import ConfigKeyError

class Config:
  """\n  Class for loading and accessing the config file.\n  """

  def __init__(self):
    self._json = {}

  def load(self, config_filepath: str):
    if not os.path.exists(config_filepath):
      raise FileNotFoundError(f"Configuration file '{config_filepath}' does not exist.")

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
    return self.__get_key_with_default("server_port", "9713")

  def __get_key(self, key):
    try:
      return self._json[key]
    except KeyError:
      raise ConfigKeyError(f"Configuration key '{key}' is missing in the config file.")

  def __get_key_with_default(self, key, default):
    return self._json.get(key, default)


In the rewritten code, I have added a new property `server_port` that returns the server port from the config file. If the key is not found, it will return a default value of "9713". I have also clarified the error messages for missing keys in the `__get_key` method.