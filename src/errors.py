import sys
from time import sleep

from colorama import Fore

def handle_error(
  description: str,
  exception_details: (str | None) = None,
  wait_time: int = 0,
  extra_description: str = "",
  should_exit: bool = False,
) -> None:
  action = "Exiting" if should_exit else "Retrying"
  action += f" in {wait_time} seconds..." if wait_time else "..."
  exception_message = f"\n{Fore.LIGHTBLACK_EX}{exception_details}" if exception_details is not None else ""

  print(f"{Fore.RED}Error: {description}{extra_description}. {action}{exception_message}{Fore.RESET}")
  sleep(wait_time)

  if should_exit:
    sys.exit(1)

# Class definitions

class AuthenticationError(Exception):
  # Exception raised for authentication errors
  pass

class TorrentDecodingError(Exception):
  # Exception raised for errors during torrent decoding
  pass

class UnknownTrackerError(Exception):
  # Exception raised for unknown tracker errors
  pass

class TorrentNotFoundError(Exception):
  # Exception raised when a torrent is not found
  pass

class TorrentAlreadyExistsError(Exception):
  # Exception raised when a torrent already exists
  pass

class ConfigKeyError(Exception):
  # Exception raised for configuration key errors
  pass

class TorrentClientError(Exception):
  # Exception raised for torrent client errors
  pass

class TorrentClientAuthenticationError(Exception):
  # Exception raised for torrent client authentication errors
  pass

class TorrentInjectionError(Exception):
  # Exception raised for errors during torrent injection
  pass