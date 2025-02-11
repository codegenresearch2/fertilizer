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
    return self.__get_key_with_default("server_port", "9713")

  def __get_key(self, key):
    try:
      return self._json[key]
    except KeyError:
      raise ConfigKeyError(f"Key '{key}' not found in config file.")

  def __get_key_with_default(self, key, default):
    return self._json.get(key, default)


In the rewritten code, I have added a new property `server_port` to the `Config` class. This property uses the `__get_key_with_default` method to return the value of the `server_port` key in the config file, or a default value of `9713` if the key is not found. This ensures that default values are tested, as per the user's preference. I have also updated the test names in the `TestConfig` class to be more descriptive, as per the user's preference.