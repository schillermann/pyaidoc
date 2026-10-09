from pyaidoc.schema_tool import SchemaTool, SchemaParameter, SchemaParameters
from pyaidoc.tools import Tools
from pyaidoc.html.page import Page


SAMPLE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "contact_upsert",
        "description": "Erfasst oder aktualisiert Kunden im CRM.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Vollständiger Name"},
                "role": {
                    "type": "string",
                    "enum": ["buyer", "owner"],
                    "default": "buyer",
                },
            },
            "required": ["name"],
        },
    },
}


def test_schema_tool_properties() -> None:
    tool = SchemaTool(SAMPLE_SCHEMA)
    assert tool.name() == "contact_upsert"
    assert tool.description() == "Erfasst oder aktualisiert Kunden im CRM."
    assert str(tool) == "contact_upsert"

    params = tool.parameters()
    assert params.empty() is False
    assert len(params) == 2

    items = params.items()
    name_p = items[0]
    assert name_p.name() == "name"
    assert name_p.type() == "string"
    assert name_p.required() is True
    assert name_p.default().present() is False

    role_p = items[1]
    assert role_p.name() == "role"
    assert "enum" in role_p.type()
    assert role_p.required() is False
    assert role_p.default().present() is True
    assert role_p.default().text() == '"buyer"'


def test_schema_tool_in_tools_collection() -> None:
    tools = Tools(SAMPLE_SCHEMA)
    page = Page(tools, "AI Tools")
    html = page.html()

    assert "contact_upsert" in html
    assert "Erfasst oder aktualisiert Kunden im CRM." in html
    assert "name" in html
    assert "Erforderlich" in html
    assert "Optional" in html
