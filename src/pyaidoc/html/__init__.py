"""HTML rendering elements conforming to Pure OOP."""

from pyaidoc.html.badge import Badge, RequiredBadge, OptionalBadge
from pyaidoc.html.row import Row
from pyaidoc.html.table import Table, EmptyTableContent, PopulatedTableContent
from pyaidoc.html.card import Card
from pyaidoc.html.section import Section, EmptySectionCards, PopulatedSectionCards
from pyaidoc.html.style import Style, DefaultCss
from pyaidoc.html.document import Document
from pyaidoc.html.page import Page
from pyaidoc.html.ternary import Ternary

__all__ = [
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
    "Ternary",
]
