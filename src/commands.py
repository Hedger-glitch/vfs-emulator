"""Реализация команд оболочки."""

def cmd_ls(state, args):
    """ls [путь] — показать содержимое каталога."""
    path = args[0] if args else "."
    node = state.resolve(path)
    if not node.is_dir:
        print(node.name)
        return
    for name in sorted(node.children):
        print(name)


def cmd_cd(state, args):
    """cd [путь] — сменить текущий каталог."""
    path = args[0] if args else "/"
    state.change_dir(path)


def _read_lines(state, path):
    """Прочитать файл как список строк. Бросает ошибку, если это папка."""
    node = state.resolve(path)
    if node.is_dir:
        raise IsADirectoryError(path)
    text = node.content.decode("utf-8", errors="replace")
    return text.splitlines()


def cmd_rev(state, args):
    """rev файл — вывести строки файла в обратном порядке символов."""
    if not args:
        raise ValueError("rev: missing file operand")
    for line in _read_lines(state, args[0]):
        print(line[::-1])


def cmd_uniq(state, args):
    """uniq файл — убрать подряд идущие одинаковые строки."""
    if not args:
        raise ValueError("uniq: missing file operand")
    prev = None
    for line in _read_lines(state, args[0]):
        if line != prev:
            print(line)
        prev = line


def cmd_head(state, args):
    """head [-N] файл — вывести первые N строк (по умолчанию 10)."""
    n = 10
    path = None

    if args and args[0].startswith("-") and args[0][1:].isdigit():
        n = int(args[0][1:])
        path = args[1] if len(args) > 1 else None
    elif args:
        path = args[0]

    if path is None:
        raise ValueError("head: missing file operand")

    for line in _read_lines(state, path)[:n]:
        print(line)