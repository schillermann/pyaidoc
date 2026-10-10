"""Callable parameter encapsulation in Pure OOP."""

import inspect
from pyaidoc.default import Default, NoDefault, PresentDefault
from pyaidoc.type_name import TypeName
from pyaidoc.ternary import Ternary
from pyaidoc.tool import Parameter as ParameterProtocol


class CallableParameter:
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
        return Ternary(
            self.required(),
            NoDefault(),
            PresentDefault(self._param.default),
        ).value()

    def __str__(self) -> str:
        return f"{self.name()}: {self.type()}"


Parameter = CallableParameter
