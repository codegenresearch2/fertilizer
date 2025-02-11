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
    injector: Injection | None = None,
) -> str:
    """
    Scans a single .torrent file and generates a new one using the tracker API.

    Args:
        source_torrent_path (str): The path to the .torrent file.
        output_directory (str): The directory to save the new .torrent files.
        red_api (RedAPI): The pre-configured RED tracker API.
        ops_api (OpsAPI): The pre-configured OPS tracker API.
        injector (Injection | None): The pre-configured torrent Injection object. Defaults to None.

    Returns:
        str: The path to the new .torrent file.
    Raises:
        TorrentDecodingError: if the original torrent file could not be decoded.
        UnknownTrackerError: if the original torrent file is not from OPS or RED.
        TorrentNotFoundError: if the original torrent file could not be found on the reciprocal tracker.
        TorrentAlreadyExistsError: if the new torrent file already exists in the input or output directory.
        TorrentExistsInClientError: if the torrent already exists in the client.
        Exception: if an unknown error occurs.
    """
    source_torrent_path = assert_path_exists(source_torrent_path)
    output_directory = mkdir_p(output_directory)

    output_torrents = list_files_of_extension(output_directory, ".torrent")
    output_infohashes = __collect_infohashes_from_files(output_torrents)

    try:
        new_tracker, new_torrent_filepath, was_previously_generated = generate_new_torrent_from_file(
            source_torrent_path,
            output_directory,
            red_api,
            ops_api,
            input_infohashes={},
            output_infohashes=output_infohashes,
        )

        if injector and new_torrent_filepath:
            injector.inject_torrent(
                source_torrent_path,
                new_torrent_filepath,
                new_tracker.site_shortname(),
            )

        return new_torrent_filepath
    except TorrentDecodingError as e:
        raise TorrentDecodingError(str(e)) from e
    except UnknownTrackerError as e:
        raise UnknownTrackerError(str(e)) from e
    except TorrentNotFoundError as e:
        raise TorrentNotFoundError(str(e)) from e
    except TorrentAlreadyExistsError as e:
        raise TorrentAlreadyExistsError(str(e)) from e
    except TorrentExistsInClientError as e:
        raise TorrentExistsInClientError(str(e)) from e
    except Exception as e:
        raise Exception(str(e)) from e


def scan_torrent_directory(
    input_directory: str,
    output_directory: str,
    red_api: RedAPI,
    ops_api: OpsAPI,
    injector: Injection | None = None,
) -> str:
    """
    Scans a directory for .torrent files and generates new ones using the tracker APIs.

    Args:
        input_directory (str): The directory containing the .torrent files.
        output_directory (str): The directory to save the new .torrent files.
        red_api (RedAPI): The pre-configured RED tracker API.
        ops_api (OpsAPI): The pre-configured OPS tracker API.
        injector (Injection | None): The pre-configured torrent Injection object. Defaults to None.

    Returns:
        str: A report of the scan.
    Raises:
        FileNotFoundError: if the input directory does not exist.
    """
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
            _, new_torrent_filepath, was_previously_generated = generate_new_torrent_from_file(
                source_torrent_path,
                output_directory,
                red_api,
                ops_api,
                input_infohashes=input_infohashes,
                output_infohashes=output_infohashes,
            )

            if injector and new_torrent_filepath:
                injector.inject_torrent(
                    source_torrent_path,
                    new_torrent_filepath,
                    new_tracker.site_shortname(),
                )

            if new_torrent_filepath and was_previously_generated:
                p.already_exists.print(
                    "Torrent was previously generated but was injected into your torrent client."
                )
            elif new_torrent_filepath:
                p.generated.print(
                    f"Found with source '{new_tracker.site_shortname()}' and generated as '{new_torrent_filepath}'."
                )
        except TorrentDecodingError as e:
            p.error.print(str(e))
            continue
        except UnknownTrackerError as e:
            p.skipped.print(str(e))
            continue
        except TorrentAlreadyExistsError as e:
            p.already_exists.print(str(e))
            continue
        except TorrentExistsInClientError as e:
            p.already_exists.print(str(e))
            continue
        except TorrentNotFoundError as e:
            p.not_found.print(str(e))
            continue
        except Exception as e:
            p.error.print(str(e))
            continue

    return p.report()


def __collect_infohashes_from_files(files: list[str]) -> dict:
    infohash_dict = {}

    for filepath in files:
        try:
            torrent_data = get_bencoded_data(filepath)

            if torrent_data and b'info' in torrent_data:
                infohash = calculate_infohash(torrent_data)
                infohash_dict[infohash] = filepath
        except (UnicodeDecodeError, KeyError):
            continue

    return infohash_dict