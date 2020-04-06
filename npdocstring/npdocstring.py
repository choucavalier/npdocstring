#!/usr/bin/env python3
import ast
import sys
from ast import AsyncFunctionDef, ClassDef, FunctionDef
from collections import namedtuple
from typing import List, Tuple, Union

AtrOrArg = namedtuple("AtrOrArg", ["name", "hint", "default"])


def measure_indentation(file_content: str) -> List[int]:
    lines = file_content.splitlines()
    indentation = [0 for i in range(len(lines))]
    for i, line in enumerate(lines):
        if len(line) == 0:
            indentation[i] = 0
        else:
            j = 0
            while j < len(line) and line[j] == " ":
                j += 1
            indentation[i] = j
    return indentation


def get_funclassdef_nodes(file_content) -> List[ast.AST]:
    root = ast.parse(file_content)
    fcnodes = []
    for node in ast.iter_child_nodes(root):
        if type(node) in [FunctionDef, AsyncFunctionDef, ClassDef]:
            if (
                node.name.startswith("__") and node.name.endswith("__")
            ) or node.name.startswith("test_"):
                continue
            if ast.get_docstring(node) is None:
                fcnodes.append(node)
            if type(node) is ClassDef:
                for sub_node in ast.iter_child_nodes(node):
                    if type(sub_node) in [FunctionDef, AsyncFunctionDef]:
                        if sub_node.name.startswith(
                            "__"
                        ) and sub_node.name.endswith("__"):
                            continue
                        if ast.get_docstring(sub_node) is None:
                            fcnodes.append(sub_node)
    return fcnodes


def parse_hint(node: ast.AST) -> Union[str, None]:
    if node is None:
        return None
    elif type(node) is ast.Name:
        return node.id
    elif type(node) is ast.Subscript:
        if node.value.id == "Union":
            hint = ""
            for i in range(len(node.slice.value.elts) - 1):
                hint += parse_hint(node.slice.value.elts[i]) + " or "
            hint += parse_hint(node.slice.value.elts[-1])
            return hint
        elif node.value.id in {"List", "Iterable"}:
            lowered = node.value.id.lower()
            if node.slice.value is None:
                return lowered
            return "{} of {}".format(lowered, parse_hint(node.slice.value))
        elif node.value.id == "Tuple":
            if type(node.slice.value) is ast.Tuple:
                if len(node.slice.value.elts) == 0:
                    return "tuple"
                elif len(node.slice.value.elts) == 1:
                    return "tuple of " + parse_hint(node.slice.value.elts[0])
                else:
                    hint = "("
                    for i in range(len(node.slice.value.elts) - 1):
                        hint += parse_hint(node.slice.value.elts[i]) + ", "
                    hint += parse_hint(node.slice.value.elts[-1]) + ")"
                    return hint
        else:
            return "FIXME"
    elif type(node) is ast.Attribute:
        return "{}.{}".format(node.value.id, node.attr)
    elif type(node) is ast.NameConstant:
        return str(node.value)
    else:
        raise Exception("parse_hint: {}".format(ast.dump(node)))


def parse_return_hint(node: Union[FunctionDef, AsyncFunctionDef]) -> str:
    if node.returns is None:
        return None
    elif type(node.returns) is ast.NameConstant:
        return "None"
    else:
        return parse_hint(node.returns)


def node_to_str(node: ast.AST) -> str:
    if type(node) is ast.NameConstant:
        return repr(node.value)
    elif type(node) is ast.Num:
        return node.n
    elif type(node) in [ast.List, ast.Tuple]:
        string = "[" if type(node) is ast.List else "("
        if len(node.elts) > 0:
            for i in range(len(node.elts) - 1):
                string += node_to_str(node.elts[i]) + ", "
            string += node_to_str(node.elts[-1])
        string += "]" if type(node) is ast.List else ")"
        return string
    elif type(node) is ast.Str:
        return repr(node.s)
    elif type(node) is ast.Attribute:
        return node.value.id + "." + node.attr
    else:
        return "FIXME"


def get_function_arguments(
    node: Union[FunctionDef, AsyncFunctionDef]
) -> List[AtrOrArg]:
    arguments = []
    n_args = len(node.args.args)
    n_defaults = len(node.args.defaults)
    for i, arg in enumerate(node.args.args):
        if arg.arg in {"self", "cls"}:
            continue
        hint = parse_hint(arg.annotation)
        if i >= n_args - n_defaults:
            default = node_to_str(node.args.defaults[n_args - n_defaults - i])
        else:
            default = None
        arguments.append(AtrOrArg(arg.arg, hint, default))
    return arguments


