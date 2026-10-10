"""REPL-цикл эмулятора оболочки."""
from pathlib import Path

from src.commands import cmd_ls, cmd_cd, cmd_rev, cmd_uniq, cmd_head
from src.parser import parse_command
from src.shell import ShellState

COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "rev": cmd_rev,
    "uniq": cmd_uniq,
    "head": cmd_head,
}


class Repl:
    """Интерактивная оболочка."""

    def __init__(self, config, vfs):
        self.config = config
        self.vfs = vfs
        self.vfs_name = vfs.name
        self.state = ShellState(vfs)
        self.running = True
        self._debug_dump()

    def _debug_dump(self):
        print("[debug] configuration:")
        print(f"  vfs_path    = {self.config.vfs_path}")
        print(f"  script_path = {self.config.script_path}")

    def prompt(self):
        return f"{self.vfs_name}> "

    def run(self):
        if self.config.script_path is not None:
            self.run_script(self.config.script_path)
            return
        self.run_interactive()

    def run_interactive(self):
        while self.running:
            try:
                line = input(self.prompt())
            except EOFError:
                print()
                break
            self.handle_safe(line)

    def run_script(self, path):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            print(f"Error: script not found: {path}")
            return

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            print(f"{self.prompt()}{line}")
            self.handle_safe(line)
            if not self.running:
                break

    def handle_safe(self, line):
        try:
            self.handle(line)
        except ValueError as exc:
            print(f"Error: {exc}")
        except (FileNotFoundError,
            NotADirectoryError,
            IsADirectoryError
        ) as exc:
            print(f"Error: {exc}")

    def handle(self, line):
        command, args = parse_command(line)
        if not command:
            return
        if command == "exit":
            self.running = False
            print("Bye!")
            return
        handler = COMMANDS.get(command)
        if handler is None:
            raise ValueError(f"unknown command '{command}'")
        handler(self.state, args)