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
from pyaidoc import Tools, Page

def assign_document(doc_id: str, deal_id: str, notify: bool = False) -> dict:
    """Weist ein Dokument einem Deal zu und benachrichtigt Beteiligte."""
    return {"status": "ok"}

def calculate_mortgage(amount: float, interest_rate: float = 3.5) -> dict:
    """Berechnet die monatliche Kreditrate für eine Immobilie."""
    return {"rate": 1200.0}

# Compose tools into an immutable collection
tools = Tools(assign_document, calculate_mortgage)

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
            "description": "Erfasst oder aktualisiert Kunden im CRM.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Vollständiger Name"},
                    "phone": {"type": "string", "description": "Telefonnummer"},
                },
                "required": ["name"],
            },
        },
    }
]

tools = Tools(*tools_specs)
Path("ai_tools_doc.html").write_text(str(Page(tools, "AI Tools Reference")), encoding="utf-8")
```

### 3. Viewing in the Browser & Regenerating on Changes

Open the generated documentation directly in your browser:

```bash
xdg-open ai_tools_doc.html
# or: google-chrome ai_tools_doc.html / firefox ai_tools_doc.html
```

Whenever you add new AI Function Calls or change parameters in your codebase, simply re-run your generation script:

```bash
python scripts/generate_ai_docs.py
```

---

## Architecture

All classes adhere strictly to Pure OOP and package-by-feature composition:

| Object | Role |
|---|---|
| `Tool` | Represents an autonomous AI tool / function call from a Python callable. |
| `SchemaTool` | Represents an AI tool / function call from an OpenAI/JSON tool schema. |
| `Tools` | Immutable collection of tools supporting `.plus(tool)`. |
| `Parameter` | Encapsulates callable parameter type, requirement status, and default value. |
| `SchemaParameter` | Encapsulates schema property type, requirement status, and default value. |
| `Parameters` / `SchemaParameters` | Encapsulates parameter collections derived from signatures or schemas. |
| `TypeName` | Object extracting clean, readable type strings from annotations. |
| `Docstring` / `EmptyDocstring` | Null Object pattern modeling presence or absence of docstrings without `None`. |
| `Default` / `NoDefault` / `PresentDefault` | Null Object pattern modeling presence or absence of defaults without `None`. |
| `Page` | Standalone HTML documentation page conforming to Pure OOP. |
| `Card` / `Table` / `Row` / `Badge` | Granular, composable HTML UI elements. |
| `Section` / `Document` / `Style` | Autonomous container, document skeleton, and CSS stylesheet objects. |




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
