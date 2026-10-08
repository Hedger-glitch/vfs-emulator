"""Точка входа эмулятора."""
import sys
from src.repl import Repl

DEFAULT_VFS_NAME = "myvfs"

def main(argv: list[str]) -> int:
    vfs_name = argv[1] if len(argv) > 1 else DEFAULT_VFS_NAME
    Repl(vfs_name).run()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))