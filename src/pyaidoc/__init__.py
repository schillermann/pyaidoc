"""pyaidoc — Zero-annotation, living HTML documentation for AI function calls and agent tools."""

from pyaidoc.default import Default, NoDefault, PresentDefault
from pyaidoc.docstring import Docstring, EmptyDocstring
from pyaidoc.type_name import TypeName
from pyaidoc.parameter import Parameter, CallableParameter
from pyaidoc.parameters import Parameters, CallableParameters
from pyaidoc.tool import Tool
from pyaidoc.callable_tool import CallableTool
from pyaidoc.schema_tool import SchemaTool, SchemaParameter, SchemaParameters
from pyaidoc.adapted_tool import AdaptedTool
from pyaidoc.tools import Tools, AdaptedTools
from pyaidoc.html.page import Page
from pyaidoc.html.card import Card
from pyaidoc.html.table import Table, EmptyTableContent, PopulatedTableContent
from pyaidoc.html.row import Row
from pyaidoc.html.badge import Badge, RequiredBadge, OptionalBadge
from pyaidoc.html.section import Section, EmptySectionCards, PopulatedSectionCards
from pyaidoc.html.style import Style, DefaultCss
from pyaidoc.html.document import Document
from pyaidoc.terminal.terminal import Terminal
from pyaidoc.ternary import Ternary

__version__ = "0.4.1"

__all__ = [
    "__version__",
    "Default",
    "NoDefault",
    "PresentDefault",
    "Docstring",
    "EmptyDocstring",
    "TypeName",
    "Parameter",
    "CallableParameter",
    "Parameters",
    "CallableParameters",
    "Tool",
    "CallableTool",
    "SchemaTool",
    "SchemaParameter",
    "SchemaParameters",
    "AdaptedTool",
    "Tools",
    "AdaptedTools",
    "Badge",
    "RequiredBadge",
    "OptionalBadge",
    "Row",
    "Table",
    "EmptyTableContent",
    "PopulatedTableContent",
    "Card",
    "Section",
    "EmptySectionCards",
    "PopulatedSectionCards",
    "Style",
    "DefaultCss",
    "Document",
    "Page",
    "Terminal",
    "Ternary",
]
