import os
import pytest

from src.config import Config
from src.errors import ConfigKeyError

class TestConfig:
  def test_loads_config_correctly(self):
    config = Config().load("tests/support/settings.json")

    assert config.red_key == "red_key"
    assert config.ops_key == "ops_key"

  def test_raises_error_on_missing_config_file(self):
    with pytest.raises(FileNotFoundError) as excinfo:
      Config().load("tests/support/missing.json")

    assert "tests/support/missing.json does not exist" in str(excinfo.value)

  def test_raises_error_on_missing_key_without_default(self):
    with open("/tmp/empty.json", "w") as f:
      f.write("{}")

    config = Config().load("/tmp/empty.json")

    with pytest.raises(ConfigKeyError) as excinfo:
      config.red_key

    assert "Key 'red_key' not found in config file." in str(excinfo.value)
    os.remove("/tmp/empty.json")

  def test_returns_default_value_if_present(self):
    with open("/tmp/empty.json", "w") as f:
      f.write("{}")

    config = Config().load("/tmp/empty.json")
    assert config.server_port == "9713"
    os.remove("/tmp/empty.json")


In the revised code, I have removed the import statement for `SetupTeardown` as it was causing an `ImportError` as per the feedback. I have also ensured that the test method names are concise and reflect the purpose of the test. The assertions have been reviewed to ensure consistency with the expected values and messages. File cleanup is done consistently at the end of the tests. The code formatting has been adjusted to match the style of the gold code.