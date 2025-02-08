import os\"nimport pytest\"n\nfrom src.config import Config\nfrom src.errors import ConfigKeyError\n\n\ndef test_loads_config():\"""\nTest that the config loads correctly.\"""\n    config = Config().load(\"tests/support/settings.json\")\n    assert config.red_key == \"secret_red\"\n    assert config.ops_key == \"secret_ops\"\n\ndef test_raises_error_on_missing_config_file():\"""\nTest that an error is raised when the config file is missing.\"""\n    with pytest.raises(FileNotFoundError):\n        Config().load(\"tests/support/missing.json\")\n\ndef test_raises_error_on_missing_key():\"""\nTest that an error is raised when a key is missing from the config file.\"""\n    with open(\"/tmp/empty.json\", \"w\") as f:\n        f.write(\"{}\")\n    config = Config().load(\"/tmp/empty.json\")\n    with pytest.raises(ConfigKeyError):\n        config.red_key\n    os.remove(\"/tmp/empty.json\")\n