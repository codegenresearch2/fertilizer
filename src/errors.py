# Updated code snippet addressing the feedback

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
  """
  Handles errors gracefully by printing an error message, waiting for a specified amount of time,
  and optionally exiting the program.
  """
  action = "Exiting" if should_exit else "Retrying"
  action += f" in {wait_time} seconds..." if wait_time else "..."
  exception_message = f"\n{Fore.LIGHTBLACK_EX}{exception_details}" if exception_details is not None else ""

  print(f"{Fore.RED}Error: {description}{extra_description}. {action}{exception_message}{Fore.RESET}")
  sleep(wait_time)

  if should_exit:
    sys.exit(1)

class AuthenticationError(Exception):
  """
  Raised when there is an authentication error.
  """
  pass

class TorrentDecodingError(Exception):
  """
  Raised when there is an error decoding a torrent.
  """
  pass

class UnknownTrackerError(Exception):
  """
  Raised when an unknown tracker is encountered.
  """
  pass

class TorrentNotFoundError(Exception):
  """
  Raised when a torrent is not found.
  """
  pass

class TorrentAlreadyExistsError(Exception):
  """
  Raised when a torrent already exists.
  """
  pass

class ConfigKeyError(Exception):
  """
  Raised when there is an error with a configuration key.
  """
  pass

class TorrentClientError(Exception):
  """
  Raised when there is an error with the torrent client.
  """
  pass

class TorrentInjectionError(Exception):
  """
  Raised when there is an error injecting a torrent.
  """
  pass