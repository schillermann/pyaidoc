"""OpenAI / JSON schema tool representation in Pure OOP."""

from typing import Any, Iterator
from pyaidoc.default import Default, NoDefault, PresentDefault
from pyaidoc.tool import Tool, Parameter, Parameters
from pyaidoc.ternary import Ternary


class EnumParameterType:
    """Encapsulates display of enum parameter types."""

    def __init__(self, prop: dict[str, Any]) -> None:
        self._prop = prop

    def matched(self) -> bool:
        return "enum" in self._prop

    def text(self) -> str:
        raw = self._prop.get("type", "any")
        return f"enum ({raw})"


class StandardParameterType:
    """Encapsulates display of standard primitive parameter types."""

    def __init__(self, prop: dict[str, Any]) -> None:
        self._prop = prop

    def matched(self) -> bool:
        return True

    def text(self) -> str:
        return str(self._prop.get("type", "any"))


class SchemaParameterType:
    """Candidate-driven resolver for schema parameter types."""

    def __init__(self, prop: dict[str, Any]) -> None:
        self._prop = prop

    def text(self) -> str:
        candidates = (EnumParameterType(self._prop), StandardParameterType(self._prop))
        for candidate in candidates:
            if candidate.matched():
                return candidate.text()
        return "any"

    def __str__(self) -> str:
        return self.text()


class SchemaParameter:
    """Encapsulates a parameter declared in a JSON/OpenAI tool schema."""

    def __init__(
        self,
        name: str,
        prop: dict[str, Any],
        required_names: tuple[str, ...] = (),
    ) -> None:
        self._name = name
        self._prop = prop
        self._required_names = required_names

    def name(self) -> str:
        return self._name

    def type(self) -> str:
        return str(SchemaParameterType(self._prop))

    def required(self) -> bool:
        return self._name in self._required_names

    def default(self) -> Default:
        return Ternary(
            "default" in self._prop,
            PresentDefault(self._prop.get("default")),
            NoDefault(),
        ).value()

    def __str__(self) -> str:
        return f"{self.name()}: {self.type()}"


class SchemaParameters:
    """Encapsulates parameters collection declared in a JSON tool schema."""

    def __init__(self, params: dict[str, Any]) -> None:
        self._params = params

    def items(self) -> tuple[SchemaParameter, ...]:
        props: dict[str, Any] = self._params.get("properties", {})
        required_names: tuple[str, ...] = tuple(self._params.get("required", []))
        return tuple(
            SchemaParameter(name, prop, required_names)
            for name, prop in props.items()
        )

    def empty(self) -> bool:
        return len(self.items()) == 0

    def __iter__(self) -> Iterator[SchemaParameter]:
        return iter(self.items())

    def __len__(self) -> int:
        return len(self.items())


class SchemaFunction:
    """Encapsulates the function definition extracted from a tool spec."""

    def __init__(self, spec: dict[str, Any]) -> None:
        self._spec = spec

    def body(self) -> dict[str, Any]:
        fn: Any = self._spec.get("function")
        if hasattr(fn, "get"):
            return fn
        return self._spec

    def name(self) -> str:
        return str(self.body().get("name", ""))

    def description(self) -> str:
        return str(self.body().get("description", ""))

    def parameters_dict(self) -> dict[str, Any]:
        raw = self.body().get("parameters", {})
        return raw if hasattr(raw, "get") else {}


class SchemaTool:
    """Represents an AI function call or agent tool from a JSON/OpenAI schema."""

    def __init__(self, spec: dict[str, Any]) -> None:
        self._function = SchemaFunction(spec)

    def name(self) -> str:
        return self._function.name()

    def description(self) -> str:
        return self._function.description()

    def parameters(self) -> Parameters:
        return SchemaParameters(self._function.parameters_dict())

    def __str__(self) -> str:
        return self.name()
