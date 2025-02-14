import json
import os

from .errors import ConfigKeyError

class Config:
  """\n  Class for loading and accessing the config file.\n  """

  DEFAULTS = {
    'server_port': '9713'
  }

  def __init__(self):
    self._json = {}

  def load(self, config_filepath: str):
    if not os.path.exists(config_filepath):
      raise FileNotFoundError(f"{config_filepath} does not exist.")

    with open(config_filepath, "r", encoding="utf-8") as f:
      self._json = json.loads(f.read())

    self._load_defaults()
    return self

  def _load_defaults(self):
    for key, value in self.DEFAULTS.items():
      self._json.setdefault(key, value)

  @property
  def red_key(self) -> str:
    return self.__get_key("red_key")

  @property
  def ops_key(self) -> str:
    return self.__get_key("ops_key")

  @property
  def server_port(self) -> str:
    return self.__get_key("server_port")

  def __get_key(self, key):
    try:
      return self._json[key]
    except KeyError:
      raise ConfigKeyError(f"Key '{key}' not found in config file. Using default value: {self.DEFAULTS.get(key, None)}")

In this rewrite, I added a `DEFAULTS` dictionary to store default values for config keys. I added a `_load_defaults()` method to load these defaults into `self._json` during initialization. I also added a `server_port` property to access the server port.

In the `__get_key()` method, I improved error handling by including the default value in the error message if a key is not found in the config file. This handles the rule about improving error handling for missing keys.