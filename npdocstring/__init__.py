"""Generate missing NumPy docstrings in your code, leveraging type hints."""
from .__about__ import __version__
from .npdocstring import process_file

__all__ = [
    "__version__",
    "process_file",
]
