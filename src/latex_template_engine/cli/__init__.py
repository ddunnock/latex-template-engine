"""Command-line interface for the LaTeX Template Engine.

This module provides the CLI entry point and command implementations
for interacting with the LaTeX template engine from the command line.

The CLI offers functionality for:
- Listing available templates
- Generating documents from templates
- Viewing template information and metadata
- Initializing new template directories
- Managing template configurations

Components:
    main: Entry point function for the CLI application

The CLI is built using Click for command parsing and Rich for enhanced
output formatting, providing a modern and user-friendly terminal experience.
"""

# Import the main CLI entry point
from .main import main

# Define what gets imported with 'from latex_template_engine.cli import *'
__all__ = ["main"]
