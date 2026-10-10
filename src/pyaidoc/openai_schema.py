"""OpenAI / Anthropic / Gemini function calling schema generator in Pure OOP."""

from typing import Any, Sequence
from pyaidoc.tool import Tool, Parameter, Tools as ToolsProtocol


class OpenAiParameterProperty:
    """Encapsulates a single parameter property dictionary in Pure OOP."""

    def __init__(self, param: Parameter) -> None:
        self._param = param

    def dictionary(self) -> dict[str, Any]:
        p_type = getattr(self._param, "schema_type", lambda: self._param.type().lower())()
        prop: dict[str, Any] = {"type": p_type}

        desc = getattr(self._param, "description", lambda: "")()
        if desc:
            prop["description"] = desc

        choices = getattr(self._param, "choices", lambda: ())()
        if choices:
            prop["enum"] = list(choices)

        if p_type == "array":
            i_type = getattr(self._param, "item_type", lambda: "string")()
            prop["items"] = {"type": i_type}

        if not self._param.required() and not self._param.default().empty():
            prop["default"] = self._param.default().value()

        return prop


class OpenAiSchema:
    """Generates an OpenAI-compatible function calling tool schema from a Tool in Pure OOP."""

    def __init__(self, tool: Tool) -> None:
        self._tool = tool

    def value(self) -> dict[str, Any]:
        properties: dict[str, Any] = {}
        required: list[str] = []

        for param in self._tool.parameters():
            properties[param.name()] = OpenAiParameterProperty(param).dictionary()
            if param.required():
                required.append(param.name())

        parameters_schema: dict[str, Any] = {
            "type": "object",
            "properties": properties,
        }
        if required:
            parameters_schema["required"] = required

        return {
            "type": "function",
            "function": {
                "name": self._tool.name(),
                "description": self._tool.description(),
                "parameters": parameters_schema,
            },
        }

    def dictionary(self) -> dict[str, Any]:
        return self.value()


class OpenAiTools:
    """Collection adapter producing a list of OpenAI function calling schemas in Pure OOP."""

    def __init__(self, tools: Sequence[Tool] | ToolsProtocol) -> None:
        self._tools = tools

    def list(self) -> list[dict[str, Any]]:
        items: Sequence[Tool] = (
            self._tools.all() if isinstance(self._tools, ToolsProtocol) else self._tools
        )
        return [OpenAiSchema(tool).value() for tool in items]
