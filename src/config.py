import json
import os

from .errors import ConfigKeyError

class Config:
  """\n  Class for loading and accessing the config file.\n  """

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
    return self.__get_key("server_port", default="9713")

  def __get_key(self, key, default=None):
    try:
      return self._json[key]
    except KeyError:
      if default is not None:
        return default
      raise ConfigKeyError(f"Key '{key}' not found in config file. Please check your configuration.")


In this rewritten code, I have added a new property `server_port` to the `Config` class that uses the `__get_key` method to retrieve the server port from the config file. If the key is not found, it will return a default value of "9713". I have also improved the error message for missing keys to provide more clarity to the user.