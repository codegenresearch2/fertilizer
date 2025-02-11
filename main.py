import os
from colorama import Fore

from src.api import RedAPI, OpsAPI
from src.args import parse_args
from src.config import Config
from src.scanner import scan_torrent_directory, scan_torrent_file
from src.webserver import run_webserver
from src.errors import TorrentDecodingError, UnknownTrackerError, TorrentNotFoundError, TorrentAlreadyExistsError

def cli_entrypoint(args, config_file=None, server=False, input_file=None, input_directory=None, output_directory=None):
    try:
        config = Config().load(config_file) if config_file else Config()
        red_api, ops_api = __verify_api_keys(config)

        if server:
            run_webserver(input_directory, output_directory, red_api, ops_api, port=os.environ.get("PORT", 9713))
        elif input_file:
            result = scan_torrent_file(input_file, output_directory, red_api, ops_api)
            print(result if result else "Error occurred while scanning the file")
        elif input_directory:
            report = scan_torrent_directory(input_directory, output_directory, red_api, ops_api)
            print(report if report else "Error occurred while scanning the directory")
    except Exception as e:
        print(f"{Fore.RED}{str(e)}{Fore.RESET}")
        exit(1)

def __verify_api_keys(config):
    red_api = RedAPI(config.get('red_key', ''))
    ops_api = OpsAPI(config.get('ops_key', ''))

    try:
        red_api.announce_url
        ops_api.announce_url
    except Exception as e:
        print(f"{Fore.RED}Error verifying API keys: {str(e)}{Fore.RESET}")
        exit(1)

    return red_api, ops_api

if __name__ == "__main__":
    args = parse_args()

    try:
        cli_entrypoint(args, args.config_file, args.server, args.input_file, args.input_directory, args.output_directory)
    except KeyboardInterrupt:
        print(f"{Fore.RED}Exiting...{Fore.RESET}")
        exit(1)