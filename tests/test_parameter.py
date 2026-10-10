import inspect
from pyaidoc.default import NoDefault, PresentDefault
from pyaidoc.parameter import Parameter
from pyaidoc.type_name import TypeName


def sample_function(name: str, count: int = 1, flag: bool = False, untyped=None) -> None:
    pass


def test_parameter_name_and_type() -> None:
    sig = inspect.signature(sample_function)
    param = Parameter(sig.parameters["name"])
    assert param.name() == "name"
    assert param.type() == "str"
    assert param.required() is True
    assert param.default().present() is False
    assert param.default().text() == "—"
    assert str(param) == "name: str"


def test_parameter_with_default() -> None:
    sig = inspect.signature(sample_function)
    param = Parameter(sig.parameters["count"])
    assert param.name() == "count"
    assert param.type() == "int"
    assert param.required() is False
    assert param.default().present() is True
    assert param.default().text() == "1"


def test_parameter_untyped() -> None:
    sig = inspect.signature(sample_function)
    param = Parameter(sig.parameters["untyped"])
    assert param.name() == "untyped"
    assert param.type() == "Any"
    assert param.required() is False
    assert param.default().present() is True
    assert param.default().text() == "None"


def test_type_name_formatting() -> None:
    assert TypeName(inspect._empty).text() == "Any"
    assert TypeName(str).text() == "str"
    assert str(TypeName(int)) == "int"
    assert TypeName(list[int]).text() == "list[int]"
    import typing
    assert TypeName(typing.List[str]).text() == "List[str]"


def test_default_html_rendering() -> None:
    assert NoDefault().html() == '<span class="pyaidoc-empty">—</span>'
    assert PresentDefault(42).html() == "<code>42</code>"
    assert PresentDefault("hello").html() == '<code>&quot;hello&quot;</code>'


def test_ternary_resolution() -> None:
    from pyaidoc.ternary import Ternary

    assert Ternary(True, "consequent", "alternative").value() == "consequent"
    assert Ternary(False, "consequent", "alternative").value() == "alternative"
    assert str(Ternary(True, 123, 456)) == "123"
