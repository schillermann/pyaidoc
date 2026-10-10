"""AiToolsCommand printing AI function calls to the terminal."""

from pyaidoc.terminal import Terminal
from pyaidoc.cli.target import ToolsTarget


class AiToolsCommand:
    """Print formatted AI agent function calls to the terminal."""

    def name(self) -> str:
        return "ai:tools"

    def description(self) -> str:
        return "Print formatted AI agent function calls to the terminal."

    def matches(self, verb: str) -> bool:
        return verb in ("ai:tools", "tools")

    def execute(self, args: list[str]) -> int:
        target = args[0] if args else ""
        tools = ToolsTarget(target).tools()
        if tools.empty():
            print("No AI agent tools discovered. Specify target via 'pr ai:tools <module:attr>'.")
            return 1
        print(Terminal(tools, "AI Function Calls Reference"))
        return 0
