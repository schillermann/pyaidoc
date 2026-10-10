# pyaidoc

[![Pure OOP](https://img.shields.io/badge/architecture-Pure%20OOP-blue.svg)](https://www.elegantobjects.org)
[![Zero Annotations](https://img.shields.io/badge/annotations-none-success.svg)](#)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](#)

> Elegant, zero-annotation HTML documentation for AI agent tools and function calls in Python.

`pyaidoc` inspects Python callables and objects representing AI tools dynamically via standard type hints and signatures — rendering a clean, responsive, human-readable HTML reference without requiring decorators, annotations, or external dependencies.

---

## Features

- **Zero Annotations**: Document your AI agent tools without cluttering domain logic with `@tool`, `@doc`, or Pydantic metadata.
- **Pure OOP Architecture**: Designed strictly following Yegor Bugayenko's *[Elegant Objects](https://www.elegantobjects.org)* principles:
  - 100% Code-free constructors (assignments only).
  - No getters, setters, or JavaBeans prefixes (`is...`, `has...`).
  - Null Object pattern (never returns `None`).
  - Immutable objects and composable decorators.
  - Zero static methods or utility classes.
- **Zero Dependencies**: Pure standard Python 3.10+ — no heavy frameworks or runtime baggage.
- **Clean HTML Output**: Modern, responsive styling with dark/light mode support, badge indicators for required/optional parameters, and parameter tables.

---

## Installation

```bash
pip install pyaidoc
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/schillermann/pyaidoc.git@main
```

---

## Quickstart

### 1. Documenting Python Functions

```python
from pathlib import Path
from pyaidoc import CallableTool, Tools, Page

def assign_document(doc_id: str, deal_id: str, notify: bool = False) -> dict:
    """Assigns a document to a deal and notifies stakeholders."""
    return {"status": "ok"}

def calculate_mortgage(amount: float, interest_rate: float = 3.5) -> dict:
    """Calculates the monthly mortgage payment for a property."""
    return {"rate": 1200.0}

# Compose tools into an immutable collection
tools = Tools(CallableTool(assign_document), CallableTool(calculate_mortgage))

# Export standalone HTML file for local viewing
Path("ai_tools_doc.html").write_text(str(Page(tools)), encoding="utf-8")
```

### 2. Documenting OpenAI / JSON Function Calling Schemas

`pyaidoc` also directly documents OpenAI / JSON tool calling specifications without conversion:

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

### 3. Viewing in the Browser & Regenerating on Changes

Open the generated documentation directly in your browser:

```bash
xdg-open ai_tools_doc.html
# or: google-chrome ai_tools_doc.html / firefox ai_tools_doc.html
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
pr ai:tools   # inspect tools alongside 'pr routes'
pr ai:docs    # generate HTML documentation
```

---

## Architecture

All classes adhere strictly to Pure OOP and package-by-feature composition:

| Object | Role |
|---|---|
| `Tool` | Pure protocol specifying name, description, and parameters for any tool. |
| `CallableTool` | Adapts an external Python callable into an autonomous AI tool. |
| `SchemaTool` | Adapts an OpenAI/JSON tool schema dictionary into an autonomous AI tool. |
| `SchemaFunction` | Encapsulates function definition and parameter dictionaries in JSON schemas. |
| `AdaptedTool` | Universal envelope adapting callables, schemas, or tools via candidate polymorphism. |
| `Tools` | Pure immutable collection of tools with code-free constructors. |
| `AdaptedTools` | Envelope decorator collection adapting arbitrary callables or schemas via composition. |
| `Parameter` | Encapsulates callable parameter type, requirement status, and default value. |
| `SchemaParameter` | Encapsulates schema property type, requirement status, and default value. |
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
