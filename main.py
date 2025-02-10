import os
from colorama import Fore

from src.api import RedAPI, OpsAPI
from src.args import parse_args
from src.config import Config
from src.scanner import scan_torrent_directory, scan_torrent_file
from src.webserver import run_webserver

class EnhancedConfig(Config):
    def __init__(self, config_file=None):
        super().__init__()
        self.config_file = config_file
        self.config_data = self.load(config_file)

    @property
    def red_key(self):
        return self.config_data.get('red_key', 'default_red_key')

    @property
    def ops_key(self):
        return self.config_data.get('ops_key', 'default_ops_key')

def cli_entrypoint(args):
    try:
        config = EnhancedConfig(args.config_file)
        red_api, ops_api = verify_api_keys(config)

        if args.server:
            run_webserver(args.input_directory, args.output_directory, red_api, ops_api, port=os.environ.get("PORT", 9713))
        elif args.input_file:
            print(scan_torrent_file(args.input_file, args.output_directory, red_api, ops_api))
        elif args.input_directory:
            print(scan_torrent_directory(args.input_directory, args.output_directory, red_api, ops_api))
    except KeyError as e:
        print(f"{Fore.RED}Missing key in configuration: {str(e)}{Fore.RESET}")
        exit(1)
    except Exception as e:
        print(f"{Fore.RED}{str(e)}{Fore.RESET}")
        exit(1)

def verify_api_keys(config):
    red_api = RedAPI(config.red_key)
    ops_api = OpsAPI(config.ops_key)

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
        cli_entrypoint(args)
    except KeyboardInterrupt:
        print(f"{Fore.RED}Exiting...{Fore.RESET}")
        exit(1)