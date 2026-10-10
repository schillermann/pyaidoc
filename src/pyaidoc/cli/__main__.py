"""pyaidoc standalone CLI runner in Pure OOP."""

import sys
from typing import Any
from pyaidoc.cli.ai_tools import AiToolsCommand
from pyaidoc.cli.ai_docs import AiDocsCommand
from pyaidoc.cli.output import Output, Stdout
from pyaidoc.cli.exit_code import ExitCode, Success, Failure
from pyaidoc.cli.arguments import Arguments


class HelpCommand:
    """Displays usage instructions for standalone pyaidoc CLI."""

    def __init__(self, output: Output = Stdout()) -> None:
        self._output = output

    @classmethod
    def standard(cls) -> "HelpCommand":
        return cls(Stdout())

    def name(self) -> str:
        return "help"

    def description(self) -> str:
        return "Show usage and available commands."

    def matches(self, verb: str) -> bool:
        return verb in ("help", "--help", "-h", "")

    def execute(self, args: Arguments = Arguments()) -> ExitCode:
        self._output.print("\npyaidoc — AI Function Calls Documentation CLI")
        self._output.print("─────────────────────────────────────────────")
        self._output.print("Usage:")
        self._output.print("  pyaidoc tools [target]    Print formatted tools to the terminal")
        self._output.print("  pyaidoc docs [target]     Generate HTML documentation (ai_tools_doc.html)")
        self._output.print("  pyaidoc help              Show this help menu\n")
        return Success()


class UnknownCommand:
    """Null object fallback for unrecognized CLI verbs."""

    def __init__(self, verb: str, output: Output = Stdout()) -> None:
        self._verb = verb
        self._output = output

    def name(self) -> str:
        return self._verb

    def description(self) -> str:
        return ""

    def matches(self, verb: str) -> bool:
        return False

    def execute(self, args: Arguments = Arguments()) -> ExitCode:
        self._output.print(f"Unknown command: '{self._verb}'. Run 'pyaidoc help' for usage.")
        return Failure(f"Unknown command: '{self._verb}'")


class CliApp:
    """Dispatches standalone pyaidoc verbs to commands without framework dependency."""

    def __init__(self, commands: tuple[Any, ...], output: Output = Stdout()) -> None:
        self._commands = commands
        self._output = output

    @classmethod
    def standard(cls) -> "CliApp":
        return cls(
            (
                AiToolsCommand(),
                AiDocsCommand(),
                HelpCommand(),
            ),
            Stdout(),
        )

    def execute(self, args: Arguments = Arguments()) -> ExitCode:
        verb = args.verb()
        rest = args.tail()
        for cmd in self._commands:
            if cmd.matches(verb):
                return cmd.execute(rest)
        return UnknownCommand(verb, self._output).execute(rest)


def main(args: list[str] | tuple[str, ...] | None = None) -> int:
    cmd_args = Arguments(*sys.argv[1:]) if args is None else Arguments(*args)
    app = CliApp(
        (
            AiToolsCommand(),
            AiDocsCommand(),
            HelpCommand(),
        ),
        Stdout(),
    )
    result: ExitCode = app.execute(cmd_args)
    return result.value()


if __name__ == "__main__":
    sys.exit(main())
