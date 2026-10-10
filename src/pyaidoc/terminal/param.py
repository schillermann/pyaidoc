"""Terminal parameter line formatter in Pure OOP."""

from typing import Any
from pyaidoc.terminal.style import Ansi, StyledText


class TerminalParam:
    """Formats a single parameter for terminal display."""

    def __init__(self, param: Any) -> None:
        self._param = param

    def text(self) -> str:
        name = StyledText(self._param.name(), Ansi.BOLD)
        param_type = StyledText(self._param.type(), Ansi.DIM)
        if self._param.required():
            badge = StyledText("[erforderlich]", Ansi.RED)
        else:
            default = self._param.default()
            if default.present():
                badge = StyledText(f"[optional, standard: {default.text()}]", Ansi.YELLOW)
            else:
                badge = StyledText("[optional]", Ansi.GREEN)
        return f"    • {name}: {param_type} {badge}"

    def __str__(self) -> str:
        return self.text()
