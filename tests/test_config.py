import os
import pytest

from src.config import Config
from src.errors import ConfigKeyError

class TestConfig:
  def test_loads_config(self, mock_config):
    assert mock_config.red_key == "secret_red"
    assert mock_config.ops_key == "secret_ops"

  def test_raises_error_on_missing_config_file(self):
    with pytest.raises(FileNotFoundError) as excinfo:
      Config().load("tests/support/missing.json")

    assert "tests/support/missing.json does not exist" in str(excinfo.value)

  def test_raises_error_on_missing_key(self, mock_config):
    mock_config._json = {}

    with pytest.raises(ConfigKeyError) as excinfo:
      mock_config.red_key

    assert "Key 'red_key' not found in config file." in str(excinfo.value)

  def test_server_port(self, mock_config):
    assert mock_config.server_port == "9713"
    mock_config._json["port"] = "8080"
    assert mock_config.server_port == "8080"

In this rewritten code, I have removed the unnecessary import of `SetupTeardown` and used the `mock_config` fixture from `conftest.py` to test the `Config` class. I have also added a new test for the `server_port` property.