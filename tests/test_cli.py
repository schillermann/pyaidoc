from pathlib import Path
import pytest
from pyaidoc.cli.ai_tools import AiToolsCommand
from pyaidoc.cli.ai_docs import AiDocsCommand
from pyaidoc.cli.target import ToolsTarget, SearchPaths, CandidateSpec, CandidateTools
from pyaidoc.cli.arguments import Arguments
from pyaidoc.cli.output import MemoryOutput, Stdout
from pyaidoc.cli.exit_code import ExitCode, Success, Failure
from pyaidoc.cli.destination import MemoryFile, LocalFile
from pyaidoc.cli.__main__ import CliApp, HelpCommand, UnknownCommand, main
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


def test_search_paths_and_candidate_spec() -> None:
    paths = SearchPaths("/test/project").all()
    assert len(paths) == 4
    assert paths[0] == "/test/project"

    spec = CandidateSpec("my_module:MY_TOOLS")
    assert spec.module_name() == "my_module"
    assert spec.attribute_name() == "MY_TOOLS"

    default_spec = CandidateSpec("my_module")
    assert default_spec.attribute_name() == "tools"


def test_arguments_encapsulation() -> None:
    args = Arguments("tools", "my.module:TOOLS")
    assert args.verb() == "tools"
    assert args.first() == "tools"
    assert args.tail().first() == "my.module:TOOLS"
    assert len(args) == 2
    assert args.empty() is False

    empty = Arguments()
    assert empty.verb() == "help"
    assert empty.empty() is True
    assert empty.first("fallback") == "fallback"


def test_exit_code_objects_purity() -> None:
    success = Success()
    assert success.ok() is True
    assert success.value() == 0
    assert int(success) == 0
    assert success == Success()

    failure = Failure("Something failed")
    assert failure.ok() is False
    assert failure.value() == 1
    assert int(failure) == 1
    assert failure.reason() == "Something failed"
    assert failure == Failure("Something failed")
    assert failure != Success()


def test_memory_output_captures_and_returns_self() -> None:
    out = MemoryOutput.empty()
    returned = out.print("line 1").print("line 2")
    assert returned is out
    assert out.lines() == ("line 1", "line 2")
    assert out.text() == "line 1\nline 2\n"


def test_memory_file_captures_and_returns_self() -> None:
    mem = MemoryFile.empty(Path("test.html"))
    returned = mem.write("<h1>Hello</h1>")
    assert returned is mem
    assert mem.content() == "<h1>Hello</h1>"
    assert mem.path() == Path("test.html")


def test_ai_tools_command_with_memory_output_and_arguments() -> None:
    out = MemoryOutput.empty()
    cmd = AiToolsCommand(output=out)
    code = cmd.execute(Arguments("non_existent:target"))
    assert code.ok() is False
    assert code.value() == 1
    assert "No AI agent tools discovered" in out.text()


def test_ai_docs_command_with_memory_output_and_memory_file() -> None:
    out = MemoryOutput.empty()
    mem_file = MemoryFile.empty(Path("test_out.html"))
    cmd = AiDocsCommand(output=out, destination=mem_file)
    code = cmd.execute(Arguments("non_existent:target"))
    assert code.ok() is False
    assert "No AI agent tools discovered" in out.text()
    assert mem_file.content() == ""


def test_cli_app_dispatch_help_and_unknown() -> None:
    out = MemoryOutput.empty()
    app = CliApp(
        (
            AiToolsCommand(output=out),
            AiDocsCommand(output=out),
            HelpCommand(output=out),
        ),
        output=out,
    )

    help_code = app.execute(Arguments("help"))
    assert help_code.ok() is True
    assert "pyaidoc — AI Function Calls Documentation CLI" in out.text()

    out_unknown = MemoryOutput.empty()
    app_unknown = CliApp(
        (AiToolsCommand(output=out_unknown),),
        output=out_unknown,
    )
    unknown_code = app_unknown.execute(Arguments("invalid_verb"))
    assert unknown_code.ok() is False
    assert "Unknown command: 'invalid_verb'" in out_unknown.text()


def test_main_entry_point_returns_int() -> None:
    res = main(["help"])
    assert res == 0

    res_unknown = main(["not_a_valid_command"])
    assert res_unknown == 1
