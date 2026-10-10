from pyaidoc.tools import Tools
from pyaidoc.terminal import Terminal, TerminalToolCard, TerminalParam
from pyaidoc.schema_tool import SchemaTool


SAMPLE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "contact_upsert",
        "description": "Erfasst Kunden im CRM.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "role": {"type": "string", "default": "buyer"},
            },
            "required": ["name"],
        },
    },
}


def test_terminal_param_output() -> None:
    tool = SchemaTool(SAMPLE_SCHEMA)
    params = list(tool.parameters())
    name_param = TerminalParam(params[0])
    role_param = TerminalParam(params[1])

    assert "name" in str(name_param)
    assert "[erforderlich]" in str(name_param)
    assert "role" in str(role_param)
    assert "[optional, standard: \"buyer\"]" in str(role_param)


def test_terminal_tool_card_output() -> None:
    tool = SchemaTool(SAMPLE_SCHEMA)
    card = TerminalToolCard(tool)
    output = str(card)

    assert "contact_upsert" in output
    assert "Erfasst Kunden im CRM." in output
    assert "name" in output


def test_terminal_full_document() -> None:
    tools = Tools(SAMPLE_SCHEMA)
    doc = Terminal(tools, "Test Suite Tools")
    output = str(doc)

    assert "Test Suite Tools (1 Tools)" in output
    assert "contact_upsert" in output
