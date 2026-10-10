"""pyaidoc standalone CLI runner in Pure OOP."""

import sys
from typing import Any
from pyaidoc.cli.ai_tools import AiToolsCommand
from pyaidoc.cli.ai_docs import AiDocsCommand


class HelpCommand:
    """Displays usage instructions for standalone pyaidoc CLI."""

    def name(self) -> str:
        return "help"

    def description(self) -> str:
        return "Show usage and available commands."

    def matches(self, verb: str) -> bool:
        return verb in ("help", "--help", "-h", "")

    def execute(self, args: list[str]) -> int:
        print("\npyaidoc — AI Function Calls Documentation CLI")
        print("─────────────────────────────────────────────")
        print("Usage:")
        print("  pyaidoc tools [target]    Print formatted tools to the terminal")
        print("  pyaidoc docs [target]     Generate HTML documentation (ai_tools_doc.html)")
        print("  pyaidoc help              Show this help menu\n")
        return 0


class CliApp:
    """Dispatches standalone pyaidoc verbs to commands without framework dependency."""

    def __init__(self, *commands: Any) -> None:
        self._commands = commands

    def execute(self, args: list[str]) -> int:
        verb = args[0] if args else "help"
        rest = args[1:] if args else []
        for cmd in self._commands:
            if cmd.matches(verb):
                return cmd.execute(rest)
        print(f"Unknown command: '{verb}'. Run 'pyaidoc help' for usage.")
        return 1


def main(args: list[str] | None = None) -> int:
    cmd_args = sys.argv[1:] if args is None else args
    app = CliApp(
        AiToolsCommand(),
        AiDocsCommand(),
        HelpCommand(),
    )
    return app.execute(cmd_args)


if __name__ == "__main__":
    sys.exit(main())
