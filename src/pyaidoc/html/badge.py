"""HTML Badge rendering in Pure OOP."""

from typing import Any
from pyaidoc.html.ternary import Ternary
from pyaidoc.tool import Parameter


class RequiredBadge:
    """Renders requirement badge for mandatory parameters."""

    def __init__(self, label: str = "Erforderlich") -> None:
        self._label = label

    def html(self) -> str:
        return f'<span class="pyaidoc-badge req">{self._label}</span>'

    def __str__(self) -> str:
        return self.html()


class OptionalBadge:
    """Renders requirement badge for optional parameters."""

    def __init__(self, label: str = "Optional") -> None:
        self._label = label

    def html(self) -> str:
        return f'<span class="pyaidoc-badge opt">{self._label}</span>'

    def __str__(self) -> str:
        return self.html()


class Badge:
    """Renders parameter requirement status as an HTML badge in Pure OOP."""

    def __init__(
        self,
        param: Parameter,
        required_badge: Any = RequiredBadge(),
        optional_badge: Any = OptionalBadge(),
    ) -> None:
        self._param = param
        self._required_badge = required_badge
        self._optional_badge = optional_badge

    def html(self) -> str:
        return str(
            Ternary(
                self._param.required(),
                self._required_badge,
                self._optional_badge,
            )
        )

    def __str__(self) -> str:
        return self.html()
