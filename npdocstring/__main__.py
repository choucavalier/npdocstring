import argparse
import os
import sys

import npdocstring

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="npdocstring",
        description=(
            "generate missing numpy docstrings automatically "
            "in Python source files."
        ),
    )
    parser.add_argument("file_path", help="Path to the file to process")
    parser.add_argument(
        "--dir", "-d", help="directory where to apply recursively."
    )
    parser.add_argument(
        "--indentation-spaces",
        help="how many indentation spaces are used",
        default=4,
        type=int,
    )
    flags = parser.parse_args()
    if flags.dir is None:
        file_content = sys.stdin.read()
        new_file_content = npdocstring.process_file(
            file_content, flags.indentation_spaces
        )
        sys.stdout.write(new_file_content)
    else:
        if not os.path.isdir(flags.dir):
            print("npdocstring: unknown directory", flags.dir)
        else:
            for root, dirs, files in os.walk(flags.dir):
                for file in files:
                    if file.endswith(".py"):
                        path = os.path.join(*([root] + dirs + [file]))
                        file_content = open(path).read()
                        new_file_content = npdocstring.process_file(
                            file_content, flags.indentation_spaces
                        )
                        with open(path + "--", "w") as f:
                            f.write(file_content)
                        with open(path, "w") as f:
                            f.write(new_file_content)
                        print(f"processed {path}")
