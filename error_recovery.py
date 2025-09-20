"""Deprecated error recovery module (stub only).

Why:
    The original error recovery subsystem was overly complex, duplicated
    localized try/except patterns, and generated continual lint/type noise.
    A single global recovery engine is unnecessary; localized handling with
    the debugger provides clearer intent and lower maintenance cost.
Where:
    This lightweight stub remains at the original import path so any legacy
    imports fail fast with a clear migration message. The historical code is
    preserved (read‑only) under ``legacy/error_recovery.py`` for reference.
How:
    Provide a minimal class whose constructor raises immediately with
    migration guidance, plus a small accessor helper used by residual
    call‑sites during the deprecation window.

Connects to:
    - debug_config.py: For modern localized logging & error reporting
    - legacy/error_recovery.py: Archived original implementation
"""

from __future__ import annotations

from typing import Any


class ErrorRecoverySystem:  # pragma: no cover - intentional stub
    """Hard deprecation placeholder.

    Why:
        Prevent accidental use of the removed centralized recovery system.
    Where:
        Only touched by outdated code paths that have not yet been migrated.
    How:
        Constructor raises ``NotImplementedError`` with guidance so the
        failure mode is explicit and actionable during development/testing.

    Connects to:
        - debug_config.py: Use ``get_debugger()`` for logging & metrics.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401
        raise NotImplementedError(
            "ErrorRecoverySystem is deprecated. Use localized try/except blocks "
            "with debug_config.get_debugger() for logging. See legacy/error_recovery.py "
            "for the archived reference implementation."
        )


def get_error_recovery() -> ErrorRecoverySystem:  # pragma: no cover
    """Return the deprecated system stub (always raises when constructed).

    Returns:
        ErrorRecoverySystem: The stub class; instantiation raises immediately.
    """
    return ErrorRecoverySystem()  # Will raise


__all__ = ["ErrorRecoverySystem", "get_error_recovery"]
