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
  source_torrent_path = assert_path_exists(source_torrent_path)
  output_directory = mkdir_p(output_directory)

  output_torrents = list_files_of_extension(output_directory, ".torrent")
  output_infohashes = __collect_infohashes_from_files(output_torrents)

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

    return new_torrent_filepath
  except Exception as e:
    raise e

def scan_torrent_directory(
  input_directory: str,
  output_directory: str,
  red_api: RedAPI,
  ops_api: OpsAPI,
  injector: Injection | None,
) -> str:
  input_directory = assert_path_exists(input_directory)
  output_directory = mkdir_p(output_directory)

  input_torrents = list_files_of_extension(input_directory, ".torrent")
  output_torrents = list_files_of_extension(output_directory, ".torrent")
  input_infohashes = __collect_infohashes_from_files(input_torrents)
  output_infohashes = __collect_infohashes_from_files(output_torrents)

  p = Progress(len(input_torrents))

  for i, source_torrent_path in enumerate(input_torrents, 1):
    basename = os.path.basename(source_torrent_path)
    print(f"({i}/{p.total}) {basename}")

    try:
      new_tracker, new_torrent_filepath, was_previously_generated = generate_new_torrent_from_file(
        source_torrent_path,
        output_directory,
        red_api,
        ops_api,
        input_infohashes,
        output_infohashes,
      )

      if injector:
        injector.inject_torrent(
          source_torrent_path,
          new_torrent_filepath,
          new_tracker.site_shortname(),
        )

      if was_previously_generated:
        if injector:
          p.already_exists.print("Torrent was previously generated but was injected into your torrent client.")
        else:
          p.already_exists.print("Torrent was previously generated.")
      else:
        p.generated.print(
          f"Found with source '{new_tracker.site_shortname()}' and generated as '{new_torrent_filepath}'."
        )
    except TorrentDecodingError as e:
      p.error.print(f"Decoding error: {str(e)}")
    except UnknownTrackerError as e:
      p.skipped.print(f"Unknown tracker error: {str(e)}")
    except TorrentAlreadyExistsError as e:
      p.already_exists.print(f"Torrent already exists: {str(e)}")
    except TorrentExistsInClientError as e:
      p.already_exists.print(f"Torrent exists in client: {str(e)}")
    except TorrentNotFoundError as e:
      p.not_found.print(f"Torrent not found: {str(e)}")
    except Exception as e:
      p.error.print(f"Unknown error: {str(e)}")

  return p.report()

def __collect_infohashes_from_files(files: list[str]) -> dict:
  infohash_dict = {}

  for filepath in files:
    try:
      torrent_data = get_bencoded_data(filepath)

      if torrent_data and b'info' in torrent_data:
        infohash = calculate_infohash(torrent_data)
        infohash_dict[infohash] = filepath
    except Exception as e:
      print(f"Error processing file {filepath}: {str(e)}")

  return infohash_dict


In the rewritten code, I have added error handling for missing 'info' key in the torrent data. I have also improved the error handling in torrent processing by providing more specific error messages. I have also maintained clean and organized test cases by separating the error handling logic from the main flow of the code.