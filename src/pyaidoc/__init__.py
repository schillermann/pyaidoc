"""pyaidoc — Zero-annotation, living HTML documentation for AI function calls and agent tools."""

from pyaidoc.default import Default, NoDefault, PresentDefault
from pyaidoc.docstring import Docstring, EmptyDocstring
from pyaidoc.type_name import TypeName
from pyaidoc.parameter import Parameter
from pyaidoc.parameters import Parameters
from pyaidoc.tool import Tool
from pyaidoc.tools import Tools
from pyaidoc.schema_tool import SchemaTool, SchemaParameter, SchemaParameters
from pyaidoc.html.page import Page
from pyaidoc.html.card import Card
from pyaidoc.html.table import Table
from pyaidoc.html.row import Row
from pyaidoc.html.badge import Badge
from pyaidoc.html.section import Section
from pyaidoc.html.style import Style
from pyaidoc.html.document import Document
from pyaidoc.terminal.terminal import Terminal

__version__ = "0.3.0"

__all__ = [
    "__version__",
    "Default",
    "NoDefault",
    "PresentDefault",
    "Docstring",
    "EmptyDocstring",
    "TypeName",
    "Parameter",
    "Parameters",
    "Tool",
    "Tools",
    "SchemaTool",
    "SchemaParameter",
    "SchemaParameters",
    "Badge",
    "Row",
    "Table",
    "Card",
    "Section",
    "Style",
    "Document",
    "Page",
    "Terminal",
]


