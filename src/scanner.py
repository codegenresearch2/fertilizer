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
        `source_torrent_path` (`str`): The path to the .torrent file.
        `output_directory` (`str`): The directory to save the new .torrent files.
        `red_api` (`RedAPI`): The pre-configured RED tracker API.
        `ops_api` (`OpsAPI`): The pre-configured OPS tracker API.
        `injector` (`Injection`): The pre-configured torrent Injection object.
    Returns:
        str: The path to the new .torrent file.
    Raises:
        FileNotFoundError: if the input directory does not exist.
        TorrentDecodingError: if the torrent file cannot be decoded.
        UnknownTrackerError: if the tracker is unknown.
        TorrentNotFoundError: if the torrent cannot be found.
        TorrentAlreadyExistsError: if the torrent already exists.
        Exception: for any other unknown errors.
    """
    try:
        source_torrent_path = assert_path_exists(source_torrent_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Input directory not found: {e}")

    output_directory = mkdir_p(output_directory)

    output_torrents = list_files_of_extension(output_directory, ".torrent")
    output_infohashes = __collect_infohashes_from_files(output_torrents)

    try:
        new_tracker, new_torrent_filepath = generate_new_torrent_from_file(
            source_torrent_path,
            output_directory,
            red_api,
            ops_api,
            input_infohashes={},
            output_infohashes=output_infohashes,
        )
    except TorrentDecodingError:
        raise TorrentDecodingError("Error decoding torrent file.")
    except UnknownTrackerError:
        raise UnknownTrackerError("Unknown tracker error.")
    except TorrentNotFoundError:
        raise TorrentNotFoundError("Torrent not found.")
    except TorrentAlreadyExistsError:
        raise TorrentAlreadyExistsError("Torrent already exists.")
    except Exception as e:
        raise Exception(f"An unknown error occurred: {e}")

    if injector:
        try:
            injector.inject_torrent(
                source_torrent_path,
                new_torrent_filepath,
                new_tracker.site_shortname(),
            )
        except Exception as e:
            raise Exception(f"Injection error: {e}")

    return new_torrent_filepath


def scan_torrent_directory(
    input_directory: str,
    output_directory: str,
    red_api: RedAPI,
    ops_api: OpsAPI,
    injector: Injection | None,
) -> str:
    """
    Scans a directory for .torrent files and generates new ones using the tracker APIs.

    Args:
        `input_directory` (`str`): The directory containing the .torrent files.
        `output_directory` (`str`): The directory to save the new .torrent files.
        `red_api` (`RedAPI`): The pre-configured RED tracker API.
        `ops_api` (`OpsAPI`): The pre-configured OPS tracker API.
        `injector` (`Injection`): The pre-configured torrent Injection object.
    Returns:
        str: A report of the scan.
    Raises:
        FileNotFoundError: if the input directory does not exist.
    """
    try:
        input_directory = assert_path_exists(input_directory)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Input directory not found: {e}")

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
            new_tracker, new_torrent_filepath = generate_new_torrent_from_file(
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

            if new_torrent_filepath:
                print(
                    f"Found with source '{new_tracker.site_shortname()}' and generated as '{new_torrent_filepath}'."
                )
        except TorrentDecodingError as e:
            print(str(e))
            p.error.print(str(e))
            continue
        except UnknownTrackerError as e:
            print(str(e))
            p.skipped.print(str(e))
            continue
        except TorrentAlreadyExistsError as e:
            print(str(e))
            p.already_exists.print(str(e))
            continue
        except TorrentExistsInClientError as e:
            print(str(e))
            p.already_exists.print(str(e))
            continue
        except TorrentNotFoundError as e:
            print(str(e))
            p.not_found.print(str(e))
            continue
        except Exception as e:
            print(str(e))
            p.error.print(str(e))
            continue

    return p.report()


def __collect_infohashes_from_files(files: list[str]) -> dict:
    infohash_dict = {}

    for filepath in files:
        try:
            torrent_data = get_bencoded_data(filepath)

            if torrent_data and 'info' in torrent_data:
                infohash = calculate_infohash(torrent_data)
                infohash_dict[infohash] = filepath
        except Exception:
            continue

    return infohash_dict