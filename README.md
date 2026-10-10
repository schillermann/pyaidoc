# pyaidoc

[![Pure OOP](https://img.shields.io/badge/architecture-Pure%20OOP-blue.svg)](https://www.elegantobjects.org)
[![Zero Annotations](https://img.shields.io/badge/annotations-none-success.svg)](#)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](#)

> Elegant, zero-annotation HTML documentation, OpenAI schema generator, and execution adapter for AI agent tools in Python.

`pyaidoc` inspects Python callables and domain capability objects dynamically via standard type hints and docstrings — rendering a clean, responsive HTML reference, generating standard OpenAI/Anthropic function calling schemas, and executing LLM JSON responses without requiring annotations, DTOs, or external frameworks.

---

## Features

- **Zero Annotations**: Document and expose your AI agent tools without cluttering domain logic with `@tool`, `@doc`, or Pydantic metadata.
- **Pure OOP Architecture**: Designed strictly following Yegor Bugayenko's *[Elegant Objects](https://www.elegantobjects.org)* principles:
  - 100% Code-free constructors (assignments only).
  - True GoF Decorator Pattern: wrap living domain objects (`Tool(capability)`) instead of syntax macros.
  - Zero DTOs or untyped data bags: strongly-typed parameter signatures.
  - Null Object pattern (never returns `None`).
  - Single Source of Truth: type hints and docstrings generate schemas, terminal docs, and HTML docs automatically.
- **OpenAI / LLM Function Schema Generator**: Generates 100% compliant function calling definitions directly from Python methods, including descriptions from Sphinx (`:param ...:`) or Google-style docstrings, choices from `typing.Literal` and `Enum`, and automatic `Optional[...]` unwrapping.
- **Autonomous LLM Invocation**: `await tool.invoke(json_string)` directly binds raw JSON strings from OpenAI to strongly-typed domain method calls.
- **Zero Dependencies**: Pure standard Python 3.10+ — no heavy frameworks or runtime baggage.
- **Clean HTML & Terminal Output**: Modern, responsive styling with dark/light mode support, badge indicators for required/optional parameters, and rich ANSI terminal cards.

---

## Installation

```bash
pip install git+https://github.com/schillermann/pyaidoc.git@main
```

---

## Quickstart

### 1. Pure OOP Domain Capabilities (Zero Annotations)

In Pure OOP, your business capability is an autonomous living object. It knows nothing about AI, OpenAI, or JSON:

```python
from typing import Literal, Optional
from pyaidoc import Tool

class ContactUpsert:
    """Creates or updates contacts in the CRM."""

    async def execute(
        self,
        name: str,
        phone: str = "",
        budget: Optional[float] = None,
        role: Literal["owner", "buyer", "tenant"] = "owner",
    ) -> dict:
        """
        Creates or updates a client contact.

        :param name: Full name of the customer or organization.
        :param phone: Phone or mobile number.
        :param budget: Maximum purchase budget in Euro.
        :param role: Transaction role of the contact.
        """
        return {"status": "saved", "name": name, "budget": budget, "role": role}

# 1. Wrap in the pure OOP Tool decorator:
tool = Tool(ContactUpsert())

# 2. Generate standard OpenAI function calling schema:
print(tool.schema())
# {
#   "type": "function",
#   "function": {
#     "name": "contact_upsert",
#     "description": "Creates or updates contacts in the CRM.",
#     "parameters": { ... }
#   }
# }

# 3. Execute directly with raw JSON string from LLM:
import asyncio
result = asyncio.run(tool.invoke('{"name": "Klaus Meyer", "budget": 650000.0}'))
print(result)
# {'status': 'saved', 'name': 'Klaus Meyer', 'budget': 650000.0, 'role': 'owner'}
```

### 2. Documenting Python Functions

```python
from pathlib import Path
from pyaidoc import Tools, Page, Tool

def assign_document(doc_id: str, deal_id: str, notify: bool = False) -> dict:
    """Assigns a document to a deal and notifies stakeholders."""
    return {"status": "ok"}

def calculate_mortgage(amount: float, interest_rate: float = 3.5) -> dict:
    """Calculates the monthly mortgage payment for a property."""
    return {"rate": 1200.0}

# Compose tools into an immutable collection
tools = Tools(Tool(assign_document), Tool(calculate_mortgage))

# Export standalone HTML file for local viewing
Path("ai_tools_doc.html").write_text(str(Page(tools)), encoding="utf-8")
```

### 3. Documenting OpenAI / JSON Function Calling Schemas

`pyaidoc` also directly documents raw OpenAI / JSON tool calling specifications without conversion:

```python
from pathlib import Path
from pyaidoc import Tools, Page, SchemaTool

tools_specs = [
    {
        "type": "function",
        "function": {
            "name": "contact_upsert",
            "description": "Creates or updates contacts in the CRM.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Full name"},
                    "phone": {"type": "string", "description": "Phone number"},
                },
                "required": ["name"],
            },
        },
    }
]

tools = Tools(*(SchemaTool(spec) for spec in tools_specs))
Path("ai_tools_doc.html").write_text(str(Page(tools, "AI Tools Reference")), encoding="utf-8")
```

---

## CLI Usage

`pyaidoc` provides an autonomous command-line interface for inspecting and generating documentation without writing boilerplate scripts:

### 1. Terminal Inspection

List and inspect tools directly in your terminal:

```bash
pyaidoc tools
```

Or target a specific module/attribute:

```bash
pyaidoc tools my_app.agent:TOOLS
```

### 2. HTML Documentation Generation

Generate standalone HTML documentation:

```bash
pyaidoc docs
# Generates ai_tools_doc.html in current directory
```

### 3. Unified Developer Workflow with `pyresponse` (Optional)

If your project uses [pyresponse](https://github.com/schillermann/pyresponse) for web services and routing, `pyaidoc` automatically registers as a plugin via entry points:

```bash
pyr ai:tools   # inspect tools alongside 'pyr routes'
pyr ai:docs    # generate HTML documentation
```

---

## Architecture

All classes adhere strictly to Pure OOP and package-by-feature composition:

| Object | Role |
|---|---|
| `Tool` | Universal OOP decorator and envelope adapting callables, capability objects, and schemas. |
| `CapabilityTool` | Adapts a domain capability object with an `execute()` method into a living Tool. |
| `CallableTool` | Adapts an external Python callable into an autonomous AI tool. |
| `SchemaTool` | Adapts an OpenAI/JSON tool schema dictionary into an autonomous AI tool. |
| `OpenAiSchema` | Generates OpenAI-compatible function calling schemas from any living Tool. |
| `OpenAiTools` | Generates a collection of OpenAI tool schemas from a list of tools. |
| `JsonType` | Translates Python type annotations to JSON Schema types with `Optional`/`Union` unwrapping. |
| `DocstringParam` | Extracts parameter descriptions from Sphinx, Epydoc, and Google-style docstrings. |
| `AdaptedTool` | Universal envelope adapting callables, schemas, or tools via candidate polymorphism. |
| `Tools` | Pure immutable collection of tools with code-free constructors. |
| `Parameter` | Encapsulates callable parameter type, requirement status, and default value. |
| `Parameters` / `SchemaParameters` | Encapsulates parameter collections derived from signatures or schemas. |
| `TypeName` | Object extracting clean type strings via candidate resolvers (zero `isinstance`). |
| `Docstring` / `EmptyDocstring` | Null Object pattern modeling presence or absence of docstrings without `None`. |
| `Default` / `NoDefault` / `PresentDefault` | Null Object pattern modeling presence or absence of defaults without `None`. |
| `Page` | Standalone HTML documentation page conforming to Pure OOP. |
| `Card` / `Table` / `Row` | Granular, composable HTML UI elements with dependency inversion. |
| `Badge` / `RequiredBadge` / `OptionalBadge` | Polymorphic UI badges for parameter requirement status. |
| `Section` / `Document` / `Style` / `DefaultCss` | Autonomous container, document skeleton, and stylesheet objects (zero global variables). |
| `ExitCode` / `Success` / `Failure` | Autonomous exit code value objects conforming to Pure OOP (no raw ints). |
| `Output` / `Stdout` / `MemoryOutput` | Text stream abstractions eliminating hardcoded global `print()` calls. |
| `FileDestination` / `LocalFile` / `MemoryFile` | Encapsulates storage destinations eliminating procedural file writes. |
| `Arguments` | Encapsulates CLI argument strings in a cohesive object (no raw string lists). |

---

## Testing

Run tests and type verification:

```bash
pytest
pyright src/ tests/
```

---

## License

MIT
