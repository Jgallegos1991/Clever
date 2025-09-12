"""
Offline Guard Module - Network access enforcement for Clever AI.

Why: Ensures strict offline-first operation by blocking all external network
     connections at the socket level, allowing only loopback connections for
     local development and testing while maintaining security and privacy.

Where: Used during application startup to enforce offline operation and by
       security validation systems to prevent external data leakage.

How: Monkey-patches Python socket module to intercept and block non-loopback
     connections, providing fine-grained network access control with opt-in
     activation and detection of network-related code references.
"""
from __future__ import annotations

import socket
from typing import Tuple

_ENABLED = False
_orig_socket = socket.socket


def _is_loopback(addr: Tuple[str, int]) -> bool:
    """
    Check if network address is a loopback address (localhost).
    
    Why: Determines whether a network connection should be allowed under
         offline-guard restrictions, permitting local connections only.
    
    Where: Used internally by _GuardedSocket to validate connection targets
           and allow local development server access while blocking external.
    
    How: Checks address against known loopback patterns including 127.x.x.x,
         localhost hostname, and IPv6 loopback (::1).
    """
    host = addr[0]
    if host.startswith('127.'):
        return True
    if host in {'localhost', '::1'}:
        return True
    return False


class _GuardedSocket(socket.socket):
    """
    Socket wrapper that blocks non-loopback network connections.
    
    Why: Implements network isolation by intercepting socket connections and
         rejecting external targets while allowing local development access.
    
    Where: Replaces standard socket.socket when offline guard is enabled,
           transparently blocking external connections across all Python code.
    
    How: Inherits from socket.socket and overrides connect methods to validate
         target addresses before allowing connections, raising errors for blocked.
    """
    
    def connect(self, address):  # type: ignore[override]
        """
        Connect to address only if it's a loopback address.
        
        Why: Enforces offline-first policy by blocking external connections
             while allowing local development and testing connections.
        
        Where: Called automatically by all Python network code that uses sockets,
               including HTTP clients, database connections, and APIs.
        
        How: Validates address against loopback criteria and raises PermissionError
             for external addresses, otherwise delegates to parent connect.
        """
        if not _is_loopback(address):
            raise PermissionError(f"Outbound network blocked to {address}")
        return super().connect(address)

    def connect_ex(self, address):  # type: ignore[override]
        """
        Non-blocking connect that returns error code for blocked addresses.
        
        Why: Provides non-exception error handling for network code that expects
             error codes rather than exceptions for connection failures.
        
        Where: Used by network libraries that handle connection errors gracefully
               and need numeric error codes for blocked connections.
        
        How: Returns ECONNREFUSED-like error code (111) for blocked addresses,
             otherwise delegates to parent connect_ex method.
        """
        if not _is_loopback(address):
            return 111  # ECONNREFUSED-like
        return super().connect_ex(address)


def enable() -> None:
    """
    Enable offline guard by replacing socket implementation.
    
    Why: Activates network isolation to ensure Clever operates offline-first
         and prevents accidental external connections or data leaks.
    
    Where: Called during application startup in app.py to enforce offline
         operation throughout the application lifecycle.
    
    How: Replaces socket.socket with _GuardedSocket globally, setting flag
         to prevent duplicate activation, safe to call multiple times.
    """
    global _ENABLED
    if _ENABLED:
        return
    socket.socket = _GuardedSocket  # type: ignore[assignment]
    _ENABLED = True


def disable() -> None:
    """
    Disable offline guard by restoring original socket implementation.
    
    Why: Allows temporary network access for testing or emergency situations
         where external connections may be necessary.
    
    Where: Used by test suites or debugging scenarios that need to validate
         network behavior or connect to external development resources.
    
    How: Restores original socket.socket implementation and clears enabled flag,
         safe to call multiple times and when already disabled.
    """
    global _ENABLED
    if not _ENABLED:
        return
    socket.socket = _orig_socket  # type: ignore[assignment]
    _ENABLED = False


def is_enabled() -> bool:
    """
    Check if offline guard is currently active.
    
    Why: Allows components to verify offline enforcement status for debugging,
         logging, or conditional behavior based on network isolation state.
    
    Where: Used by monitoring systems, debug interfaces, and components that
         need to report or adapt behavior based on offline status.
    
    How: Returns boolean flag indicating whether socket replacement is active
         and network connections are being filtered.
    """
    return _ENABLED


def contains_network_reference(text: str) -> bool:
    """
    Detect network-related terms in text that indicate external connectivity.
    
    Why: Provides static analysis capability to identify code or content that
         may attempt external network access, supporting security auditing.
    
    Where: Used by code analysis tools, security scanners, and validation
           systems to detect potential offline policy violations.
    
    How: Searches for common network-related terms (URLs, API calls, protocols)
         in text content using case-insensitive pattern matching.
    """
    network_terms = [
        'http://', 'https://', 'www.', '.com', '.org', '.net',
        'fetch(', 'axios', 'request', 'download', 'upload',
        'api.', 'endpoint', 'curl', 'wget'
    ]
    text_lower = text.lower()
    return any(term in text_lower for term in network_terms)
