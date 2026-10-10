"""Тесты парсера."""
from src.parser import parse_command


def test_simple():
    assert parse_command("ls -la") == ("ls", ["-la"])


def test_quotes():
    assert parse_command('ls "my folder"') == ("ls", ["my folder"])


def test_empty():
    assert parse_command("   ") == ("", [])


def test_syntax_error():
    try:
        parse_command('ls "unclosed')
    except ValueError:
        return
    assert False, "expected ValueError"