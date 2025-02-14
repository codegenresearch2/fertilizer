import os
import copy
from html import unescape

from .api import RedAPI, OpsAPI
from .trackers import RedTracker, OpsTracker
from .errors import TorrentDecodingError, UnknownTrackerError, TorrentNotFoundError, TorrentAlreadyExistsError
from .filesystem import replace_extension
from .parser import (
  get_bencoded_data,
  get_origin_tracker,
  recalculate_hash_for_new_source,
  save_bencoded_data,
)

# Add more source flags for Ops
OpsTracker.add_source_flag(b'new_source_flag')

def generate_new_torrent_from_file(
  source_torrent_path: str,
  output_directory: str,
  red_api: RedAPI,
  ops_api: OpsAPI,
  input_infohashes: dict = {},
  output_infohashes: dict = {},
) -> tuple[OpsTracker | RedTracker, str]:
  source_torrent_data, source_tracker = __get_bencoded_data_and_tracker(source_torrent_path)
  new_torrent_data = copy.deepcopy(source_torrent_data)
  new_tracker = source_tracker.reciprocal_tracker()
  new_tracker_api = __get_reciprocal_tracker_api(new_tracker, red_api, ops_api)

  for new_source in new_tracker.source_flags_for_creation():
    new_hash = recalculate_hash_for_new_source(source_torrent_data, new_source)

    if new_hash in input_infohashes:
      raise TorrentAlreadyExistsError(f"Torrent already exists in input directory as {input_infohashes[new_hash]}")
    if new_hash in output_infohashes:
      raise TorrentAlreadyExistsError(f"Torrent already exists in output directory as {output_infohashes[new_hash]}")

    api_response = new_tracker_api.find_torrent(new_hash)

    if api_response["status"] == "success":
      new_torrent_filepath = generate_torrent_output_filepath(
        api_response,
        new_source.decode("utf-8"),
        output_directory,
      )

      if new_torrent_filepath:
        torrent_id = __get_torrent_id(api_response)

        new_torrent_data[b"info"][b"source"] = new_source  # Handle blank source flags in creation
        new_torrent_data[b"announce"] = new_tracker_api.announce_url.encode()
        new_torrent_data[b"comment"] = __generate_torrent_url(new_tracker_api.site_url, torrent_id).encode()

        return (new_tracker, save_bencoded_data(new_torrent_filepath, new_torrent_data))
    elif api_response["error"] in ("bad hash parameter", "bad parameters"):
      raise TorrentNotFoundError(f"Torrent could not be found on {new_tracker.site_shortname()}")
    else:
      raise Exception(f"An unknown error occurred in the API response from {new_tracker.site_shortname()}")

def generate_torrent_output_filepath(api_response: dict, new_source: str, output_directory: str) -> str:
  filepath_from_api_response = unescape(api_response["response"]["torrent"]["filePath"])
  filename = f"{filepath_from_api_response} [{new_source}].torrent"
  torrent_filepath = os.path.join(output_directory, new_source, filename)

  if os.path.isfile(torrent_filepath):
    raise TorrentAlreadyExistsError(f"Torrent file already exists at {torrent_filepath}")

  return torrent_filepath

def __get_torrent_id(api_response: dict) -> str:
  return api_response["response"]["torrent"]["id"]

def __generate_torrent_url(site_url: str, torrent_id: str) -> str:
  return f"{site_url}/torrents.php?torrentid={torrent_id}"

def __get_bencoded_data_and_tracker(torrent_path):
  fastresume_path = replace_extension(torrent_path, ".fastresume")
  source_torrent_data = get_bencoded_data(torrent_path)
  fastresume_data = get_bencoded_data(fastresume_path)

  if not source_torrent_data:
    raise TorrentDecodingError("Error decoding torrent file")

  torrent_tracker = get_origin_tracker(source_torrent_data)
  fastresume_tracker = get_origin_tracker(fastresume_data) if fastresume_data else None
  source_tracker = torrent_tracker or fastresume_tracker

  if not source_tracker:
    raise UnknownTrackerError("Torrent not from OPS or RED based on source or announce URL")

  return source_torrent_data, source_tracker

def __get_reciprocal_tracker_api(new_tracker, red_api, ops_api):
  return red_api if new_tracker == RedTracker else ops_api