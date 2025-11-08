"""Core module for U-CHS backend application."""

from .config import settings
from .logging_config import setup_logging

__all__ = ["settings", "setup_logging"]
