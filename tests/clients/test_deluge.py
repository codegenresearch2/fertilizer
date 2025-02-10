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

ERROR_CODES = {
  "NO_AUTH": 1,
}

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

class TestSetup(SetupTeardown):
  def test_successful_authentication(self, api_url, deluge_client):
    assert deluge_client._deluge_cookie is None

    with requests_mock.Mocker() as m:
      m.post(
        api_url,
        additional_matcher=auth_matcher,
        json={"result": True},
        headers={"Set-Cookie": "supersecret"},
      )
      m.post(api_url, additional_matcher=connected_matcher, json={"result": True})
      m.post(api_url, additional_matcher=label_plugin_matcher, json={"result": ["Label"]})

      response = deluge_client.setup()

      assert response
      assert deluge_client._deluge_cookie is not None

  def test_failed_authentication(self, api_url, deluge_client):
    with requests_mock.Mocker() as m:
      m.post(api_url, additional_matcher=auth_matcher, json={"result": False})

      with pytest.raises(TorrentClientError) as excinfo:
        deluge_client.setup()

      assert "Reached Deluge RPC endpoint but failed to authenticate" in str(excinfo.value)

  def test_authentication_error_code(self, api_url, deluge_client):
    with requests_mock.Mocker() as m:
      m.post(
        api_url,
        additional_matcher=auth_matcher,
        json={"error": {"code": ERROR_CODES["NO_AUTH"]}},
      )

      with pytest.raises(TorrentClientAuthenticationError) as excinfo:
        deluge_client.setup()

      assert "Failed to authenticate with Deluge" in str(excinfo.value)

class TestGetTorrentInfo(SetupTeardown):
  def test_returns_torrent_details(self, api_url, deluge_client, torrent_info_response):
    with requests_mock.Mocker() as m:
      m.post(
        api_url,
        additional_matcher=torrent_info_matcher,
        json={
          "result": {
            "torrents": {"foo": torrent_info_response},
          },
        },
      )

      response = deluge_client.get_torrent_info("foo")

      assert response == {
        "complete": True,
        "label": "fertilizer",
        "save_path": "/tmp/bar/",
      }

  def test_authentication_error_code(self, api_url, deluge_client):
    with requests_mock.Mocker() as m:
      m.post(
        api_url,
        additional_matcher=torrent_info_matcher,
        json={"error": {"code": ERROR_CODES["NO_AUTH"]}},
      )

      with pytest.raises(TorrentClientAuthenticationError) as excinfo:
        deluge_client.get_torrent_info("foo")

      assert "Failed to authenticate with Deluge" in str(excinfo.value)

class TestInjectTorrent(SetupTeardown):
  def test_injects_torrent(self, api_url, deluge_client, torrent_info_response):
    torrent_path = get_torrent_path("red_source")

    with requests_mock.Mocker() as m:
      m.post(
        api_url,
        additional_matcher=torrent_info_matcher,
        json={
          "result": {
            "torrents": {"foo": torrent_info_response},
          },
        },
      )

      m.post(
        api_url,
        additional_matcher=add_torrent_matcher,
        json={"result": "abc123"},
      )

      response = deluge_client.inject_torrent("foo", torrent_path)
      request_params = m.request_history[1].json()["params"]

      assert response == "abc123"
      assert request_params[0] == "red_source.fertilizer.torrent"
      assert request_params[1] == base64.b64encode(open(torrent_path, "rb").read()).decode()
      assert request_params[2] == {"download_location": "/tmp/bar/", "seed_mode": True, "add_paused": False}

  def test_reauthenticates_on_auth_error_code(self, api_url, deluge_client, torrent_info_response):
    torrent_path = get_torrent_path("red_source")

    with requests_mock.Mocker() as m:
      m.post(
        api_url,
        additional_matcher=torrent_info_matcher,
        json={
          "result": {
            "torrents": {"foo": torrent_info_response},
          },
        },
      )

      m.post(
        api_url,
        additional_matcher=add_torrent_matcher,
        json={"error": {"code": ERROR_CODES["NO_AUTH"]}},
      )

      m.post(
        api_url,
        additional_matcher=auth_matcher,
        json={"result": True},
        headers={"Set-Cookie": "newsecret"},
      )

      m.post(
        api_url,
        additional_matcher=add_torrent_matcher,
        json={"result": "abc123"},
      )

      response = deluge_client.inject_torrent("foo", torrent_path)

      assert response == "abc123"
      assert deluge_client._deluge_cookie == "newsecret"

I have addressed the feedback received from the oracle.

In the `TestSetup` class, I have added a test case for successful authentication and a test case for failed authentication. I have also added a test case for handling authentication errors with error codes.

In the `TestGetTorrentInfo` class, I have added a test case for handling authentication errors with error codes.

In the `TestInjectTorrent` class, I have added a test case for re-authentication if the cookie has expired.

I have also updated the test method names to be more descriptive and ensured that the assertions are consistent with the expected outcomes.

Additionally, I have removed the invalid comment that was causing the syntax error.