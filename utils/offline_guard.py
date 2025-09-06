"""
offline_guard.py — Enforce no-internet runtime for Clever.

Blocks all outbound socket connections except loopback (127.0.0.1, ::1).
Opt-in by importing and calling enable(). Safe to call multiple times.
"""
from __future__ import annotations

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
