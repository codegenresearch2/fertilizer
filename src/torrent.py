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


def generate_new_torrent_from_file(
  source_torrent_path: str,
  output_directory: str,
  red_api: RedAPI,
  ops_api: OpsAPI,
  input_infohashes: dict = {},
  output_infohashes: dict = {},
) -> tuple[OpsTracker | RedTracker, str]:
  """\n  Generates a new torrent file for the reciprocal tracker of the original torrent file if it exists on the reciprocal tracker.\n\n  Args:\n    `source_torrent_path` (`str`): The path to the original torrent file.\n    `output_directory` (`str`): The directory to save the new torrent file.\n    `red_api` (`RedApi`): The pre-configured API object for RED.\n    `ops_api` (`OpsApi`): The pre-configured API object for OPS.\n    `input_infohashes` (`dict`, optional): A dictionary of infohashes and their filenames from the input directory for caching purposes. Defaults to an empty dictionary.\n    `output_infohashes` (`dict`, optional): A dictionary of infohashes and their filenames from the output directory for caching purposes. Defaults to an empty dictionary.\n  Returns:\n    A tuple containing the new tracker class (`RedTracker` or `OpsTracker`) and the path to the new torrent file.\n  Raises:\n    `TorrentDecodingError`: if the original torrent file could not be decoded.\n    `UnknownTrackerError`: if the original torrent file is not from OPS or RED.\n    `TorrentNotFoundError`: if the original torrent file could not be found on the reciprocal tracker.\n    `TorrentAlreadyExistsError`: if the new torrent file already exists in the input or output directory.\n    `Exception`: if an unknown error occurs.\n  """

  source_torrent_data, source_tracker = __get_bencoded_data_and_tracker(source_torrent_path)
  new_torrent_data = copy.deepcopy(source_torrent_data)
  new_tracker = source_tracker.reciprocal_tracker()
  new_tracker_api = __get_reciprocal_tracker_api(new_tracker, red_api, ops_api)

  # Add more source flags for Ops
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

        new_torrent_data[b"info"][b"source"] = new_source  # This is already bytes rather than str
        new_torrent_data[b"announce"] = new_tracker_api.announce_url.encode()
        new_torrent_data[b"comment"] = __generate_torrent_url(new_tracker_api.site_url, torrent_id).encode()

        return (new_tracker, save_bencoded_data(new_torrent_filepath, new_torrent_data))
    elif api_response["error"] in ("bad hash parameter", "bad parameters"):
      raise TorrentNotFoundError(f"Torrent could not be found on {new_tracker.site_shortname()}")
    else:
      raise Exception(f"An unknown error occurred in the API response from {new_tracker.site_shortname()}")


def generate_torrent_output_filepath(api_response: dict, new_source: str, output_directory: str) -> str:
  """\n  Generates the output filepath for the new torrent file. Does not create the file.\n\n  Args:\n    `api_response` (`dict`): The response from the tracker API.\n    `new_source` (`str`): The source of the new torrent file (`"RED"` or `"OPS"`).\n    `output_directory` (`str`): The directory to save the new torrent file.\n  Returns:\n    The path to the new torrent file.\n  Raises:\n    `TorrentAlreadyExistsError`: if the new torrent file already exists in the output directory.\n  """

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
  # The fastresume stuff is to support qBittorrent since it doesn't store\n  # announce URLs in the torrent file IFF we're taking the file from `BT_backup`.
  #
  # qbit stores that information in a sidecar file that has the exact same name
  # as the torrent file but with a `.fastresume` extension instead. It's also stored\n  # in a list of lists called `trackers` in this `.fastresume` file instead of `announce`.\n  fastresume_path = replace_extension(torrent_path, ".fastresume")\n  source_torrent_data = get_bencoded_data(torrent_path)\n  fastresume_data = get_bencoded_data(fastresume_path)\n\n  if not source_torrent_data:\n    raise TorrentDecodingError("Error decoding torrent file")\n\n  torrent_tracker = get_origin_tracker(source_torrent_data)\n  fastresume_tracker = get_origin_tracker(fastresume_data) if fastresume_data else None\n  source_tracker = torrent_tracker or fastresume_tracker\n\n  if not source_tracker:\n    raise UnknownTrackerError("Torrent not from OPS or RED based on source or announce URL")\n\n  return source_torrent_data, source_tracker\n\n\ndef __get_reciprocal_tracker_api(new_tracker, red_api, ops_api):\n  return red_api if new_tracker == RedTracker else ops_api