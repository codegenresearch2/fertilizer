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
      else:
        raise ConfigKeyError(f"Key '{key}' not found in config file.")

In the updated code, I have revised the error handling logic in the `__get_key` method to match the gold code. Now, the method directly tries to access the key and handles the `KeyError` in a single block. If a default value is provided and the key is not found, the method returns the default value. If no default value is provided and the key is not found, the method raises a `ConfigKeyError`. I have also ensured that the way I access keys in the `_json` dictionary is consistent with the gold code.