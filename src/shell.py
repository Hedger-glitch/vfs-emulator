"""Состояние оболочки: текущий каталог и работа с путями."""

class ShellState:
    """Хранит VFS и текущий каталог, умеет разрешать пути."""

    def __init__(self, vfs):
        self.vfs = vfs
        self.cwd_parts = []  # путь от корня; [] = корень

    def cwd(self):
        """Вернуть узел текущей папки."""
        node = self.vfs.root
        for part in self.cwd_parts:
            node = node.children[part]
        return node

    def _compute_parts(self, path):
        """Превратить путь в список имён от корня.

        Умеет: '/', '/a/b', 'a/b', '..', '.', 'a/../b'.
        """
        if path.startswith("/"):
            parts = []
        else:
            parts = list(self.cwd_parts)

        for part in path.split("/"):
            if part == "" or part == ".":
                continue
            if part == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(part)

        return parts

    def resolve(self, path):
        """Путь -> узел VFS. Бросает FileNotFoundError, если путь не найден."""
        parts = self._compute_parts(path)
        node = self.vfs.root
        for part in parts:
            if not node.is_dir or part not in node.children:
                raise FileNotFoundError(path)
            node = node.children[part]
        return node

    def change_dir(self, path):
        """Сменить текущий каталог."""
        parts = self._compute_parts(path)
        target = self.resolve(path)
        if not target.is_dir:
            raise NotADirectoryError(path)
        self.cwd_parts = parts