"""LaTeX Template Engine

A modern LaTeX template engine with Jinja2 templating and editor integrations.

This package provides a comprehensive solution for generating LaTeX
documents from Jinja2 templates with support for:
- Dynamic template variables and configuration
- Structured document sections and hierarchies
- Editor integrations for Neovim and VS Code
- CLI tools for template management and document generation

Main Components:
    TemplateEngine: Core engine for loading and rendering templates
    Template: Wrapper for individual Jinja2 templates with metadata
    TemplateConfig: Pydantic schema for template configuration

Example:
    >>> from latex_template_engine import TemplateEngine
    >>> engine = TemplateEngine()
    >>> engine.generate_document('report', {'title': 'My Report'})
"""

# Package metadata
__version__ = "0.1.0"
__author__ = "David Dunnock"
__description__ = "LaTeX template engine with Jinja2 and editor integrations"

from .config.schema import TemplateConfig

# Core imports - these are the main public API components
from .core.engine import TemplateEngine
from .core.template import Template

# Define what gets imported with 'from latex_template_engine import *'
__all__ = ["TemplateEngine", "Template", "TemplateConfig"]
