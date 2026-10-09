from pyaidoc.parameter import Parameter


class Badge:
    """Renders parameter requirement status as an HTML badge."""

    def __init__(self, param: Parameter) -> None:
        self._param = param

    def html(self) -> str:
        if self._param.required():
            return '<span class="pyaidoc-badge req">Erforderlich</span>'
        return '<span class="pyaidoc-badge opt">Optional</span>'

    def __str__(self) -> str:
        return self.html()
