"""
Test: Offline guard blocks outbound network connections.

Why: Ensures Rule #1 (Strictly Offline) is actually enforced at runtime, not just by policy documentation.
Where: Uses `utils.offline_guard.enable()` then attempts to open an external socket (e.g., to example.com) which should fail.
How: Patch socket to enforce blocking (implemented by offline_guard). We try a simple connection; success would mean a failure of enforcement. The test asserts an exception is raised.

Connects to:
    - utils/offline_guard.py: The enforcement logic hooking socket / requests
    - app.py: Calls offline_guard.enable() during startup
"""
from __future__ import annotations

import socket
import pytest

# Import inside test to avoid side effects before enabling
from utils import offline_guard  # type: ignore


def test_offline_guard_blocks_external_connection():
    """
    Validate that after enabling offline guard, outbound connections are blocked.

    Why: Runtime validation of security boundary (no external network IO allowed).
    Where: Relies on offline_guard monkey-patching the socket module's connect.
    How: Enable guard, attempt to connect to a known external host. Expect OSError/RuntimeError.

    Connects to:
        - utils/offline_guard.py: enforced patch
        - test suite policy layer (ensures offline regression detection)
    """
    offline_guard.enable()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        with pytest.raises(Exception):  # broad: implementation may raise various error types
            s.settimeout(1)
            s.connect(("93.184.216.34", 80))  # example.com public IP
    finally:
        s.close()
