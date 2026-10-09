"""OpenAI / JSON schema tool representation in Pure OOP."""

from typing import Any, Iterator
from pyaidoc.default import Default, NoDefault, PresentDefault


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
        raw_type = self._prop.get("type", "any")
        if "enum" in self._prop:
            return f"enum ({raw_type})"
        return str(raw_type)

    def required(self) -> bool:
        return self._name in self._required_names

    def default(self) -> Default:
        if "default" in self._prop:
            return PresentDefault(self._prop["default"])
        return NoDefault()

    def __str__(self) -> str:
        return f"{self.name()}: {self.type()}"


class SchemaParameters:
    """Encapsulates parameters collection declared in a JSON tool schema."""

    def __init__(self, params: dict[str, Any]) -> None:
        self._params = params

    def items(self) -> list[SchemaParameter]:
        props: dict[str, Any] = self._params.get("properties", {})
        required_names: tuple[str, ...] = tuple(self._params.get("required", []))
        return [
            SchemaParameter(name, prop, required_names)
            for name, prop in props.items()
        ]


    def empty(self) -> bool:
        return len(self.items()) == 0

    def __iter__(self) -> Iterator[SchemaParameter]:
        return iter(self.items())

    def __len__(self) -> int:
        return len(self.items())


class SchemaTool:
    """Represents an AI function call or agent tool from a JSON/OpenAI schema."""

    def __init__(self, spec: dict[str, Any]) -> None:
        self._spec = spec

    def name(self) -> str:
        body: dict[str, Any] = self._spec.get("function", self._spec)
        return str(body.get("name", ""))

    def description(self) -> str:
        body: dict[str, Any] = self._spec.get("function", self._spec)
        return str(body.get("description", ""))

    def parameters(self) -> SchemaParameters:
        body: dict[str, Any] = self._spec.get("function", self._spec)
        params: dict[str, Any] = body.get("parameters", {})
        return SchemaParameters(params)

    def __str__(self) -> str:
        return self.name()

