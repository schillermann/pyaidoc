import inspect
from pyaidoc.default import Default, NoDefault, PresentDefault
from pyaidoc.type_name import TypeName


class Parameter:
    """Encapsulates a callable parameter conforming to Pure OOP."""

    def __init__(self, param: inspect.Parameter) -> None:
        self._param = param

    def name(self) -> str:
        return self._param.name

    def type(self) -> str:
        return TypeName(self._param.annotation).text()

    def required(self) -> bool:
        return self._param.default is inspect._empty

    def default(self) -> Default:
        if self.required():
            return NoDefault()
        return PresentDefault(self._param.default)

    def __str__(self) -> str:
        return f"{self.name()}: {self.type()}"
