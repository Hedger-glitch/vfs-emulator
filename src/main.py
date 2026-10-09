"""Точка входа эмулятора."""
import sys

from src.config import parse_args
from src.repl import Repl


def main(argv: list[str]) -> int:
    config = parse_args(argv)
    Repl(config).run()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))