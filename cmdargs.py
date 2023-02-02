import sys


def get_all_args() -> list:
    return sys.argv


def find_arg(arg: str) -> bool:
    return arg in sys.argv


def num_args() -> int:
    return len(sys.argv)
