"""Template representation for Jinja2 templates.

This module defines the Template class which serves as a wrapper around
Jinja2 Template objects, adding LaTeX-specific functionality and metadata
management capabilities.

The Template class bridges the gap between raw Jinja2 templates and the
structured configuration system used by the LaTeX template engine.
"""

from typing import Dict, Any, Optional
from jinja2 import Template as Jinja2Template
from ..config.schema import TemplateConfig


class Template:
    """Wrapper around Jinja2 Template with LaTeX-specific configuration.
    
    This class encapsulates a Jinja2 template along with its associated
    configuration metadata, providing a unified interface for template
    operations within the LaTeX template engine.
    
    Attributes:
        jinja_template: The underlying Jinja2 template object
        config: Optional configuration object containing template metadata
                and variable definitions
    """

    def __init__(self, jinja_template: Jinja2Template, config: Optional[TemplateConfig] = None):
        """Initialize a Template.

        Args:
            jinja_template: The Jinja2 template object to wrap
            config: Optional TemplateConfig object containing metadata
                   such as field definitions, document structure, and
                   template-specific settings
        """
        self.jinja_template = jinja_template
        self.config = config

    def render(self, variables: Dict[str, Any]) -> str:
        """Render the template with given variables.

        This method delegates to the underlying Jinja2 template's render
        method, but could be extended in the future to add LaTeX-specific
        preprocessing, validation, or post-processing steps.

        Args:
            variables: Dictionary of variables to pass to the template.
                      Keys should match variable names used in the template,
                      and values can be any JSON-serializable type.

        Returns:
            str: The rendered LaTeX document content as a string
            
        Raises:
            jinja2.TemplateError: If template rendering fails due to
                                 syntax errors or missing variables
        """
        return self.jinja_template.render(variables)
    
    def validate_variables(self, variables: Dict[str, Any]) -> bool:
        """Validate variables against template configuration.
        
        This method checks if the provided variables match the expected
        structure defined in the template's configuration.
        
        Args:
            variables: Variables to validate
            
        Returns:
            bool: True if variables are valid, False otherwise
            
        Note:
            This method is a placeholder for future implementation.
            Currently returns True for all inputs.
        """
        # TODO: Implement variable validation against config.fields
        # This should check required fields, types, and constraints
        return True
    
    def get_required_variables(self) -> list[str]:
        """Get list of required variable names from configuration.
        
        Returns:
            list[str]: List of required variable names, or empty list
                      if no configuration is available
        """
        if not self.config or not self.config.fields:
            return []
        
        return [field.name for field in self.config.fields if field.required]
