"""Core template engine components.

This module contains the fundamental classes and functionality for the LaTeX
template engine. The core components handle template loading, rendering, and
management of Jinja2 templates with LaTeX-specific configurations.

Components:
    TemplateEngine: Main engine class that orchestrates template
        operations
    Template: Individual template wrapper with metadata and rendering
        capabilities

The core module is designed to be independent of CLI or editor integrations,
making it suitable for embedding in other applications or using
programmatically.
"""

# Import core classes that form the public API of this module
from .engine import TemplateEngine
from .template import Template

# Define what gets imported when using
# 'from latex_template_engine.core import *'
__all__ = ["TemplateEngine", "Template"]
