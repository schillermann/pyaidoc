"""HTML document skeleton renderer in Pure OOP."""

import html
from pyaidoc.html.style import Style


class Document:
    """Renders a complete, standalone HTML document skeleton."""

    def __init__(self, title: str, content: str, style: Style = Style()) -> None:
        self._title = title
        self._content = content
        self._style = style

    def html(self) -> str:
        escaped_title = html.escape(self._title)
        stylesheet = str(self._style)
        return (
            "<!DOCTYPE html>\n"
            '<html lang="de">\n'
            "<head>\n"
            '  <meta charset="utf-8">\n'
            '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f"  <title>{escaped_title}</title>\n"
            f"  <style>\n{stylesheet}  </style>\n"
            "</head>\n"
            "<body>\n"
            f"{self._content}\n"
            "</body>\n"
            "</html>"
        )

    def __str__(self) -> str:
        return self.html()
