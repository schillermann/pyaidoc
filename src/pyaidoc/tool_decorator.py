import inspect
import json
import types
from typing import Any, Callable, Optional
from pyaidoc.adapted_tool import AdaptedTool
from pyaidoc.openai_schema import OpenAiSchema
from pyaidoc.tool import Parameters


class TargetExecutable:
    """Encapsulates target execution for a tool in Pure OOP."""

    def __init__(self, origin: Any) -> None:
        self._origin = origin

    def target(self) -> Callable[..., Any]:
        if hasattr(self._origin, "execute") and callable(getattr(self._origin, "execute")):
            return getattr(self._origin, "execute")
        return self._origin

    def sync_call(self, *args: Any, **kwargs: Any) -> Any:
        return self.target()(*args, **kwargs)

    async def async_call(self, *args: Any, **kwargs: Any) -> Any:
        res = self.target()(*args, **kwargs)
        if inspect.iscoroutine(res):
            return await res
        return res

    def filtered_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        fn = self.target()
        if not callable(fn):
            return kwargs
        sig = inspect.signature(fn)
        has_var_kw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
        if has_var_kw:
            return kwargs
        accepted = set(sig.parameters.keys())
        return {k: v for k, v in kwargs.items() if k in accepted}


class Tool:
    """Universal AI Tool decorator and envelope in Pure OOP."""

    def __init__(
        self,
        origin: Any,
        name: str = "",
        description: str = "",
        ignored: tuple[str, ...] = ("self", "cls"),
    ) -> None:
        self._origin = origin
        self._custom_name = name
        self._custom_description = description
        self._ignored = ignored

    def name(self) -> str:
        if self._custom_name:
            return self._custom_name
        return AdaptedTool(self._origin, ignored=self._ignored).name()

    def description(self) -> str:
        if self._custom_description:
            return self._custom_description
        return AdaptedTool(self._origin, ignored=self._ignored).description()

    def parameters(self) -> Parameters:
        return AdaptedTool(self._origin, ignored=self._ignored).parameters()

    def schema(self) -> dict[str, Any]:
        """Returns the OpenAI / Anthropic / Gemini function calling schema."""
        return OpenAiSchema(self).value()

    def __get__(self, instance: Any, owner: Any = None) -> Any:
        if instance is None:
            return self
        return Tool(
            types.MethodType(self._origin, instance),
            name=self._custom_name,
            description=self._custom_description,
            ignored=self._ignored,
        )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return TargetExecutable(self._origin).sync_call(*args, **kwargs)

    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Asynchronously executes the wrapped tool action."""
        return await TargetExecutable(self._origin).async_call(*args, **kwargs)

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
        executable = TargetExecutable(self._origin)
        return await executable.async_call(**executable.filtered_kwargs(kwargs))

    def __str__(self) -> str:
        return self.name()


def tool(
    origin: Optional[Callable[..., Any]] = None,
    *,
    name: str = "",
    description: str = "",
    ignored: tuple[str, ...] = ("self", "cls"),
) -> Any:
    """Decorator converting a Python function or class into an AI Tool."""
    if origin is not None:
        return Tool(origin, name=name, description=description, ignored=ignored)

    def decorator(fn: Callable[..., Any]) -> Tool:
        return Tool(fn, name=name, description=description, ignored=ignored)

    return decorator

