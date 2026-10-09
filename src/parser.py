"""Парсер командной строки с поддержкой кавычек"""
import shlex

def parse_command(line: str) -> tuple[str, list[str]]:
    """Разбирает строку на команду и аргументы (с учетом кавычек)."""
    try:
        tokens = shlex.split(line)
    except ValueError as ex:
        raise ValueError(f"syntax error: {ex}") from ex
    if not tokens:
        return "", []
    return tokens[0], tokens[1::]