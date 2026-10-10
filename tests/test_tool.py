import pytest
from pyaidoc.tool import Tool
from pyaidoc.callable_tool import CallableTool
from pyaidoc.adapted_tool import AdaptedTool
from pyaidoc.parameters import Parameters


def assign_document(doc_id: str, deal_id: str, notify: bool = False) -> dict:
    """Weist ein Dokument einem Deal zu und benachrichtigt Beteiligte."""
    return {"status": "ok"}


def undocumented_tool(query: str) -> None:
    pass


class ActionAgent:
    """Verarbeitet eingehende Kundenanfragen."""

    def handle(self, query: str) -> None:
        """Führt eine Kundenanfrage aus."""
        pass


def test_tool_name_and_description() -> None:
    tool: Tool = CallableTool(assign_document)
    assert tool.name() == "assign_document"
    assert str(tool) == "assign_document"
    assert tool.description() == "Weist ein Dokument einem Deal zu und benachrichtigt Beteiligte."
    params = list(tool.parameters())
    assert len(params) == 3
    assert params[0].name() == "doc_id"
    assert params[0].type() == "str"
    assert params[0].required() is True
    assert params[2].name() == "notify"
    assert params[2].default().text() == "False"


def test_tool_from_method() -> None:
    agent = ActionAgent()
    tool: Tool = CallableTool(agent.handle)
    assert tool.name() == "handle"
    assert tool.description() == "Führt eine Kundenanfrage aus."
    params = list(tool.parameters())
    assert len(params) == 1
    assert params[0].name() == "query"


def test_undocumented_tool_fallback() -> None:
    tool: Tool = CallableTool(undocumented_tool)
    assert tool.description() == "Keine Beschreibung verfügbar."


def test_parameters_fails_fast_on_invalid_origin() -> None:
    with pytest.raises(TypeError):
        Parameters(12345).items()  # type: ignore[arg-type]


def test_adapted_tool_from_function_and_schema() -> None:
    callable_tool = CallableTool(assign_document)
    assert callable_tool.name() == "assign_document"

    adapted_func: Tool = AdaptedTool(assign_document)
    assert adapted_func.name() == "assign_document"
    assert "Weist ein Dokument" in adapted_func.description()

    schema = {
        "function": {
            "name": "calc",
            "description": "Calculate something",
            "parameters": {"type": "object", "properties": {}},
        }
    }
    adapted_schema: Tool = AdaptedTool(schema)
    assert adapted_schema.name() == "calc"
    assert adapted_schema.description() == "Calculate something"


def test_adapted_tool_from_capability_instance() -> None:
    class DummyCapability:
        """Erfasst einen neuen Kunden im CRM."""

        def name(self) -> str:
            return "customer_intake"

        def execute(self, full_name: str, email: str = "") -> dict:
            return {"name": full_name, "email": email}

    cap = DummyCapability()
    tool: Tool = AdaptedTool(cap)
    assert tool.name() == "customer_intake"
    assert "Erfasst einen neuen Kunden" in tool.description()
    params = list(tool.parameters())
    assert len(params) == 2
    assert params[0].name() == "full_name"
    assert params[0].required() is True
    assert params[1].name() == "email"
    assert params[1].required() is False


@pytest.mark.asyncio
async def test_tool_invoke_filters_unexpected_kwargs() -> None:
    from pyaidoc.tool_decorator import Tool as DecoratorTool

    class StrictCapability:
        def name(self) -> str:
            return "strict"

        async def execute(self, message: str) -> str:
            return f"echo: {message}"

    tool = DecoratorTool(StrictCapability())
    res = await tool.invoke({"message": "hello", "unexpected_hallucination": 123}, tenant_id="t_1")
    assert res == "echo: hello"


def test_docstring_present_and_empty() -> None:
    from pyaidoc.docstring import Docstring, EmptyDocstring

    def with_doc() -> None:
        """Some docstring."""
        pass

    def without_doc() -> None:
        pass

    assert Docstring(with_doc).present() is True
    assert Docstring(with_doc).empty() is False
    assert Docstring(without_doc).present() is False
    assert Docstring(without_doc).empty() is True
    assert EmptyDocstring().present() is False
    assert EmptyDocstring().empty() is True


def test_tool_custom_ignored_parameters() -> None:
    from pyaidoc.tool_decorator import Tool as DecoratorTool

    class AppCapability:
        def name(self) -> str:
            return "app_action"

        def ignored_parameters(self) -> tuple[str, ...]:
            return ("self", "framework_ctx")

        def execute(self, title: str, framework_ctx: str = "") -> None:
            pass

    cap_tool = DecoratorTool(AppCapability())
    param_names = [p.name() for p in cap_tool.parameters()]
    assert param_names == ["title"]



