import os
import copy
import bencoder
from hashlib import sha1

from .utils import flatten
from .trackers import RedTracker, OpsTracker
from .errors import TorrentDecodingError

def is_valid_infohash(infohash: str) -> bool:
  if not isinstance(infohash, str) or len(infohash) != 40:
    return False
  try:
    return bool(int(infohash, 16))
  except ValueError:
    return False

def get_source(torrent_data: dict) -> bytes | None:
  try:
    return torrent_data[b"info"][b"source"]
  except KeyError:
    return None

def get_name(torrent_data: dict) -> bytes | None:
  try:
    return torrent_data[b"info"][b"name"]
  except KeyError:
    return None

def get_announce_url(torrent_data: dict) -> list[bytes] | None:
  from_announce = torrent_data.get(b"announce")
  if from_announce:
    return from_announce if isinstance(from_announce, list) else [from_announce]

  from_trackers = torrent_data.get(b"trackers")
  if from_trackers:
    return flatten(from_trackers)

  return None

def get_origin_tracker(torrent_data: dict) -> RedTracker | OpsTracker | None:
  source = get_source(torrent_data) or b""
  announce_url = get_announce_url(torrent_data) or []

  if source in RedTracker.source_flags_for_search() or any(RedTracker.announce_url() in url for url in announce_url):
    return RedTracker

  if source in OpsTracker.source_flags_for_search() or any(OpsTracker.announce_url() in url for url in announce_url):
    return OpsTracker

  return None

def calculate_infohash(torrent_data: dict) -> str:
  if b"info" not in torrent_data:
    raise TorrentDecodingError("Torrent data does not contain 'info' key")
  return sha1(bencoder.encode(torrent_data[b"info"])).hexdigest().upper()

def recalculate_hash_for_new_source(torrent_data: dict, new_source: (bytes | str)) -> str:
  torrent_data = copy.deepcopy(torrent_data)
  torrent_data[b"info"][b"source"] = new_source

  return calculate_infohash(torrent_data)

def get_bencoded_data(filename: str) -> dict:
  try:
    with open(filename, "rb") as f:
      data = bencoder.decode(f.read())
    return data
  except Exception:
    return None

def save_bencoded_data(filepath: str, torrent_data: dict) -> str:
  parent_dir = os.path.dirname(filepath)
  if parent_dir:
    os.makedirs(parent_dir, exist_ok=True)

  with open(filepath, "wb") as f:
    f.write(bencoder.encode(torrent_data))

  return filepath

I have made the following changes to address the feedback:

1. **Error Handling**: In the `calculate_infohash` function, I have modified the exception raised when the 'info' key is missing to be `TorrentDecodingError` instead of `ValueError`.

2. **Redundant Imports**: I have removed the `shutil` import since it is not used in the code.

3. **Parent Directory Creation**: In the `save_bencoded_data` function, I have ensured that the parent directory is created if it does not exist.

4. **Return Values**: In the `save_bencoded_data` function, I have directly returned the `filepath` after writing the data, rather than calling `copy_and_mkdir`.

5. **Exception Handling in `get_bencoded_data`**: I have removed the print statement when an exception occurs and simply returned `None` for a cleaner error handling strategy.

Here is the updated code:


import os
import copy
import bencoder
from hashlib import sha1

from .utils import flatten
from .trackers import RedTracker, OpsTracker
from .errors import TorrentDecodingError

def is_valid_infohash(infohash: str) -> bool:
  if not isinstance(infohash, str) or len(infohash) != 40:
    return False
  try:
    return bool(int(infohash, 16))
  except ValueError:
    return False

def get_source(torrent_data: dict) -> bytes | None:
  try:
    return torrent_data[b"info"][b"source"]
  except KeyError:
    return None

def get_name(torrent_data: dict) -> bytes | None:
  try:
    return torrent_data[b"info"][b"name"]
  except KeyError:
    return None

def get_announce_url(torrent_data: dict) -> list[bytes] | None:
  from_announce = torrent_data.get(b"announce")
  if from_announce:
    return from_announce if isinstance(from_announce, list) else [from_announce]

  from_trackers = torrent_data.get(b"trackers")
  if from_trackers:
    return flatten(from_trackers)

  return None

def get_origin_tracker(torrent_data: dict) -> RedTracker | OpsTracker | None:
  source = get_source(torrent_data) or b""
  announce_url = get_announce_url(torrent_data) or []

  if source in RedTracker.source_flags_for_search() or any(RedTracker.announce_url() in url for url in announce_url):
    return RedTracker

  if source in OpsTracker.source_flags_for_search() or any(OpsTracker.announce_url() in url for url in announce_url):
    return OpsTracker

  return None

def calculate_infohash(torrent_data: dict) -> str:
  if b"info" not in torrent_data:
    raise TorrentDecodingError("Torrent data does not contain 'info' key")
  return sha1(bencoder.encode(torrent_data[b"info"])).hexdigest().upper()

def recalculate_hash_for_new_source(torrent_data: dict, new_source: (bytes | str)) -> str:
  torrent_data = copy.deepcopy(torrent_data)
  torrent_data[b"info"][b"source"] = new_source

  return calculate_infohash(torrent_data)

def get_bencoded_data(filename: str) -> dict:
  try:
    with open(filename, "rb") as f:
      data = bencoder.decode(f.read())
    return data
  except Exception:
    return None

def save_bencoded_data(filepath: str, torrent_data: dict) -> str:
  parent_dir = os.path.dirname(filepath)
  if parent_dir:
    os.makedirs(parent_dir, exist_ok=True)

  with open(filepath, "wb") as f:
    f.write(bencoder.encode(torrent_data))

  return filepath