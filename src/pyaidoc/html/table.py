from pyaidoc.html.row import Row
from pyaidoc.parameters import Parameters


class Table:
    """Renders Parameters collection as an HTML table."""

    def __init__(self, params: Parameters) -> None:
        self._params = params

    def html(self) -> str:
        if self._params.empty():
            return '<p class="pyaidoc-no-params">Keine Parameter erforderlich.</p>'

        rows_html = "".join(str(Row(param)) for param in self._params)
        return (
            '<table class="pyaidoc-table">'
            "<thead><tr>"
            "<th>Parameter</th><th>Typ</th><th>Status</th><th>Standardwert</th>"
            "</tr></thead>"
            f"<tbody>{rows_html}</tbody>"
            "</table>"
        )

    def __str__(self) -> str:
        return self.html()
