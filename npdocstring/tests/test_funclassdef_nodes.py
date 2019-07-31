from ..npdocstring import get_funclassdef_nodes


def test_get_funclassdef_nodes():

  file_content = open('npdocstring/tests/samples/in/basic.py').read()
  fcnodes = get_funclassdef_nodes(file_content)
  assert len(fcnodes) == 4
  assert fcnodes[0].name == 'basic_function'
  assert fcnodes[1].name == 'BasicClass'
  assert fcnodes[2].name == 'basic_method'
  assert fcnodes[3].name == 'basic_async_method'
