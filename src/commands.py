"""Реализация команд оболочки."""

HEAD_DEFAULT_LINES = 10
MIN_ARGS_TWO_OPERANDS = 2

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
    n = HEAD_DEFAULT_LINES
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


def cmd_mv(state, args):
    """mv источник цель — переместить или переименовать файл/папку."""
    if len(args) < MIN_ARGS_TWO_OPERANDS:
        raise ValueError("mv: missing operand")

    src_path = args[0]
    dst_path = args[1]

    src_node = state.resolve(src_path)

    try:
        dst_node = state.resolve(dst_path)
        if dst_node.is_dir:
            new_parent = dst_node
            new_name = src_node.name
        else:
            new_parent = _parent_of(state, dst_path)
            new_name = dst_node.name
    except FileNotFoundError:
        new_parent = _parent_of(state, dst_path)
        new_name = dst_path.rstrip("/").split("/")[-1]

    _remove_from_tree(state.vfs.root, src_node)

    src_node.name = new_name
    new_parent.add_child(src_node)


def _parent_of(state, path):
    """Найти родительский узел для пути."""
    if path.startswith("/"):
        parent_path = path.rsplit("/", 1)[0]
        if parent_path == "":
            parent_path = "/"
    else:
        if "/" in path:
            parent_path = path.rsplit("/", 1)[0]
        else:
            parent_path = "."
    return state.resolve(parent_path)


def _remove_from_tree(node, target):
    """Рекурсивно удалить target из дерева node. Возвращает True, если нашли."""
    for name, child in list(node.children.items()):
        if child is target:
            del node.children[name]
            return True
        if child.is_dir and _remove_from_tree(child, target):
            return True
    return False


def cmd_chmod(state, args):
    """chmod режим путь... — изменить права доступа."""
    if len(args) < MIN_ARGS_TWO_OPERANDS:
        raise ValueError("chmod: missing operand")

    mode_str = args[0]
    try:
        mode = int(mode_str, 8)
    except ValueError:
        raise ValueError(f"chmod: invalid mode '{mode_str}'")

    for path in args[1:]:
        node = state.resolve(path)
        node.mode = mode