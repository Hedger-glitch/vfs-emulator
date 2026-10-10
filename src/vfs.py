"""Виртуальная файловая система в памяти."""
import base64
import xml.etree.ElementTree as ET


class VfsError(Exception):
    """Ошибка загрузки или работы VFS."""
    pass


class VfsNode:
    """Узел дерева: либо папка, либо файл."""

    def __init__(self, name, is_dir, content=b"", mode=0o644):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.mode = mode
        self.children = {}

    def add_child(self, node):
        """Добавить дочерний узел в словарь по его имени."""
        self.children[node.name] = node


class Vfs:
    """Виртуальная файловая система, живущая в памяти."""

    def __init__(self, root, name):
        self.root = root
        self.name = name

    @staticmethod
    def from_xml(path):
        """Загрузить VFS из XML-файла. Возвращает объект Vfs."""
        try:
            tree = ET.parse(path)
        except FileNotFoundError as exc:
            raise VfsError(f"file not found: {path}") from exc
        except ET.ParseError as exc:
            raise VfsError(f"invalid XML: {exc}") from exc

        root_el = tree.getroot()
        if root_el.tag != "vfs":
            raise VfsError("root element must be <vfs>")

        name = root_el.get("name", "vfs")
        root_node = Vfs._parse_root(root_el)
        return Vfs(root_node, name)

    @staticmethod
    def _parse_root(el):
        """Разбирает корневой <vfs>: находит внутри <dir>."""
        dir_el = el.find("dir")
        if dir_el is None:
            raise VfsError("vfs must contain <dir>")
        return Vfs._parse_dir(dir_el)

    @staticmethod
    def _parse_dir(el):
        """Рекурсивно разбирает <dir>: файлы и вложенные папки."""
        node = VfsNode(name=el.get("name", "/"), is_dir=True)

        for child in el:
            if child.tag == "dir":
                node.add_child(Vfs._parse_dir(child))
            elif child.tag == "file":
                content = Vfs._parse_file_content(child)
                node.add_child(VfsNode(
                    name=child.get("name", ""),
                    is_dir=False,
                    content=content,
                ))
            else:
                raise VfsError(f"unknown tag <{child.tag}>")

        return node

    @staticmethod
    def _parse_file_content(el):
        """Достаёт содержимое файла из base64."""
        raw = el.get("content", "")
        try:
            return base64.b64decode(raw)
        except Exception as exc:
            raise VfsError(f"invalid base64 in file {el.get('name')}") from exc


def default_vfs():
    """Пустая VFS, если файл не указан."""
    root = VfsNode(name="/", is_dir=True)
    return Vfs(root=root, name="default")