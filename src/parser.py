import os
import copy
import bencoder
from hashlib import sha1

from .utils import flatten
from .trackers import RedTracker, OpsTracker
from .errors import TorrentDecodingError

def is_valid_infohash(infohash: str) -> bool:
    """
    Check if the given infohash is valid.

    Args:
        infohash (str): The infohash to validate.

    Returns:
        bool: True if the infohash is valid, False otherwise.
    """
    if not isinstance(infohash, str) or len(infohash) != 40:
        return False
    try:
        return bool(int(infohash, 16))
    except ValueError:
        return False

def get_source(torrent_data: dict) -> bytes | None:
    """
    Get the source from the torrent data.

    Args:
        torrent_data (dict): The torrent data.

    Returns:
        bytes | None: The source if present, None otherwise.
    """
    try:
        return torrent_data[b"info"][b"source"]
    except KeyError:
        return None

def get_name(torrent_data: dict) -> bytes | None:
    """
    Get the name from the torrent data.

    Args:
        torrent_data (dict): The torrent data.

    Returns:
        bytes | None: The name if present, None otherwise.
    """
    try:
        return torrent_data[b"info"][b"name"]
    except KeyError:
        return None

def get_announce_url(torrent_data: dict) -> list[bytes] | None:
    """
    Get the announce URL from the torrent data.

    Args:
        torrent_data (dict): The torrent data.

    Returns:
        list[bytes] | None: The announce URL if present, None otherwise.
    """
    from_announce = torrent_data.get(b"announce")
    if from_announce:
        return from_announce if isinstance(from_announce, list) else [from_announce]

    from_trackers = torrent_data.get(b"trackers")
    if from_trackers:
        return flatten(from_trackers)

    return None

def get_origin_tracker(torrent_data: dict) -> RedTracker | OpsTracker | None:
    """
    Get the origin tracker from the torrent data.

    Args:
        torrent_data (dict): The torrent data.

    Returns:
        RedTracker | OpsTracker | None: The origin tracker if present, None otherwise.
    """
    source = get_source(torrent_data) or b""
    announce_url = get_announce_url(torrent_data) or []

    if source in RedTracker.source_flags_for_search() or any(RedTracker.announce_url() in url for url in announce_url):
        return RedTracker

    if source in OpsTracker.source_flags_for_search() or any(OpsTracker.announce_url() in url for url in announce_url):
        return OpsTracker

    return None

def calculate_infohash(torrent_data: dict) -> str:
    """
    Calculate the infohash from the torrent data.

    Args:
        torrent_data (dict): The torrent data.

    Returns:
        str: The calculated infohash.

    Raises:
        TorrentDecodingError: If the torrent data does not contain the 'info' key.
    """
    try:
        return sha1(bencoder.encode(torrent_data[b"info"])).hexdigest().upper()
    except KeyError:
        raise TorrentDecodingError("Torrent data does not contain 'info' key")

def recalculate_hash_for_new_source(torrent_data: dict, new_source: (bytes | str)) -> str:
    """
    Recalculate the hash for a new source in the torrent data.

    Args:
        torrent_data (dict): The torrent data.
        new_source (bytes | str): The new source.

    Returns:
        str: The recalculated hash.
    """
    torrent_data = copy.deepcopy(torrent_data)
    torrent_data[b"info"][b"source"] = new_source

    return calculate_infohash(torrent_data)

def get_bencoded_data(filename: str) -> dict:
    """
    Get the bencoded data from a file.

    Args:
        filename (str): The path to the file.

    Returns:
        dict: The bencoded data if successful, None otherwise.
    """
    try:
        with open(filename, "rb") as f:
            data = bencoder.decode(f.read())
        return data
    except Exception:
        return None

def save_bencoded_data(filepath: str, torrent_data: dict) -> str:
    """
    Save the bencoded data to a file.

    Args:
        filepath (str): The path to the file.
        torrent_data (dict): The torrent data.

    Returns:
        str: The filepath.
    """
    parent_dir = os.path.dirname(filepath)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(filepath, "wb") as f:
        f.write(bencoder.encode(torrent_data))

    return filepath