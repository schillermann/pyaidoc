"""Terminal document representation of AI tools in Pure OOP."""

from pyaidoc.tools import Tools
from pyaidoc.terminal.style import Ansi, StyledText
from pyaidoc.terminal.tool_card import TerminalToolCard


class Terminal:
    """Renders AI agent tools as a styled terminal document."""

    def __init__(self, tools: Tools, title: str = "AI Agent Function Calls") -> None:
        self._tools = tools
        self._title = title

    def text(self) -> str:
        count = len(self._tools)
        header = StyledText(f"🤖 {self._title} ({count} Tools)", f"{Ansi.BOLD}{Ansi.GREEN}")
        divider = StyledText("─" * 60, Ansi.DIM)
        sections = [f"\n{header}\n{divider}"]
        for tool in self._tools:
            sections.append(TerminalToolCard(tool).text())
            sections.append(str(divider))
        return "\n".join(sections) + "\n"

    def __str__(self) -> str:
        return self.text()
