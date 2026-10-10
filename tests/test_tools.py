from pyaidoc.tool import Tool
from pyaidoc.tools import Tools


def tool_a() -> None:
    pass


def tool_b() -> None:
    pass


def test_tools_collection_composition() -> None:
    tools = Tools(tool_a, tool_b)
    all_tools = tools.all()
    assert len(all_tools) == 2
    assert all_tools[0].name() == "tool_a"
    assert all_tools[1].name() == "tool_b"
    assert tools.empty() is False



def test_tools_immutability_plus() -> None:
    initial = Tools(tool_a)
    updated = initial.plus(tool_b)
    assert len(initial.all()) == 1
    assert len(updated.all()) == 2


def test_tools_empty() -> None:
    tools = Tools()
    assert tools.empty() is True
    assert len(tools) == 0


def test_package_version() -> None:
    import pyaidoc
    assert pyaidoc.__version__ == "0.3.0"


