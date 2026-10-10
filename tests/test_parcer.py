"""Тесты парсера."""
from src.parser import parse_command


def test_simple():
    """Простой случай: команда и один аргумент."""
    assert parse_command("ls -la") == ("ls", ["-la"])


def test_quotes():
    """Аргумент в кавычках — один аргумент с пробелом."""
    assert parse_command('ls "my folder"') == ("ls", ["my folder"])


def test_empty():
    """Пустая строка — пустая команда."""
    assert parse_command("   ") == ("", [])