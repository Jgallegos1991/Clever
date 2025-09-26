"""
offline_guard.py - Offline Guard Utility for Clever's Digital Sovereignty System

Why: Enforces strict offline operation by blocking all outbound network connections except loopback, ensuring compliance with Clever's digital sovereignty principles and maintaining complete local control of the cognitive partnership system.

Where: Used by app.py and system_validator.py to guarantee offline-only operation for all Clever AI components. Critical component of Clever's digital sovereignty architecture ensuring total privacy and control.

How: Monkey-patches socket.socket to raise errors on non-loopback connections, provides enable/disable toggles, and utility checks for network references in text.

File Usage:
    - Digital sovereignty: Primary enforcement mechanism for offline-only operation
    - Network isolation: Ensures no external network calls compromise privacy or control
    - System startup: Activated during app.py initialization to enforce offline mode
    - Input validation: Validates user input for network references to prevent external calls
    - Testing framework: Used by validation systems to test offline compliance
    - Security enforcement: Prevents accidental network leaks or external dependencies
    - Privacy protection: Ensures all cognitive partnership data stays local
    - Development safety: Protects against inadvertent external service calls during development

Connects to:
    - app.py: Core application integration for startup offline enforcement
        - `enable()` called at startup to enforce offline mode
        - `contains_network_reference()` used to validate user input against network terms
    - system_validator.py: System validation and testing integration
        - `enable()`, `disable()`, and `is_enabled()` used to test offline guard functionality
    - config.py: Configuration system integration for offline mode settings
    - evolution_engine.py: Learning system ensuring all data processing stays local
    - persona.py: Personality engine operating entirely offline for privacy
    - database.py: Local data persistence without external dependencies
    - nlp_processor.py: Natural language processing using only local models
    - .github/copilot-instructions.md: Digital sovereignty principles this utility enforces
    - SECURITY.md: Security policy supported by offline operation enforcement
"""

import socket
from typing import Tuple

_ENABLED = False
_orig_socket = socket.socket


def _is_loopback(addr: Tuple[str, int]) -> bool:
    """
    Check if the given address is a loopback address (localhost/127.0.0.1)
    
    Why: Ensures only local connections are allowed when offline guard is enabled
    Where: Used by _GuardedSocket to validate outbound connections
    How: Checks host string for loopback patterns and reserved names
    """
    host = addr[0]
    if host.startswith("127."):
        return True
    if host in {"localhost", "::1"}:
        return True
    return False

    # ...existing code...
    host = addr[0]
    if host.startswith("127."):
        return True
    if host in {"localhost", "::1"}:
        return True
    return False


class _GuardedSocket(socket.socket):
    """
    Custom socket class that blocks outbound connections except loopback
    
    Why: Enforces offline-only operation by raising errors on non-local connections
    Where: Used to monkey-patch socket.socket when offline guard is enabled
    How: Overrides connect/connect_ex to check address and block as needed
    """
    def connect(self, address):  # type: ignore[override]
        if not _is_loopback(address):
            raise PermissionError(f"Outbound network blocked to {address}")
        return super().connect(address)

    def connect_ex(self, address):  # type: ignore[override]
        if not _is_loopback(address):
            return 111  # ECONNREFUSED-like
        return super().connect_ex(address)


def enable() -> None:
    """
    Enable offline guard by monkey-patching socket.socket
    
    Why: Activates strict offline mode for Clever AI
    Where: Called at app startup and by system_validator
    How: Replaces socket.socket with _GuardedSocket, sets enabled flag
    """
    global _ENABLED
    if _ENABLED:
        return
    socket.socket = _GuardedSocket  # type: ignore[assignment]
    _ENABLED = True


def disable() -> None:
    """
    Disable offline guard and restore original socket behavior
    
    Why: Allows temporary re-enabling of network for debugging/maintenance
    Where: Used by developers or system scripts as needed
    How: Restores original socket.socket, clears enabled flag
    """
    global _ENABLED
    if not _ENABLED:
        return
    socket.socket = _orig_socket  # type: ignore[assignment]
    _ENABLED = False


def is_enabled() -> bool:
    """
    Check if offline guard is currently enabled
    
    Why: Provides status for system validation and debugging
    Where: Used by app.py, system_validator.py, and health checks
    How: Returns internal enabled flag
    """
    return _ENABLED


def contains_network_reference(text: str) -> bool:
    """
    Check if text contains network/internet references that should be blocked
    
    Why: Detects user input or code that may attempt external network access
    Where: Used by app.py to block requests referencing internet resources
    How: Scans text for common network keywords and patterns
    """
    network_terms = [
        "http://",
        "https://",
        "www.",
        ".com",
        ".org",
        ".net",
        "fetch(",
        "axios",
        "request",
        "download",
        "upload",
        "api.",
        "endpoint",
        "curl",
        "wget",
    ]
    text_lower = text.lower()
    return any(term in text_lower for term in network_terms)
    network_terms = [
        "http://",
        "https://",
        "www.",
        ".com",
        ".org",
        ".net",
        "fetch(",
        "axios",
        "request",
        "download",
        "upload",
        "api.",
        "endpoint",
        "curl",
        "wget",
    ]
    text_lower = text.lower()
    return any(term in text_lower for term in network_terms)
