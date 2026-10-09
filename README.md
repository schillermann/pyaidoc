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
from pyaidoc import Tools, Page

def assign_document(doc_id: str, deal_id: str, notify: bool = False) -> dict:
    """Weist ein Dokument einem Deal zu und benachrichtigt Beteiligte."""
    return {"status": "ok"}

def calculate_mortgage(amount: float, interest_rate: float = 3.5) -> dict:
    """Berechnet die monatliche Kreditrate für eine Immobilie."""
    return {"rate": 1200.0}

# Compose tools into an immutable collection
tools = Tools(assign_document, calculate_mortgage)

# Render standalone HTML documentation
page = Page(tools)
html_output = page.html()

# Or get just the embedded section for an existing dashboard:
section = page.section_html()
```

---

## Architecture

All classes adhere strictly to Pure OOP and package-by-feature composition:

| Object | Role |
|---|---|
| `Tool` | Represents an autonomous AI tool / function call from a Python callable. |
| `Tools` | Immutable collection of tools supporting `.plus(tool)`. |
| `Parameter` | Encapsulates parameter type, requirement status, and default value. |
| `Parameters` | Encapsulates the collection of parameters derived from a signature. |
| `TypeName` | Object extracting clean, readable type strings from annotations. |
| `Docstring` / `EmptyDocstring` | Null Object pattern modeling presence or absence of docstrings without `None`. |
| `Default` / `NoDefault` / `PresentDefault` | Null Object pattern modeling presence or absence of defaults without `None`. |
| `Page` | Standalone HTML documentation page conforming to Pure OOP. |
| `Card` / `Table` / `Row` / `Badge` | Granular, composable HTML UI elements. |
| `Section` / `Document` / `Style` | Autonomous container, document skeleton, and CSS stylesheet objects. |



---

## Ecosystem & Web Integration

`pyaidoc` is 100% autonomous and has zero external dependencies. It pairs naturally with other Pure OOP libraries in the ecosystem:

* **[pyresponse](https://github.com/schillermann/pyresponse)**: A declarative, pure object-oriented ASGI web framework.

Because `pyaidoc` produces clean HTML strings through living objects, integrating it into a `pyresponse` route requires zero glue code:

```python
from pyresponse import Get
from pyresponse.response.text import Text
from pyresponse.response.header import Header
from pyaidoc import Tools, Page

# Expose living AI tool documentation over HTTP
route = Get(
    "/ai-tools",
    Header(Text(str(Page(tools))), "content-type", "text/html; charset=utf-8"),
)
```

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
