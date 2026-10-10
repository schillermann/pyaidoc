"""Terminal representation of an AI tool in Pure OOP."""

from pyaidoc.tool import Tool
from pyaidoc.terminal.style import Ansi, StyledText
from pyaidoc.terminal.param import TerminalParam


class TerminalToolCard:
    """Formats an AI tool card with ANSI styling for terminal display."""

    def __init__(self, tool: Tool) -> None:
        self._tool = tool

    def text(self) -> str:
        name = StyledText(self._tool.name(), f"{Ansi.BOLD}{Ansi.CYAN}")
        desc = self._tool.description().strip()
        lines = [f"  ⚡ {name}"]
        if desc:
            lines.append(f"     {StyledText(desc, Ansi.DIM)}")
        params = self._tool.parameters()
        if not params.empty():
            lines.append("     Parameter:")
            for p in params:
                lines.append(TerminalParam(p).text())
        else:
            lines.append(f"     {StyledText('(Keine Parameter)', Ansi.DIM)}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.text()
