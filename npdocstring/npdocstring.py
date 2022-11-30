#!/usr/bin/env python3
import ast
from ast import AsyncFunctionDef, ClassDef, FunctionDef
from collections import namedtuple

AtrOrArg = namedtuple("AtrOrArg", ["name", "hint", "default"])


def measure_indentation(file_content: str) -> list[int]:
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


def get_funclassdef_nodes(file_content) -> list[ast.AST]:
    root = ast.parse(file_content)
    fcnodes: list[ast.AST] = []
    for node in ast.iter_child_nodes(root):
        if isinstance(node, (FunctionDef, AsyncFunctionDef, ClassDef)):
            if (
                node.name.startswith("__") and node.name.endswith("__")
            ) or node.name.startswith("test_"):
                continue
            if ast.get_docstring(node) is None:
                fcnodes.append(node)
            if isinstance(node, ClassDef):
                for sub_node in ast.iter_child_nodes(node):
                    if isinstance(sub_node, (FunctionDef, AsyncFunctionDef)):
                        if sub_node.name.startswith(
                            "__"
                        ) and sub_node.name.endswith("__"):
                            continue
                        if ast.get_docstring(sub_node) is None:
                            fcnodes.append(sub_node)
    return fcnodes


def get_subscript(node: ast.Subscript) -> str:
    if isinstance(node.value, ast.Name):
        return node.value.id
    elif isinstance(node.value, ast.Attribute):
        return node.value.attr
    return "FIXME"


def parse_subscript_elt_hint(node: ast.AST, i: int) -> str:
    assert hasattr(node, "slice")
    assert hasattr(node.slice, "elts")
    elt_hint = parse_hint(node.slice.elts[i])
    if elt_hint is None:
        raise RuntimeError(
            "Could not parse subscript element. Subscript was: {}. Element was: {}".format(
                ast.dump(node),
                ast.dump(node.slice.elts[i]),
            )
        )
    return elt_hint


def parse_hint(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Subscript):
        if hasattr(node, "slice"):
            if get_subscript(node) == "Union" and hasattr(node.slice, "elts"):
                elt_hints = [
                    parse_subscript_elt_hint(node, i)
                    for i in range(len(node.slice.elts))
                ]
                return " or ".join(elt_hints)
            elif get_subscript(node).lower() in {"list", "iterable"}:
                lowered = get_subscript(node).lower()
                if node.slice is None:
                    return lowered
                return "{} of {}".format(lowered, parse_hint(node.slice))
            elif get_subscript(node) == "Tuple":
                if isinstance(node.slice, ast.Tuple):
                    if (
                        not hasattr(node.slice, "elts")
                        or len(node.slice.elts) == 0
                    ):
                        return "tuple"
                    elif (
                        hasattr(node.slice, "elts")
                        and len(node.slice.elts) == 1
                    ):
                        elt_hint = parse_subscript_elt_hint(node, 0)
                        return "tuple of " + elt_hint
                    elif hasattr(node.slice, "elts"):
                        elt_hints = [
                            parse_subscript_elt_hint(node, i)
                            for i in range(len(node.slice.elts))
                        ]
                        return "({})".format(", ".join(elt_hints))
                return "FIXME"
            else:
                return "FIXME"
        else:
            return "FIXME"
    elif isinstance(node, ast.Attribute):
        toconcat = list()
        n: ast.Attribute | ast.Name = node
        while not isinstance(n, ast.Name):
            assert isinstance(n, ast.Attribute)
            toconcat.append(n.attr)
            assert isinstance(n.value, (ast.Attribute, ast.Name))
            n = n.value
        assert isinstance(n, ast.Name)
        toconcat.append(n.id)
        return ".".join(reversed(toconcat))
    elif isinstance(node, (ast.Constant, ast.NameConstant)):
        return str(node.value)
    elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        left_hint = parse_hint(node.left)
        right_hint = parse_hint(node.right)
        assert isinstance(left_hint, str)
        assert isinstance(right_hint, str)
        return left_hint + " or " + right_hint
    else:
        raise Exception("parse_hint: {}".format(ast.dump(node)))


def parse_return_hint(node: FunctionDef | AsyncFunctionDef) -> str | None:
    if node.returns is None:
        return None
    elif type(node.returns) is ast.NameConstant:
        return "None"
    else:
        return parse_hint(node.returns)


def node_to_str(node: ast.AST) -> str:
    if isinstance(node, (ast.NameConstant, ast.Constant)):
        return repr(node.value)
    elif isinstance(node, ast.Num):
        return str(node.n)
    elif isinstance(node, (ast.List, ast.Tuple)) and hasattr(node, "elts"):
        string = "[" if isinstance(node, ast.List) else "("
        if len(node.elts) > 0:
            for i in range(len(node.elts) - 1):
                string += node_to_str(node.elts[i]) + ", "
            string += node_to_str(node.elts[-1])
        string += "]" if isinstance(node, ast.List) else ")"
        return string
    elif isinstance(node, ast.Str):
        return repr(node.s)
    elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        return node.value.id + "." + node.attr
    else:
        return "FIXME"


def get_function_arguments(
    node: FunctionDef | AsyncFunctionDef,
) -> list[AtrOrArg]:
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


def make_atrorarg_string(args: list[AtrOrArg], section_name: str) -> str:
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


def make_parameters_string(args: list[AtrOrArg]) -> str:
    return make_atrorarg_string(args, "Parameters")


def make_attributes_string(args: list[AtrOrArg]) -> str:
    return make_atrorarg_string(args, "Attributes")


def generate_function_docstring(node: FunctionDef | AsyncFunctionDef) -> str:
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


def get_class_constructor(cnode: ClassDef) -> FunctionDef | None:
    constructor = None
    for node in cnode.body:
        if isinstance(node, FunctionDef) and node.name == "__init__":
            constructor = node
            break
    return constructor


def get_class_attributes(constructor: FunctionDef) -> list[AtrOrArg]:
    attributes = []
    for node in constructor.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Attribute):
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
    node: FunctionDef | AsyncFunctionDef | ClassDef,
    indentation: list[int],
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
    docstrings: list[str],
    file_content: str,
    indentation: list[int],
    fcnodes: list[ast.AST],
    indentation_spaces: int,
) -> str:
    processed = ""
    lines = file_content.splitlines(keepends=True)
    splits = []
    for node in fcnodes:
        assert isinstance(node, (FunctionDef, AsyncFunctionDef, ClassDef))
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


def process_file(file_content: str, indentation_spaces: int = 4):
    indentation = measure_indentation(file_content)
    fcnodes = get_funclassdef_nodes(file_content)
    docstrings = []
    for node in fcnodes:
        if isinstance(node, (FunctionDef, AsyncFunctionDef)):
            docstrings.append(generate_function_docstring(node))
        elif isinstance(node, ClassDef):
            docstrings.append(generate_class_docstring(node))
    new_file_content = integrate_docstrings(
        docstrings, file_content, indentation, fcnodes, indentation_spaces
    )
    return new_file_content
