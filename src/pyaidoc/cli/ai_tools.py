"""AiToolsCommand printing AI function calls to an output stream in Pure OOP."""

from typing import Any
from pyaidoc.terminal import Terminal
from pyaidoc.cli.target import ToolsTarget
from pyaidoc.cli.output import Output, Stdout
from pyaidoc.cli.exit_code import ExitCode, Success, Failure
from pyaidoc.cli.arguments import Arguments


class AiToolsCommand:
    """Print formatted AI agent function calls to an output stream in Pure OOP."""

    def __init__(self, output: Output = Stdout()) -> None:
        self._output = output

    @classmethod
    def standard(cls) -> "AiToolsCommand":
        """Secondary constructor with standard terminal output."""
        return cls(Stdout())

    def name(self) -> str:
        return "ai:tools"

    def description(self) -> str:
        return "Print formatted AI agent function calls to the terminal."

    def matches(self, verb: str) -> bool:
        return verb in ("ai:tools", "tools")

    def execute(self, args: Any = Arguments()) -> ExitCode:
        parsed = args if isinstance(args, Arguments) else Arguments(*args)
        target = parsed.first()
        tools = ToolsTarget(target).tools()
        if tools.empty():
            self._output.print("No AI agent tools discovered. Specify target via 'pyaidoc tools <module:attr>'.")
            return Failure("No AI agent tools discovered.")
        self._output.print(str(Terminal(tools, "AI Function Calls Reference")))
        return Success()
