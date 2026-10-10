"""Тесты VFS."""
from pathlib import Path

from src.vfs import Vfs


def test_load_minimal():
    """Загрузка минимальной VFS."""
    vfs = Vfs.from_xml(Path("vfs/minimal.xml"))
    assert vfs.name == "minimal"
    assert "readme.txt" in vfs.root.children


def test_load_deep():
    """Загрузка VFS с тремя уровнями вложенности."""
    vfs = Vfs.from_xml(Path("vfs/deep.xml"))
    lvl1 = vfs.root.children["level1"]
    lvl2 = lvl1.children["level2"]
    lvl3 = lvl2.children["level3"]
    assert "deep.txt" in lvl3.children