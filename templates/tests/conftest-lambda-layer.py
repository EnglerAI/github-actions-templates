"""Pytest configuration and path setup.

Ensures the project root and python/ are on sys.path so tests can import
layer_testing_utils when run as 'pytest tests/' (e.g. in CI). The package
lives at python/layer_testing_utils.py, so python/ must be on the path.
"""
from pathlib import Path
import sys

_repo_root = Path(__file__).resolve().parent.parent
_python_dir = _repo_root / "python"

# Add python/ first so "from layer_testing_utils import ..." resolves to python/layer_testing_utils.py
if str(_python_dir) not in sys.path:
    sys.path.insert(0, str(_python_dir))
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))