def make_atrorarg_string(args: List[AtrOrArg], section_name: str) -> str:
    string = ""
    if len(args) > 0:
        string += "{}\n{}\n".format(section_name, "-" * len(section_name))
        for arg in args:
            string += arg.name
            if arg.hint is not None:
                string += " : {}".format(arg.hint)
                if arg.default is not None:
                    string += ", optional (default={})".format(arg.default)
            else:
                string += " : FIXME"
            string += "\n    FIXME\n\n"
    return string


def make_parameters_string(args: List[AtrOrArg]) -> str:
    return make_atrorarg_string(args, "Parameters")


def make_attributes_string(args: List[AtrOrArg]) -> str:
    return make_atrorarg_string(args, "Attributes")


def generate_function_docstring(
    node: Union[FunctionDef, AsyncFunctionDef]
) -> str:
    docstring = '"""\nFIXME'
    arguments = get_function_arguments(node)
    if len(arguments):
        docstring += "\n\n"
        docstring += make_parameters_string(arguments)
    returns = parse_return_hint(node)
    if returns is not None:
        docstring += "Returns\n-------\n"
        docstring += returns + "\n"
        docstring += "    FIXME\n\n"
    docstring += '"""\n'
    return docstring


def get_class_constructor(cnode: ClassDef) -> FunctionDef:
    constructor = None
    for node in cnode.body:
        if type(node) is FunctionDef and node.name == "__init__":
            constructor = node
            break
    return constructor


def get_class_attributes(constructor: FunctionDef) -> List[AtrOrArg]:
    attributes = []
    for node in constructor.body:
        if type(node) is ast.Assign:
            for target in node.targets:
                if type(target) is ast.Attribute:
                    attributes.append(
                        AtrOrArg(name=target.attr, hint=None, default=None)
                    )
    return attributes


def generate_class_docstring(cnode: ClassDef) -> str:
    docstring = '"""\nFIXME'
    constructor = get_class_constructor(cnode)
    if constructor is not None:
        arguments = get_function_arguments(constructor)
        arg_names = [arg.name for arg in arguments]
        attributes = get_class_attributes(constructor)
        attributes = [
            attr for attr in attributes if attr.name not in arg_names
        ]
        if len(arguments) > 0 or len(attributes) > 0:
            docstring += "\n\n"
            docstring += make_parameters_string(arguments)
            docstring += make_attributes_string(attributes)
    docstring += '"""\n'
    return docstring


def pad_docstring(docstring: str, pad: str) -> str:
    lines = docstring.splitlines(keepends=True)
    for i in range(len(lines)):
        if len(lines[i]) > 1:
            lines[i] = pad + lines[i]
    return "".join(lines)


def get_fcnode_last_lineno(
    node: Union[FunctionDef, AsyncFunctionDef, ClassDef],
    indentation: List[int],
    indentation_spaces: int,
) -> int:
    lineno = node.body[0].lineno - 1
    while (
        indentation[lineno] == node.lineno + indentation_spaces
        or indentation[lineno] == 0
    ):
        lineno -= 1
    return lineno


def integrate_docstrings(
    docstrings: List[Tuple[ast.AST, str]],
    file_content: str,
    indentation: List[int],
    fcnodes: List[ast.AST],
    indentation_spaces: int,
) -> str:
    processed = ""
    lines = file_content.splitlines(keepends=True)
    splits = []
    for node in fcnodes:
        splits.append(
            get_fcnode_last_lineno(node, indentation, indentation_spaces)
        )
    for i, split in enumerate(splits):
        start_line = 0 if i < 1 else splits[i - 1]
        processed += "".join(lines[start_line:split])
        pad = " " * (indentation[fcnodes[i].lineno - 1] + indentation_spaces)
        processed += pad_docstring(docstrings[i], pad)
    processed += "".join(lines[splits[-1] :])
    return processed


def process_file(file_content: str, indentation_spaces: int):
    indentation = measure_indentation(file_content)
    fcnodes = get_funclassdef_nodes(file_content)
    docstrings = []
    for node in fcnodes:
        if type(node) in [FunctionDef, AsyncFunctionDef]:
            docstrings.append(generate_function_docstring(node))
        elif type(node) is ClassDef:
            docstrings.append(generate_class_docstring(node))
    new_file_content = integrate_docstrings(
        docstrings, file_content, indentation, fcnodes, indentation_spaces
    )
    return new_file_content
