"""Tests for OpenAiSchema and Tool decorator in Pure OOP."""

from typing import Literal
import pytest
from pyaidoc import Tool, tool, OpenAiSchema, OpenAiTools


@tool
def fill_template(
    template_type: Literal["alleinauftrag", "suchauftrag"],
    customer_name: str,
    commission_rate: float = 3.57,
) -> dict:
    """Befüllt eine Vertragsvorlage mit Kundendaten.

    :param template_type: Die Art des Vertrags (Alleinauftrag oder Suchauftrag)
    :param customer_name: Vollständiger Name des Kunden
    :param commission_rate: Provisionssatz in Prozent
    """
    return {
        "template": template_type,
        "customer": customer_name,
        "commission": commission_rate,
    }


def test_tool_decorator_attributes_and_execution() -> None:
    import asyncio

    assert fill_template.name() == "fill_template"
    assert "Befüllt eine Vertragsvorlage" in fill_template.description()

    # Direct execution via call and execute
    res1 = fill_template("alleinauftrag", "Max Mustermann")
    assert res1["customer"] == "Max Mustermann"
    assert res1["commission"] == 3.57

    res2 = asyncio.run(fill_template.execute("suchauftrag", "Erika Musterfrau", commission_rate=4.0))
    assert res2["customer"] == "Erika Musterfrau"
    assert res2["commission"] == 4.0


def test_openai_schema_generation() -> None:
    schema = fill_template.schema()
    assert schema["type"] == "function"
    fn = schema["function"]
    assert fn["name"] == "fill_template"
    assert "Befüllt eine Vertragsvorlage" in fn["description"]

    params = fn["parameters"]
    assert params["type"] == "object"
    assert params["required"] == ["template_type", "customer_name"]

    props = params["properties"]
    assert props["template_type"]["type"] == "string"
    assert props["template_type"]["enum"] == ["alleinauftrag", "suchauftrag"]
    assert "Art des Vertrags" in props["template_type"]["description"]

    assert props["customer_name"]["type"] == "string"
    assert "Name des Kunden" in props["customer_name"]["description"]

    assert props["commission_rate"]["type"] == "number"
    assert props["commission_rate"]["default"] == 3.57


def test_pure_oop_tool_wrapper() -> None:
    def create_lead(title: str, budget: int = 500000) -> str:
        """Erstellt einen Lead."""
        return f"Lead {title}: {budget}"

    wrapped = Tool(create_lead, name="lead_create")
    assert wrapped.name() == "lead_create"
    schema = OpenAiSchema(wrapped).value()
    assert schema["function"]["name"] == "lead_create"
    assert "budget" in schema["function"]["parameters"]["properties"]
    assert schema["function"]["parameters"]["properties"]["budget"]["type"] == "integer"


def test_openai_tools_collection() -> None:
    tools_list = OpenAiTools([fill_template]).list()
    assert len(tools_list) == 1
    assert tools_list[0]["function"]["name"] == "fill_template"


def test_capability_object_adaptation_and_invoke() -> None:
    import asyncio

    class ContactUpsert:
        """Erfasst oder aktualisiert Kontakte im CRM."""

        def name(self) -> str:
            return "contact_upsert"

        async def execute(self, name: str, phone: str = "", email: str = "") -> dict:
            """Erfasst einen Kontakt.

            :param name: Vollständiger Name
            :param phone: Telefonnummer
            :param email: E-Mail-Adresse
            """
            return {"saved": True, "name": name, "phone": phone, "email": email}

    cap_tool = Tool(ContactUpsert())
    assert cap_tool.name() == "contact_upsert"
    schema = cap_tool.schema()
    assert schema["function"]["name"] == "contact_upsert"
    assert "name" in schema["function"]["parameters"]["required"]

    # Test direct async execute
    res1 = asyncio.run(cap_tool.execute(name="Klaus Meyer", phone="0171 123456"))
    assert res1["saved"] is True
    assert res1["name"] == "Klaus Meyer"

    # Test invoke with JSON string from LLM
    json_payload = '{"name": "Erika Muster", "email": "erika@example.com"}'
    res2 = asyncio.run(cap_tool.invoke(json_payload))
    assert res2["saved"] is True
    assert res2["name"] == "Erika Muster"
    assert res2["email"] == "erika@example.com"


def test_optional_and_array_schema() -> None:
    from typing import Optional, List

    class PropertyFilter:
        def execute(
            self,
            location: str,
            min_rooms: Optional[int] = None,
            max_price: Optional[float] = None,
            tags: Optional[List[str]] = None,
        ) -> str:
            """Filtert Immobilien.

            :param location: Stadt oder PLZ
            :param min_rooms: Mindestanzahl Zimmer
            :param max_price: Höchstpreis
            :param tags: Such-Tags
            """
            return "filtered"

    tool_obj = Tool(PropertyFilter())
    props = tool_obj.schema()["function"]["parameters"]["properties"]
    assert props["location"]["type"] == "string"
    assert props["min_rooms"]["type"] == "integer"
    assert props["max_price"]["type"] == "number"
    assert props["tags"]["type"] == "array"
    assert props["tags"]["items"]["type"] == "string"

