import os
from urllib.parse import urlparse, unquote
import unittest

from src.utils import url_join

class TorrentClient:
    def __init__(self):
        self.torrent_label = "fertilizer"

    def setup(self):
        """
        Setup method to be implemented by subclasses.
        """
        raise NotImplementedError

    def get_torrent_info(self, *_args, **_kwargs):
        """
        Method to get torrent information to be implemented by subclasses.
        """
        raise NotImplementedError

    def inject_torrent(self, *_args, **_kwargs):
        """
        Method to inject a torrent to be implemented by subclasses.
        """
        raise NotImplementedError

    def _extract_credentials_from_url(self, url, base_path=None):
        """
        Extract credentials from a given URL.

        Args:
            url (str): The URL to extract credentials from.
            base_path (str, optional): The base path to append to the URL. Defaults to None.

        Returns:
            tuple: A tuple containing the URL, username, and password.
        """
        parsed_url = urlparse(url)
        username = unquote(parsed_url.username) if parsed_url.username else ""
        password = unquote(parsed_url.password) if parsed_url.password else ""
        origin = f"{parsed_url.scheme}://{parsed_url.hostname}:{parsed_url.port}"

        if base_path is not None:
            href = url_join(origin, os.path.normpath(base_path))
        else:
            href = url_join(origin, parsed_url.path)

        return href, username, password

    def _determine_label(self, torrent_info):
        """
        Determine the label for a given torrent information.

        Args:
            torrent_info (dict): The torrent information.

        Returns:
            str: The determined label.
        """
        current_label = torrent_info.get("label")

        if not current_label:
            return self.torrent_label

        if current_label == self.torrent_label or current_label.endswith(f".{self.torrent_label}"):
            return current_label

        return f"{current_label}.{self.torrent_label}"

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