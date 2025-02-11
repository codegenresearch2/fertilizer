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

I have revised the code to address the feedback received.

1. In the `__get_key` method, I have simplified the error handling by always attempting to access the key and only checking for the default value in the exception handling, as suggested in the oracle feedback.

2. I have updated the `server_port` property to directly pass the default value as a second argument to the `__get_key` method, as suggested in the oracle feedback.

3. I have revised the error handling in the `__get_key` method to raise the `ConfigKeyError` only if the key is not found and no default is provided, as suggested in the oracle feedback.