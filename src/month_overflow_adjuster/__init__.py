"""Public API for the month overflow adjuster.

Only :func:`add_months` is exported; the helpers in :mod:`core` stay private so
that the package surface stays small and the clamping rule has one home.
"""

from .core import add_months

__all__ = ["add_months"]
