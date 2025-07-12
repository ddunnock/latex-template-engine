"""Core template engine implementation using Jinja2.

This module defines the core TemplateEngine class responsible for managing
LaTeX templates. The engine loads templates, resolves variables, and generates
final LaTeX documents using Jinja2, making it a central component of the
LaTeX template system.

Template File Convention:
    All Jinja2 template files use the `.tex.j2` extension to distinguish
    them from regular LaTeX files and clearly indicate they are templates.

Components:
    TemplateEngine: Provides methods for loading, listing, and rendering
        templates and manages template configurations.
    Template: Represents individual templates and provides rendering
        capabilities.

Usage:
    Initialize a TemplateEngine to manage your templates directory and
    perform operations like listing available templates, loading specific
    templates, and generating LaTeX documents.

Example:
    from pathlib import Path
    engine = TemplateEngine(Path('./templates'))
    template_names = engine.list_templates()  # Lists .tex.j2 files
    document = engine.generate_document('report', {'title': 'Report Title'})
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from jinja2 import Environment, FileSystemLoader
from pydantic import ValidationError

from ..config.schema import TemplateConfig
from .template import Template


class TemplateEngine:
    """Main template engine for generating LaTeX documents.

    Responsibilities:
    - Loading and parsing Jinja2 template files
    - Rendering templates with user-supplied variables
    - Validating template configurations using Pydantic schemas
    - Managing template directory paths and structures
    """

    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize the template engine.

        Args:
            template_dir: Directory containing Jinja2 templates. If None,
                          defaults to a 'templates' directory relative to
                          the package root.
        """
        if template_dir:
            self.template_dir = template_dir
        else:
            package_root = Path(__file__).parent.parent.parent.parent
            self.template_dir = package_root / "templates"
        # Setup Jinja2 environment with custom delimiters to avoid conflicts
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            block_start_string="<%",
            block_end_string="%>",
            variable_start_string="<<",
            variable_end_string=">>",
            comment_start_string="<#",
            comment_end_string="#>",
            trim_blocks=True,  # Remove trailing newlines after blocks
            lstrip_blocks=True,  # Strip leading spaces on block lines
        )

    def load_template(self, template_name: str) -> Template:
        """Load a template by name.

        This method attempts to load a template by its filename (excluding the
        file extension) and its corresponding configuration file (.yaml).

        Args:
            template_name: Name of the template file (without .tex.j2
                           extension)

        Returns:
            Template: A template object that wraps the Jinja2 template
                and its associated configuration

        Raises:
            FileNotFoundError: If the template file is not found in the
                directory.
            ValueError: If the configuration file is invalid or cannot be
                parsed.
        """
        # Locate template and configuration paths
        template_path = self.template_dir / f"{template_name}.tex.j2"
        config_path = self.template_dir / f"{template_name}.yaml"

        # Check if template file exists
        if not template_path.exists():
            raise FileNotFoundError(f"Template {template_name}.tex.j2 not found")

        # Load Jinja2 template
        jinja_template = self.env.get_template(f"{template_name}.tex.j2")

        # Attempt to load and validate configuration file, if present
        config = None
        if config_path.exists():
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f)
                try:
                    config = TemplateConfig(**config_data)
                except ValidationError as e:
                    raise ValueError(f"Invalid template configuration: {e}")

        # Return the template object
        return Template(jinja_template, config)

    def list_templates(self) -> List[str]:
        """List all available templates.

        This method scans the template directory and returns a list of all
        available template filenames (without their .tex.j2 extensions).

        Returns:
            List[str]: Sorted list of template names
        """
        templates = []
        for file_path in self.template_dir.glob("*.tex.j2"):
            # Extract filename without .tex.j2 extension
            template_name = file_path.name.replace(".tex.j2", "")
            templates.append(template_name)
        return sorted(templates)

    def generate_document(
        self,
        template_name: str,
        variables: Dict[str, Any],
        output_path: Optional[Path] = None,
    ) -> str:
        """Generate a LaTeX document from a template.

        This method uses a specified template to generate a LaTeX document by
        rendering it with provided variables. The result can optionally
        be written to an output file.

        Args:
            template_name: Name of the template to use
            variables: Variables to pass to the template for dynamic
                rendering
            output_path: Optional filesystem path to save the generated
                document

        Returns:
            str: The generated LaTeX content
        """
        # Load the template
        template = self.load_template(template_name)

        # Render template with the given variables
        content = template.render(variables)

        # If an output path is provided, write the generated content to
        # the file
        if output_path:
            output_path.write_text(content)

        # Return the rendered document content
        return content

    def create_template(
        self, name: str, content: str, config: Optional[TemplateConfig] = None
    ) -> None:
        """Create a new template.

        This method allows users to define a new Jinja2 template and
        optionally provide an associated configuration in YAML format.

        Args:
            name: Base filename for the new template (without .tex.j2
                extension)
            content: String content of the Jinja2 template
            config: Optional configuration object for the template
                     defining variables and structure
        """
        # Define paths for template and config files
        template_path = self.template_dir / f"{name}.tex.j2"
        config_path = self.template_dir / f"{name}.yaml"

        # Write the template content to the .tex.j2 file
        template_path.write_text(content)

        # If a configuration is provided, dump it to a YAML file
        if config:
            config_path.write_text(config.model_dump_yaml())
