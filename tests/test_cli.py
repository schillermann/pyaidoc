import pytest
from pyaidoc.cli.ai_tools import AiToolsCommand
from pyaidoc.cli.ai_docs import AiDocsCommand
from pyaidoc.cli.target import ToolsTarget
from pyaidoc.tools import Tools


def test_ai_tools_command_matches() -> None:
    cmd = AiToolsCommand()
    assert cmd.name() == "ai:tools"
    assert cmd.matches("ai:tools") is True
    assert cmd.matches("tools") is True
    assert cmd.matches("serve") is False


def test_ai_docs_command_matches() -> None:
    cmd = AiDocsCommand()
    assert cmd.name() == "ai:docs"
    assert cmd.matches("ai:docs") is True
    assert cmd.matches("docs") is True


def test_tools_target_fallback() -> None:
    target = ToolsTarget("non_existent:module")
    tools = target.tools()
    assert isinstance(tools, Tools)
    assert tools.empty() is True
