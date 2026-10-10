"""Точка входа эмулятора."""
import sys

from src.config import parse_args
from src.repl import Repl
from src.vfs import Vfs, VfsError, default_vfs


def main(argv):
    config = parse_args(argv)

    if config.vfs_path is not None:
        try:
            vfs = Vfs.from_xml(config.vfs_path)
        except VfsError as exc:
            print(f"Error loading VFS: {exc}")
            return 1
    else:
        vfs = default_vfs()
        print("[debug] VFS not specified, using default in-memory VFS")

    Repl(config, vfs).run()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))