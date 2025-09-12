"""
Offline Guard - Enforce strict no-internet runtime for Clever AI.

Why: Maintains Clever AI's offline-first architecture by preventing all
     external network connections while preserving local loopback access.
Where: Core security module imported and enabled at application startup
       to ensure complete network isolation for privacy and security.
How: Patches socket.socket globally to intercept connection attempts,
     blocks non-loopback addresses with PermissionError or error codes.
"""
from __future__ import annotations

import socket
from typing import Tuple

_ENABLED = False
_orig_socket = socket.socket


def _is_loopback(addr: Tuple[str, int]) -> bool:
    """
    Determine if an address is a local loopback connection.
    
    Why: Identifies safe local connections to allow while blocking
         all external network access for offline-first operation.
    Where: Called by _GuardedSocket connection methods to validate
           addresses before allowing socket connections.
    How: Checks if host starts with 127. prefix or matches known
         loopback identifiers (localhost, ::1) for IPv4/IPv6.
    
    Args:
        addr: Tuple containing host string and port number
        
    Returns:
        bool: True if address is loopback, False for external addresses
    """
    host = addr[0]
    if host.startswith('127.'):
        return True
    if host in {'localhost', '::1'}:
        return True
    return False


class _GuardedSocket(socket.socket):
    """
    Socket wrapper that enforces offline-only operation by blocking external connections.
    
    Why: Provides complete network isolation while preserving local functionality
         required for Flask server and internal Clever AI operations.
    Where: Replaces standard socket.socket when offline_guard is enabled,
           intercepting all connection attempts system-wide.
    How: Inherits from socket.socket, overrides connection methods to validate
         addresses against loopback rules before allowing connections.
    """
    
    def connect(self, address):  # type: ignore[override]
        """Connect to address only if it's a loopback address, otherwise block with PermissionError."""
        if not _is_loopback(address):
            raise PermissionError(f"Outbound network blocked to {address}")
        return super().connect(address)

    def connect_ex(self, address):  # type: ignore[override]
        """Attempt connection to address, returning error code for non-loopback addresses."""
        if not _is_loopback(address):
            return 111  # ECONNREFUSED-like
        return super().connect_ex(address)


def enable() -> None:
    """
    Enable offline guard by patching global socket to block external connections.
    
    Why: Activates network isolation to enforce Clever AI's offline-first
         architecture and prevent accidental external network calls.
    Where: Called at application startup in app.py to establish global
           network restrictions for the entire Python process.
    How: Replaces socket.socket globally with _GuardedSocket, sets
         enabled flag to prevent duplicate activation.
    """
    global _ENABLED
    if _ENABLED:
        return
    socket.socket = _GuardedSocket  # type: ignore[assignment]
    _ENABLED = True


def disable() -> None:
    """
    Disable offline guard by restoring original socket functionality.
    
    Why: Allows temporary restoration of full network access for testing
         or specific operations that require external connectivity.
    Where: Called in test scenarios or specific situations where network
           access restoration is explicitly needed.
    How: Restores original socket.socket implementation, clears enabled
         flag to allow re-enablement if needed.
    """
    global _ENABLED
    if not _ENABLED:
        return
    socket.socket = _orig_socket  # type: ignore[assignment]
    _ENABLED = False


def is_enabled() -> bool:
    """
    Check if offline guard is currently active and blocking external connections.
    
    Why: Allows other components to verify network isolation status
         and adapt behavior based on offline enforcement state.
    Where: Used by diagnostic functions and components that need to
           confirm offline-first operation is properly enforced.
    How: Returns the global _ENABLED flag that tracks whether
         socket patching is currently active.
    
    Returns:
        bool: True if offline guard is active, False otherwise
    """
    return _ENABLED


def contains_network_reference(text: str) -> bool:
    """
    Analyze text content for network/internet references that violate offline-first principles.
    
    Why: Provides static analysis capability to detect potential network
         dependencies in code or configuration before runtime execution.
    Where: Used by validation tools and code analysis functions to
           identify offline-first policy violations in Clever AI components.
    How: Searches text for common network-related terms, URLs, and API
         patterns using case-insensitive string matching.
    
    Args:
        text: String content to analyze for network references
        
    Returns:
        bool: True if network references found, False if content appears offline-safe
    """
    network_terms = [
        'http://', 'https://', 'www.', '.com', '.org', '.net',
        'fetch(', 'axios', 'request', 'download', 'upload',
        'api.', 'endpoint', 'curl', 'wget'
    ]
    text_lower = text.lower()
    return any(term in text_lower for term in network_terms)
