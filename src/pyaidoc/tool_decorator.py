import inspect
import json
import types
from typing import Any, Callable, Optional
from pyaidoc.adapted_tool import AdaptedTool
from pyaidoc.openai_schema import OpenAiSchema
from pyaidoc.tool import Parameters


class Tool:
    """Universal AI Tool decorator and envelope in Pure OOP."""

    def __init__(
        self,
        origin: Any,
        name: str = "",
        description: str = "",
    ) -> None:
        self._origin = origin
        self._custom_name = name
        self._custom_description = description

    def name(self) -> str:
        if self._custom_name:
            return self._custom_name
        return AdaptedTool(self._origin).name()

    def description(self) -> str:
        if self._custom_description:
            return self._custom_description
        return AdaptedTool(self._origin).description()

    def parameters(self) -> Parameters:
        return AdaptedTool(self._origin).parameters()

    def schema(self) -> dict[str, Any]:
        """Returns the OpenAI / Anthropic / Gemini function calling schema."""
        return OpenAiSchema(self).value()

    def __get__(self, instance: Any, owner: Any = None) -> Any:
        if instance is None:
            return self
        return Tool(types.MethodType(self._origin, instance), name=self._custom_name, description=self._custom_description)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        target = (
            getattr(self._origin, "execute")
            if hasattr(self._origin, "execute") and callable(getattr(self._origin, "execute"))
            else self._origin
        )
        return target(*args, **kwargs)

    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Asynchronously executes the wrapped tool action."""
        target = (
            getattr(self._origin, "execute")
            if hasattr(self._origin, "execute") and callable(getattr(self._origin, "execute"))
            else self._origin
        )
        res = target(*args, **kwargs)
        if inspect.iscoroutine(res):
            return await res
        return res

    async def invoke(self, arguments: Any = None, **extra_kwargs: Any) -> Any:
        """Asynchronously executes the tool, parsing arguments from JSON string or mapping."""
        kwargs: dict[str, Any] = {}
        if isinstance(arguments, str):
            trimmed = arguments.strip()
            if trimmed:
                kwargs = json.loads(trimmed)
        elif isinstance(arguments, dict):
            kwargs = dict(arguments)
        kwargs.update(extra_kwargs)
        return await self.execute(**kwargs)

    def __str__(self) -> str:
        return self.name()


def tool(origin: Optional[Callable[..., Any]] = None, *, name: str = "", description: str = "") -> Any:
    """Decorator converting a Python function or class into an AI Tool."""
    if origin is not None:
        return Tool(origin, name=name, description=description)

    def decorator(fn: Callable[..., Any]) -> Tool:
        return Tool(fn, name=name, description=description)

    return decorator
