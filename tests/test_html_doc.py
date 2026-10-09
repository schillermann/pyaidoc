from pyaidoc.html.page import Page
from pyaidoc.html.card import Card
from pyaidoc.html.badge import Badge
from pyaidoc.html.section import Section
from pyaidoc.html.style import Style
from pyaidoc.html.document import Document
from pyaidoc.parameter import Parameter
from pyaidoc.tool import Tool
from pyaidoc.tools import Tools
import inspect


def calculate_mortgage(amount: float, interest_rate: float = 3.5) -> dict:
    """Berechnet die monatliche Kreditrate für eine Immobilie."""
    return {}


def ping() -> str:
    """Einfacher Statuscheck."""
    return "pong"


def test_page_renders_tools() -> None:
    tools = Tools(calculate_mortgage, ping)
    page = Page(tools)
    html_output = page.html()

    assert "<!DOCTYPE html>" in html_output
    assert "<title>AI Agent Tools &amp; Function Calls</title>" in html_output
    assert "calculate_mortgage" in html_output
    assert "Berechnet die monatliche Kreditrate für eine Immobilie." in html_output
    assert "amount" in html_output
    assert "float" in html_output
    assert "Erforderlich" in html_output
    assert "interest_rate" in html_output
    assert "3.5" in html_output
    assert "Optional" in html_output
    assert "ping" in html_output
    assert "Keine Parameter erforderlich." in html_output


def test_card_individual_render() -> None:
    card = Card(Tool(ping))
    html_output = card.html()
    assert "ping" in html_output
    assert "Einfacher Statuscheck." in html_output
    assert "Keine Parameter erforderlich." in html_output


def test_badge_rendering() -> None:
    sig = inspect.signature(calculate_mortgage)
    req_param = Parameter(sig.parameters["amount"])
    opt_param = Parameter(sig.parameters["interest_rate"])

    assert "Erforderlich" in Badge(req_param).html()
    assert "req" in str(Badge(req_param))
    assert "Optional" in Badge(opt_param).html()
    assert "opt" in str(Badge(opt_param))


def test_page_empty_state() -> None:
    page = Page(Tools())
    section = page.section_html()
    assert "Keine AI-Tools registriert." in section


def test_page_str_conversion() -> None:
    page = Page(Tools(ping))
    assert str(page) == page.html()


def test_card_str_conversion() -> None:
    card = Card(Tool(ping))
    assert str(card) == card.html()


def test_section_and_style_autonomous_render() -> None:
    style = Style()
    assert ":root" in str(style)
    section = Section(Tools(ping), "My Tools")
    assert "My Tools" in str(section)


def test_document_autonomous_render() -> None:
    doc = Document("Test Page", "<p>Hello</p>")
    assert "<title>Test Page</title>" in str(doc)
    assert "<p>Hello</p>" in str(doc)
    assert "<!DOCTYPE html>" in str(doc)


def test_page_custom_title() -> None:
    page = Page(Tools(ping), "Custom Tools Title")
    assert page.title() == "Custom Tools Title"
    assert "<title>Custom Tools Title</title>" in page.html()

