import sys
from pathlib import Path

# Ensure repo root is on PYTHONPATH so tests can import aes_socket_utils.py
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
