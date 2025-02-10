import os
from urllib.parse import urlparse, unquote

from src.filesystem import sane_join
from src.utils import url_join

class TorrentClient:
    def __init__(self):
        self.torrent_label = "fertilizer"

    def setup(self):
        raise NotImplementedError

    def get_torrent_info(self, *_args, **_kwargs):
        raise NotImplementedError

    def inject_torrent(self, *_args, **_kwargs):
        raise NotImplementedError

    def _extract_credentials_from_url(self, url, base_path=None):
        parsed_url = urlparse(url)
        username = unquote(parsed_url.username) if parsed_url.username else ""
        password = unquote(parsed_url.password) if parsed_url.password else ""
        origin = f"{parsed_url.scheme}://{parsed_url.hostname}:{parsed_url.port}"

        if base_path is not None:
            href = url_join(origin, os.path.normpath(base_path))
        else:
            href = url_join(origin, (parsed_url.path if parsed_url.path != "/" else ""))

        return href, username, password

    def _determine_label(self, torrent_info):
        current_label = torrent_info.get("label")

        if not current_label:
            return self.torrent_label

        if current_label == self.torrent_label or current_label.endswith(f".{self.torrent_label}"):
            return current_label

        return f"{current_label}.{self.torrent_label}"

# Adding a test class for functionality
class TestTorrentClient(unittest.TestCase):
    def setUp(self):
        self.client = TorrentClient()

    def test_extract_credentials_from_url(self):
        url = "http://username:password@example.com:8080/api/v2"
        expected_output = ("http://example.com:8080/api/v2", "username", "password")
        self.assertEqual(self.client._extract_credentials_from_url(url), expected_output)

    def test_determine_label(self):
        torrent_info = {"label": "test"}
        expected_output = "test.fertilizer"
        self.assertEqual(self.client._determine_label(torrent_info), expected_output)