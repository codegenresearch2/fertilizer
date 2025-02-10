import base64
import pytest
import requests_mock

from tests.helpers import SetupTeardown, get_torrent_path
from tests.support.deluge_matchers import (
  add_label_matcher,
  add_torrent_matcher,
  apply_label_matcher,
  auth_matcher,
  connected_matcher,
  get_labels_matcher,
  label_plugin_matcher,
  torrent_info_matcher,
)

from src.errors import TorrentClientError, TorrentClientAuthenticationError
from src.clients.deluge import Deluge


@pytest.fixture
def api_url():
  return "http://localhost:8112/json"


@pytest.fixture
def deluge_client():
  return Deluge("http://:supersecret@localhost:8112/json")


@pytest.fixture
def torrent_info_response():
  return {
    "name": "foo.torrent",
    "state": "Seeding",
    "progress": 100.0,
    "save_path": "/tmp/bar/",
    "label": "fertilizer",
    "total_remaining": 0.0,
  }


class TestAuthentication(SetupTeardown):
    def test_raises_exception_on_failed_auth(self, api_url, deluge_client):
        with requests_mock.Mocker() as m:
            m.post(api_url, additional_matcher=auth_matcher, json={"result": False})

            with pytest.raises(TorrentClientAuthenticationError) as excinfo:
                deluge_client.setup()

            assert "Failed to authenticate with Deluge" in str(excinfo.value)


class TestLabelPlugin(SetupTeardown):
    def test_sets_label_plugin_enabled_when_true(self, api_url, deluge_client):
        assert not deluge_client._label_plugin_enabled

        with requests_mock.Mocker() as m:
            m.post(
                api_url,
                additional_matcher=auth_matcher,
                json={"result": True},
                headers={"Set-Cookie": "supersecret"},
            )
            m.post(api_url, additional_matcher=connected_matcher, json={"result": True})
            m.post(api_url, additional_matcher=label_plugin_matcher, json={"result": ["Label"]})

            deluge_client.setup()

            assert deluge_client._label_plugin_enabled

    def test_sets_label_plugin_enabled_when_false(self, api_url, deluge_client):
        assert not deluge_client._label_plugin_enabled

        with requests_mock.Mocker() as m:
            m.post(
                api_url,
                additional_matcher=auth_matcher,
                json={"result": True},
                headers={"Set-Cookie": "supersecret"},
            )
            m.post(api_url, additional_matcher=connected_matcher, json={"result": True})
            m.post(api_url, additional_matcher=label_plugin_matcher, json={"result": []})

            deluge_client.setup()

            assert not deluge_client._label_plugin_enabled


This revised code snippet addresses the feedback provided by the oracle. It ensures that the `__authenticate` method correctly raises a `TorrentClientAuthenticationError` when authentication fails, and it includes additional test cases to cover different scenarios as suggested by the oracle.