import os
from colorama import Fore

from src.api import RedAPI, OpsAPI
from src.args import parse_args
from src.config import Config
from src.scanner import scan_torrent_directory, scan_torrent_file
from src.webserver import run_webserver


def __verify_api_keys(config):
    """
    Verifies the API keys by initializing the RedAPI and OpsAPI instances.
    Performs any necessary checks or lookups.
    """
    red_api = RedAPI(config.red_key)
    ops_api = OpsAPI(config.ops_key)

    # This will perform a lookup with the API and raise if there was a failure.
    # Also caches the announce URL for future use which is a nice bonus
    red_api.announce_url
    ops_api.announce_url

    return red_api, ops_api


def cli_entrypoint(args):
    try:
        config = Config().load(args.config_file)
        port = config.get("webserver_port", os.environ.get("PORT", 9713))
        red_api, ops_api = __verify_api_keys(config)

        if args.server:
            run_webserver(args.input_directory, args.output_directory, red_api, ops_api, port=port)
        elif args.input_file:
            print(scan_torrent_file(args.input_file, args.output_directory, red_api, ops_api))
        elif args.input_directory:
            print(scan_torrent_directory(args.input_directory, args.output_directory, red_api, ops_api))
    except Exception as e:
        print(f"{Fore.RED}{str(e)}{Fore.RESET}")
        exit(1)


if __name__ == "__main__":
    args = parse_args()

    try:
        cli_entrypoint(args)
    except KeyboardInterrupt:
        print(f"{Fore.RED}Exiting...{Fore.RESET}")
        exit(1)