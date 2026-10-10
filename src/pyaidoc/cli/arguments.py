"""Command line arguments object in Pure OOP."""


class Arguments:
    """Encapsulates immutable command line arguments in Pure OOP."""

    def __init__(self, *items: str) -> None:
        self._items = items

    def verb(self) -> str:
        """Returns the primary verb or default help."""
        return self._items[0] if self._items else "help"

    def first(self, fallback: str = "") -> str:
        """Returns the first positional argument or fallback."""
        return self._items[0] if self._items else fallback

    def tail(self) -> "Arguments":
        """Returns a new Arguments object with all elements except the first."""
        return Arguments(*self._items[1:])

    def empty(self) -> bool:
        """Indicates whether arguments collection is empty."""
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Arguments{self._items}"
