"""AiDocsCommand generating static HTML documentation in Pure OOP."""

from pathlib import Path
from typing import Any
from pyaidoc.html.page import Page
from pyaidoc.cli.target import ToolsTarget
from pyaidoc.cli.output import Output, Stdout
from pyaidoc.cli.destination import FileDestination, LocalFile
from pyaidoc.cli.exit_code import ExitCode, Success, Failure
from pyaidoc.cli.arguments import Arguments


class AiDocsCommand:
    """Generate static HTML documentation for AI function calls in Pure OOP."""

    def __init__(
        self,
        output: Output = Stdout(),
        destination: FileDestination = LocalFile(Path("ai_tools_doc.html")),
    ) -> None:
        self._output = output
        self._destination = destination

    @classmethod
    def standard(cls) -> "AiDocsCommand":
        """Secondary constructor with standard output and local file destination."""
        return cls(Stdout(), LocalFile(Path("ai_tools_doc.html")))

    def name(self) -> str:
        return "ai:docs"

    def description(self) -> str:
        return "Generate static HTML documentation file (ai_tools_doc.html)."

    def matches(self, verb: str) -> bool:
        return verb in ("ai:docs", "docs")

    def execute(self, args: Any = Arguments()) -> ExitCode:
        parsed = args if isinstance(args, Arguments) else Arguments(*args)
        target = parsed.first()
        tools = ToolsTarget(target).tools()
        if tools.empty():
            self._output.print("No AI agent tools discovered. Specify target via 'pyaidoc docs <module:attr>'.")
            return Failure("No AI agent tools discovered.")
        page = Page(tools, "AI Agent Function Calls Reference")
        self._destination.write(str(page))
        self._output.print(f"✅ HTML documentation for {len(tools)} tools generated successfully!")
        self._output.print(f"📄 File: {self._destination.path()}")
        return Success()
