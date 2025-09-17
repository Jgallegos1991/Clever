"""
"""

import socket
from typing import Tuple

_ENABLED = False
_orig_socket = socket.socket


def _is_loopback(addr: Tuple[str, int]) -> bool:
    host = addr[0]
    if host.startswith('127.'):
        return True
    if host in {'localhost', '::1'}:
        return True
    return False

    # ...existing code...
    host = addr[0]
    if host.startswith('127.'):
        return True
    if host in {'localhost', '::1'}:
        return True
    return False


class _GuardedSocket(socket.socket):
    def connect(self, address):  # type: ignore[override]
        if not _is_loopback(address):
            raise PermissionError(f"Outbound network blocked to {address}")
        return super().connect(address)

    def connect_ex(self, address):  # type: ignore[override]
        if not _is_loopback(address):
            return 111  # ECONNREFUSED-like
        return super().connect_ex(address)



def enable() -> None:
    global _ENABLED
    if _ENABLED:
        return
    socket.socket = _GuardedSocket  # type: ignore[assignment]
    _ENABLED = True


def disable() -> None:
    global _ENABLED
    if not _ENABLED:
        return
    socket.socket = _orig_socket  # type: ignore[assignment]
    _ENABLED = False


def is_enabled() -> bool:
    return _ENABLED


def contains_network_reference(text: str) -> bool:
    """Check if text contains network/internet references that should be blocked"""
    network_terms = [
        'http://', 'https://', 'www.', '.com', '.org', '.net',
        'fetch(', 'axios', 'request', 'download', 'upload',
        'api.', 'endpoint', 'curl', 'wget'
    ]
    text_lower = text.lower()
    return any(term in text_lower for term in network_terms)
    network_terms = [
        'http://', 'https://', 'www.', '.com', '.org', '.net',
        'fetch(', 'axios', 'request', 'download', 'upload',
        'api.', 'endpoint', 'curl', 'wget'
    ]
    text_lower = text.lower()
    return any(term in text_lower for term in network_terms)
