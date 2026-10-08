"""REPL-цикл эмулятора оболочки."""
from src.commands import cmd_ls, cmd_cd
from src.parcer import parse_command

STUB_COMMANDS = {"ls": cmd_ls, "cd": cmd_cd}

class Repl:
    """Интерактивная оболочка."""

    def __init__(self, vfs_name: str) -> None:
        self.vfs_name = vfs_name
        self.running = True

    def prompt(self) -> str:
        return f"{self.vfs_name}> "

    def run(self) -> None:
        while self.running:
            try:
                line = input(self.prompt())
            except EOFError:
                print()
                break
            try:
                self.handle(line)
            except ValueError as ex:
                print(f"Error: {ex}")

    def handle(self, line: str) -> None:
        command, args = parse_command(line)
        if not command:
            return
        if command == "exit":
            self.running = False
            return
        handler = STUB_COMMANDS.get(command)
        if handler is None:
            raise ValueError(f"unknown command '{command}'")
        handler(args)