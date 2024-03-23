from common.shared_main import shared_main

from voting_system import scheme


def main() -> None:
    shared_main("elections_test", scheme)


if __name__ == "__main__":
    main()
