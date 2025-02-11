import os

from .api import RedAPI, OpsAPI
from .filesystem import mkdir_p, list_files_of_extension, assert_path_exists
from .progress import Progress
from .torrent import generate_new_torrent_from_file
from .parser import get_bencoded_data, calculate_infohash
from .errors import (
  TorrentDecodingError,
  UnknownTrackerError,
  TorrentNotFoundError,
  TorrentAlreadyExistsError,
  TorrentExistsInClientError,
)
from .injection import Injection

def scan_torrent_file(
  source_torrent_path: str,
  output_directory: str,
  red_api: RedAPI,
  ops_api: OpsAPI,
  injector: Injection | None,
) -> str:
    """
    Scans a single .torrent file and generates a new one using the tracker API.

    Args:
        source_torrent_path (str): The path to the .torrent file.
        output_directory (str): The directory to save the new .torrent files.
        red_api (RedAPI): The pre-configured RED tracker API.
        ops_api (OpsAPI): The pre-configured OPS tracker API.
        injector (Injection): The pre-configured torrent Injection object.

    Returns:
        str: The path to the new .torrent file.

    Raises:
        See `generate_new_torrent_from_file`.
    """
    source_torrent_path = assert_path_exists(source_torrent_path)
    output_directory = mkdir_p(output_directory)

    output_torrents = list_files_of_extension(output_directory, ".torrent")
    output_infohashes = __collect_infohashes_from_files(output_torrents)

    p = Progress()

    try:
        new_tracker, new_torrent_filepath, _ = generate_new_torrent_from_file(
            source_torrent_path,
            output_directory,
            red_api,
            ops_api,
            input_infohashes={},
            output_infohashes=output_infohashes,
        )

        if injector:
            injector.inject_torrent(
                source_torrent_path,
                new_torrent_filepath,
                new_tracker.site_shortname(),
            )

        p.generated.print(f"Found with source '{new_tracker.site_shortname()}' and generated as '{new_torrent_filepath}'.")
        return new_torrent_filepath
    except (TorrentDecodingError, UnknownTrackerError, TorrentAlreadyExistsError, TorrentExistsInClientError, TorrentNotFoundError) as e:
        p.error.print(str(e))
    except Exception as e:
        p.error.print(f"An unknown error occurred: {e}")

def __collect_infohashes_from_files(files: list[str]) -> dict:
    """
    Collects infohashes from a list of .torrent files.

    Args:
        files (list[str]): A list of file paths to .torrent files.

    Returns:
        dict: A dictionary mapping infohashes to file paths.
    """
    infohash_dict = {}

    for filepath in files:
        try:
            torrent_data = get_bencoded_data(filepath)

            if torrent_data:
                infohash = calculate_infohash(torrent_data)
                infohash_dict[infohash] = filepath
        except UnicodeDecodeError:
            continue

    return infohash_dict

I have addressed the feedback by improving the docstring formatting, simplifying the exception handling, and adding a progress reporting mechanism. I have also made sure to handle similar exceptions in a more concise manner.