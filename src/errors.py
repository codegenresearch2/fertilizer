import sys
from time import sleep

from colorama import Fore

from src.api import OpsAPI, RedAPI, AuthenticationError
from src.progress import Progress

class TorrentClient:
    def __init__(self, tracker, api_key):
        if tracker == 'OPS':
            self.api = OpsAPI(api_key)
        elif tracker == 'RED':
            self.api = RedAPI(api_key)
        else:
            raise UnknownTrackerError(f'Unknown tracker: {tracker}')

    def find_torrent(self, torrent_hash):
        try:
            return self.api.find_torrent(torrent_hash)
        except AuthenticationError as e:
            raise AuthenticationError(f'Authentication to {self.api.sitename} failed') from e
        except Exception as e:
            raise TorrentClientError(f'Error while finding torrent on {self.api.sitename}') from e

    @property
    def announce_url(self):
        return self.api.announce_url

def handle_error(description: str, exception_details: str = None, wait_time: int = 0, extra_description: str = "", should_exit: bool = False) -> None:
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

class TorrentInjectionError(Exception):
    pass

I have rewritten the code according to the provided rules. I have added a `TorrentClient` class that encapsulates the request logic for reusability. The `find_torrent` method now handles authentication errors explicitly and improves error handling for better clarity. The `handle_error` function remains unchanged. The exception classes `TorrentDecodingError`, `UnknownTrackerError`, `TorrentNotFoundError`, `TorrentAlreadyExistsError`, `ConfigKeyError`, and `TorrentInjectionError` are also left unchanged.