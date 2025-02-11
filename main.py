import os
from colorama import Fore

from src.api import RedAPI, OpsAPI
from src.args import parse_args
from src.config import Config
from src.scanner import scan_torrent_directory, scan_torrent_file
from src.webserver import run_webserver

def cli_entrypoint(args):
    try:
        config = Config().load(args.config_file)
        red_api, ops_api = __verify_api_keys(config)

        if args.server:
            run_webserver(args.input_directory, args.output_directory, red_api, ops_api, port=config.server_port)
        elif args.input_file:
            print(scan_torrent_file(args.input_file, args.output_directory, red_api, ops_api))
        elif args.input_directory:
            print(scan_torrent_directory(args.input_directory, args.output_directory, red_api, ops_api))
    except Exception as e:
        print(f"{Fore.RED}{str(e)}{Fore.RESET}")
        exit(1)

def __verify_api_keys(config):
    # Initialize API objects with provided keys
    red_api = RedAPI(config.red_key)
    ops_api = OpsAPI(config.ops_key)

    try:
        # Perform a lookup with the API to validate keys and cache the announce URL for future use
        red_api.announce_url
        ops_api.announce_url
    except Exception as e:
        print(f"{Fore.RED}Error verifying API keys: {str(e)}{Fore.RESET}")
        exit(1)

    return red_api, ops_api

if __name__ == "__main__":
    args = parse_args()

    try:
        cli_entrypoint(args)
    except KeyboardInterrupt:
        print(f"{Fore.RED}Exiting...{Fore.RESET}")
        exit(1)