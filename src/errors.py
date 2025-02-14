import sys
from time import sleep

from colorama import Fore
from .api import OpsAPI, RedAPI, AuthenticationError

def handle_request_error(description: str, exception_details: (str | None) = None, wait_time: int = 0, extra_description: str = "", should_exit: bool = False) -> None:
    action = "Exiting" if should_exit else "Retrying"
    action += f" in {wait_time} seconds..." if wait_time else "..."
    exception_message = f"\n{Fore.LIGHTBLACK_EX}{exception_details}" if exception_details is not None else ""

    print(f"{Fore.RED}Error: {description}{extra_description}. {action}{exception_message}{Fore.RESET}")
    sleep(wait_time)

    if should_exit:
        sys.exit(1)

class TorrentDecodingError(Exception):
    pass

class UnknownTrackerError(Exception):
    pass

class TorrentNotFoundError(Exception):
    pass

class TorrentAlreadyExistsError(Exception):
    pass

class ConfigKeyError(Exception):
    pass

class TorrentClientError(Exception):
    pass

class TorrentInjectionError(Exception):
    pass

class TorrentManager:
    def __init__(self, tracker_name, api_key):
        if tracker_name == 'OPS':
            self.api = OpsAPI(api_key)
        elif tracker_name == 'RED':
            self.api = RedAPI(api_key)
        else:
            raise UnknownTrackerError(f"Unknown tracker: {tracker_name}")

    def find_torrent(self, torrent_hash: str) -> dict:
        try:
            return self.api.find_torrent(torrent_hash)
        except AuthenticationError as e:
            handle_request_error(description=f"Authentication to {self.api.sitename} failed", exception_details=e, should_exit=True)
        except Exception as e:
            handle_request_error(description="Failed to find torrent", exception_details=e)


In the rewritten code, I have encapsulated the request logic for reusability by creating a `TorrentManager` class that takes a tracker name and API key as input. This class initializes the appropriate API object based on the tracker name. The `find_torrent` method of this class handles the request to find a torrent and explicitly handles authentication errors. I have also improved error handling for better clarity by using a separate `handle_request_error` function to handle request errors.