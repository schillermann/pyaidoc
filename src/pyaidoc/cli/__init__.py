"""pyaidoc CLI package in Pure OOP."""

from pyaidoc.cli.target import (
    ToolsTarget,
    SearchPaths,
    CandidateSpec,
    CandidateTools,
    TargetCandidates,
)
from pyaidoc.cli.ai_tools import AiToolsCommand
from pyaidoc.cli.ai_docs import AiDocsCommand
from pyaidoc.cli.arguments import Arguments
from pyaidoc.cli.output import Output, Stdout, MemoryOutput
from pyaidoc.cli.exit_code import ExitCode, Success, Failure
from pyaidoc.cli.destination import FileDestination, LocalFile, MemoryFile

__all__ = [
    "ToolsTarget",
    "SearchPaths",
    "CandidateSpec",
    "CandidateTools",
    "TargetCandidates",
    "AiToolsCommand",
    "AiDocsCommand",
    "Arguments",
    "Output",
    "Stdout",
    "MemoryOutput",
    "ExitCode",
    "Success",
    "Failure",
    "FileDestination",
    "LocalFile",
    "MemoryFile",
]
