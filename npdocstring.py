import sys
import ast
from collections import namedtuple
from ast import FunctionDef, AsyncFunctionDef, ClassDef
from typing import List, Union


def measure_indentation(file_content: str) -> List[int]:

  lines = file_content.splitlines()
  indentation = [0 for i in range(len(lines))]

  for i, line in enumerate(lines):
    if len(line) == 0:
      indentation[i] = 0
    else:
      j = 0
      while line[j] == ' ':
        j += 1
      indentation[i] = j

  return indentation


def get_funclassdef_nodes(file_content) -> List[ast.AST]:

  root = ast.parse(file_content)
  fcnodes = []

  for node in ast.iter_child_nodes(root):
    if type(node) in [FunctionDef, AsyncFunctionDef, ClassDef]:
      if ast.get_docstring(node) is None: fcnodes.append(node)
      if type(node) == ClassDef:
        for sub_node in ast.iter_child_nodes(node):
          if type(sub_node) in [FunctionDef, AsyncFunctionDef]:
            if ast.get_docstring(sub_node) is None: fcnodes.append(sub_node)

  return fcnodes


def parse_hint(node: ast.AST) -> Union[str, None]:

  if node is None:
    hint = None
  elif type(node) == ast.Name:
    hint = node.id
  elif type(node) == ast.Subscript:
    if node.value.id == 'Union':
      hint = ''
      for i in range(len(node.slice.value.elts) - 1):
        hint += parse_hint(node.slice.value.elts[i]) + ' or '
      hint += parse_hint(node.slice.value.elts[-1])
    elif node.value.id == 'List':
      hint = '{} of {}'.format(
        node.value.id.lower(), parse_hint(node.slice.value)
      )

  return hint


Argument = namedtuple('Argument', ['name', 'hint', 'default'])


def get_function_arguments(
  node: Union[FunctionDef, AsyncFunctionDef]
) -> List[Argument]:

  arguments = []

  n_args = len(node.args.args)
  n_defaults = len(node.args.defaults)

  for i, arg in enumerate(node.args.args):
    if arg.arg == 'self': continue
    hint = parse_hint(arg.annotation)
    if i >= n_args - n_defaults:
      default_node = node.args.defaults[n_args - n_defaults - i]
      if type(default_node) is ast.NameConstant:
        default = 'None'
      else:
        default = default_node.s
    else:
      default = None
    arguments.append(Argument(arg.arg, hint, default))

  return arguments


def generate_function_docstring(
  node: Union[FunctionDef, AsyncFunctionDef]
) -> str:

  args = get_function_arguments(node)

  if node.returns is None:
    returns = None
  elif type(node.returns) is ast.NameConstant:
    returns = 'None'
  else:
    returns = parse_hint(node.returns)

  docstring = '\'\'\'\n\n'

  if len(args) > 0:
    docstring += 'Parameters\n----------\n'
    for arg in args:
      docstring += arg.name
      if arg.hint is not None:
        docstring += ' : {}'.format(arg.hint)
        if arg.default is not None:
          docstring += ', optional (default={})'.format(repr(arg.default))
        docstring += '\n  FIXME\n\n'

  if returns is not None:
    docstring += 'Returns\n-------\n'
    docstring += returns + '\n'
    docstring += '  FIXME\n\n'

  docstring += '\'\'\''

  return docstring


def generate_class_docstring(node: ClassDef) -> str:

  return ''


def integrate_docstrings(
  docstrings: List[str], file_content: str, indentation: List[int]
) -> str:

  return ''


def process_file(file_content: str):

  indentation = measure_indentation(file_content)
  fcnodes = get_funclassdef_nodes(file_content)

  docstrings = []
  for node in fcnodes:
    if type(node) in [FunctionDef, AsyncFunctionDef]:
      docstrings.append(generate_function_docstring(node))
    elif type(node) is ClassDef:
      docstrings.append(generate_class_docstring(node))

  new_file_content = integrate_docstrings(
    docstrings, file_content, indentation
  )

  sys.stdout.write(new_file_content)


if __name__ == '__main__':

  file_content = sys.stdin.read()
  process_file(file_content)
