"""Pytest configuration and path setup.

Ensures the project root is on sys.path so tests can import lambda_function
when run as 'pytest tests/' (e.g. in CI). Without this, the test module is
loaded from tests/ and the repo root is not on the path.
"""
from pathlib import Path
import sys

# Add repo root so "from lambda_function import ..."
# works when tests live in tests/
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))
