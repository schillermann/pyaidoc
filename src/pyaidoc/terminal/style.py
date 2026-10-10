"""ANSI terminal styling encapsulation in Pure OOP."""


class Ansi:
    """Terminal ANSI styling codes."""

    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    RESET = "\033[0m"


class StyledText:
    """Decorates a text segment with ANSI formatting."""

    def __init__(self, text: str, code: str) -> None:
        self._text = text
        self._code = code

    def __str__(self) -> str:
        return f"{self._code}{self._text}{Ansi.RESET}"
