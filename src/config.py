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

  def __get_key(self, key, default=None):
    return self._json.get(key, default)

  @property
  def red_key(self) -> str:
    return self.__get_key("red_key")

  @property
  def ops_key(self) -> str:
    return self.__get_key("ops_key")

  @property
  def server_port(self) -> str:
    return self.__get_key("server_port", "9713")

  def test_returns_default_server_port(self):
    config = Config()
    assert config.server_port == "9713"

  def test_returns_config_server_port(self):
    config = Config()
    config._json = {"server_port": "8080"}
    assert config.server_port == "8080"


I've rewritten the code according to the provided rules. I've added a new `server_port` property that defaults to "9713". I've also changed the `__get_key` method to use `dict.get` to return the default value if the key is not present. I've added two test methods to ensure that the default value is correctly returned when no value is set and that the set value is correctly returned when it's present. I've also named the test methods more descriptively for clarity.