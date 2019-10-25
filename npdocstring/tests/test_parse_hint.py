from ..npdocstring import get_funclassdef_nodes, get_function_arguments


def test_parse_nested_hint():
    file_content = open("npdocstring/tests/samples/in/hints.py").read()
    fcnodes = get_funclassdef_nodes(file_content)
    assert len(fcnodes) == 4
    args = get_function_arguments(fcnodes[0])
    assert len(args) == 1
    assert args[0].hint == "list of list of int"


def test_parse_union_hint():
    file_content = open("npdocstring/tests/samples/in/hints.py").read()
    fcnodes = get_funclassdef_nodes(file_content)
    assert len(fcnodes) == 4
    args = get_function_arguments(fcnodes[1])
    assert len(args) == 1
    assert args[0].hint == "list of int or str"


def test_parse_complex_hint():
    file_content = open("npdocstring/tests/samples/in/hints.py").read()
    fcnodes = get_funclassdef_nodes(file_content)
    assert len(fcnodes) == 4
    args = get_function_arguments(fcnodes[2])
    assert len(args) == 1
    assert args[0].hint == "list of list of int or str"


def test_parse_union_hint():
    file_content = open("npdocstring/tests/samples/in/hints.py").read()
    fcnodes = get_funclassdef_nodes(file_content)
    assert len(fcnodes) == 4
    args = get_function_arguments(fcnodes[3])
    assert len(args) == 1
    assert args[0].hint == "int or iterable of int"
