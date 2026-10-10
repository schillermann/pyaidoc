"""Callable parameter encapsulation in Pure OOP."""

import inspect
from typing import Any, Callable, Optional
from pyaidoc.default import Default, NoDefault, PresentDefault
from pyaidoc.type_name import TypeName
from pyaidoc.ternary import Ternary
from pyaidoc.docstring_param import DocstringParam
from pyaidoc.json_type import JsonType


class CallableParameter:
    """Encapsulates a callable parameter conforming to Pure OOP."""

    def __init__(
        self,
        param: inspect.Parameter,
        origin: Optional[Callable[..., Any]] = None,
    ) -> None:
        self._param = param
        self._origin = origin

    def name(self) -> str:
        return self._param.name

    def type(self) -> str:
        return TypeName(self._param.annotation).text()

    def schema_type(self) -> str:
        return JsonType(self._param.annotation).text()

    def item_type(self) -> str:
        return JsonType(self._param.annotation).item_type()

    def choices(self) -> tuple[Any, ...]:
        return JsonType(self._param.annotation).choices()

    def description(self) -> str:
        if self._origin is not None:
            doc_desc = DocstringParam(self._origin, self.name()).text()
            if doc_desc:
                return doc_desc
        return ""

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
