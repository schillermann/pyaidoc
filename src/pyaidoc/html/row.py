import html
from pyaidoc.html.badge import Badge
from pyaidoc.parameter import Parameter


class Row:
    """Renders a single Parameter as an HTML table row via pure polymorphism."""

    def __init__(self, param: Parameter) -> None:
        self._param = param

    def html(self) -> str:
        escaped_name = html.escape(self._param.name())
        escaped_type = html.escape(self._param.type())
        default_html = self._param.default().html()
        badge_html = str(Badge(self._param))

        return (
            "<tr>"
            f"<td><code>{escaped_name}</code></td>"
            f'<td><span class="pyaidoc-type">{escaped_type}</span></td>'
            f"<td>{badge_html}</td>"
            f"<td>{default_html}</td>"
            "</tr>"
        )

    def __str__(self) -> str:
        return self.html()
