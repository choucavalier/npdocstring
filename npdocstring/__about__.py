from importlib import metadata

try:
    __version__ = metadata.version("npdocstring")
except Exception:
    __version__ = "unknown"
