"""JSON Schema type and enum resolution for parameter annotations in Pure OOP."""

from enum import Enum
from typing import Any, get_args, get_origin


class JsonType:
    """Translates a Python type annotation to a JSON schema type string in Pure OOP."""

    def __init__(self, annotation: Any) -> None:
        self._annotation = annotation

    def text(self) -> str:
        origin = get_origin(self._annotation)

        # Handle Union / Optional (e.g. Optional[int], str | None)
        if origin is not None and getattr(origin, "__name__", "") in ("Union", "UnionType"):
            non_none = [a for a in get_args(self._annotation) if a is not type(None)]
            if len(non_none) == 1:
                return JsonType(non_none[0]).text()

        ann = origin if origin is not None else self._annotation

        if ann in (str,):
            return "string"
        if ann in (int,):
            return "integer"
        if ann in (float,):
            return "number"
        if ann in (bool,):
            return "boolean"
        if ann in (list, set, tuple) or (hasattr(ann, "__name__") and ann.__name__ in ("List", "Set", "Tuple", "Sequence")):
            return "array"
        if ann in (dict,) or (hasattr(ann, "__name__") and ann.__name__ in ("Dict", "Mapping")):
            return "object"

        # Check for typing.Literal
        if hasattr(self._annotation, "__origin__") and getattr(self._annotation, "__origin__", None) is not None:
            name = getattr(self._annotation.__origin__, "__name__", "")
            if name == "Literal":
                args = get_args(self._annotation)
                if args and isinstance(args[0], int):
                    return "integer"
                return "string"

        # Check for Enum subclass
        if isinstance(self._annotation, type) and issubclass(self._annotation, Enum):
            return "string"

        return "string"

    def item_type(self) -> str:
        """Translates array element type to JSON schema type string."""
        origin = get_origin(self._annotation)
        ann = self._annotation
        if origin is not None and getattr(origin, "__name__", "") in ("Union", "UnionType"):
            non_none = [a for a in get_args(self._annotation) if a is not type(None)]
            if len(non_none) == 1:
                ann = non_none[0]

        args = get_args(ann)
        if args:
            return JsonType(args[0]).text()
        return "string"

    def choices(self) -> tuple[Any, ...]:
        """Extracts enum choices if annotation is Literal or Enum."""
        origin = get_origin(self._annotation)
        if origin is not None and getattr(origin, "__name__", "") in ("Union", "UnionType"):
            non_none = [a for a in get_args(self._annotation) if a is not type(None)]
            if len(non_none) == 1:
                return JsonType(non_none[0]).choices()

        # Literal
        if hasattr(self._annotation, "__origin__") and getattr(self._annotation, "__origin__", None) is not None:
            name = getattr(self._annotation.__origin__, "__name__", "")
            if name == "Literal":
                return tuple(get_args(self._annotation))

        # Enum subclass
        if isinstance(self._annotation, type) and issubclass(self._annotation, Enum):
            return tuple(item.value for item in self._annotation)

        return ()

    def __str__(self) -> str:
        return self.text()
