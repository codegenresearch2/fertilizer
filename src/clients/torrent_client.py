import os
from urllib.parse import urlparse, unquote

from src.utils import url_join
from src.filesystem import assert_path_exists, mkdir_p, list_files_of_extension, replace_extension

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
        """
        Extract credentials from the given URL and construct the base URL.

        Args:
            url (str): The URL to extract credentials from.
            base_path (str, optional): The base path to append to the URL. Defaults to None.

        Returns:
            tuple: A tuple containing the base URL, username, and password.
        """
        parsed_url = urlparse(url)
        username = unquote(parsed_url.username) if parsed_url.username else ""
        password = unquote(parsed_url.password) if parsed_url.password else ""
        origin = f"{parsed_url.scheme}://{parsed_url.hostname}:{parsed_url.port}"

        if base_path is not None:
            href = url_join(origin, os.path.normpath(base_path))
        else:
            href = url_join(origin, parsed_url.path if parsed_url.path != "/" else "")

        return href, username, password

    def _determine_label(self, torrent_info):
        """
        Determine the label for the torrent based on the current label.

        Args:
            torrent_info (dict): Information about the torrent.

        Returns:
            str: The determined label for the torrent.
        """
        current_label = torrent_info.get("label")

        if not current_label:
            return self.torrent_label

        if current_label == self.torrent_label or current_label.endswith(f".{self.torrent_label}"):
            return current_label

        return f"{current_label}.{self.torrent_label}"

# Adding new tests
def test_extract_credentials_from_url():
    client = TorrentClient()
    url = "http://username:password@example.com:8080/api/v2"
    assert client._extract_credentials_from_url(url) == ("http://example.com:8080/api/v2", "username", "password")

def test_determine_label():
    client = TorrentClient()
    assert client._determine_label({"label": "test"}) == "test.fertilizer"
    assert client._determine_label({"label": "test.fertilizer"}) == "test.fertilizer"
    assert client._determine_label({"label": "fertilizer"}) == "fertilizer"
    assert client._determine_label({"label": ""}) == "fertilizer"