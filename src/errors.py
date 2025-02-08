def handle_error(description: str, exception_details: (str | None) = None, wait_time: int = 0, extra_description: str = '', should_exit: bool = False) -> None:\n    action = 'Exiting' if should_exit else 'Retrying'\n    action += f' in {wait_time} seconds...' if wait_time else '...'\n    exception_message = f'\n{Fore.LIGHTBLACK_EX}{exception_details}' if exception_details is not None else ''\n    print(f'{Fore.RED}Error: {description}{extra_description}. {action}{exception_message}{Fore.RESET}')\n    sleep(wait_time)\n    if should_exit:\n        sys.exit(1)