"""Конфигурация эмулятора."""
import argparse
from pathlib import Path

class Config:
    """Параметры запуска эмулятора."""
    def __init__(self, vfs_path, script_path, vfs_name):
        self.vfs_path = vfs_path
        self.script_path = script_path
        self.vfs_name = vfs_name

def parse_args(argv: list[str]) -> Config:
    """Разбирает аргументы командой строки в объект Config."""
    parser = argparse.ArgumentParser(prog="vfs-emulator")
    parser.add_argument("--vfs", type=Path, help="Путь к файлу VFS")
    parser.add_argument("--script", type=Path, help="Путь к стартовому скрипту")
    parser.add_argument("--name", default="myvfs", help="Имя VFS для приглашения")
    ns = parser.parse_args(argv[1:])
    return Config(
        vfs_path=ns.vfs,
        script_path=ns.script,
        vfs_name=ns.name
    )