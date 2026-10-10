"""AiDocsCommand generating static HTML documentation."""

from pathlib import Path
from pyaidoc.html.page import Page
from pyaidoc.cli.target import ToolsTarget


class AiDocsCommand:
    """Generate static HTML documentation for AI function calls."""

    def name(self) -> str:
        return "ai:docs"

    def description(self) -> str:
        return "Generate static HTML documentation file (ai_tools_doc.html)."

    def matches(self, verb: str) -> bool:
        return verb in ("ai:docs", "docs")

    def execute(self, args: list[str]) -> int:
        target = args[0] if args else ""
        tools = ToolsTarget(target).tools()
        if tools.empty():
            print("No AI agent tools discovered. Specify target via 'pr ai:docs <module:attr>'.")
            return 1
        dest = Path.cwd() / "ai_tools_doc.html"
        page = Page(tools, "AI Agent Function Calls Reference")
        dest.write_text(str(page), encoding="utf-8")
        print(f"✅ HTML documentation for {len(tools)} tools generated successfully!")
        print(f"📄 File: {dest}")
        return 0
