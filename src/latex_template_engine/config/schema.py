"""Configuration schemas for templates and the engine.

This module defines Pydantic models and enums representing configuration
schemas used by the LaTeX template engine. These schemas are used to
validate and manage template metadata, document sections, and variable
definitions.

Components:
    DocumentType: Enumeration of supported LaTeX document classes.
    FieldType: Enumeration of supported field types for template variables.
    TemplateField: Model defining the characteristics and constraints of
a variable within a template.
    SectionConfig: Model describing configuration for a document section,
including required fields and optional subsections.
    TemplateConfig: Model encapsulating the overall template structure,
including metadata, fields, sections, and LaTeX-specific settings.

Example:
    from .schema import TemplateConfig
    config = TemplateConfig(name='report', description='An academic report')
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum


class DocumentType(str, Enum):
    """Supported document types."""
    ARTICLE = "article"
    REPORT = "report"
    BOOK = "book"
    LETTER = "letter"
    BEAMER = "beamer"


class FieldType(str, Enum):
    """Supported field types for template variables."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    CHOICE = "choice"
    LIST = "list"


class TemplateField(BaseModel):
    """Configuration for a template field.

    Attributes:
        name: Name of the field variable as used in templates
        type: The type of data expected (e.g., STRING, INTEGER)
        label: A human-readable label for the field (used in GUIs)
        description: Optional description explaining the purpose of the field
        required: Whether this field is mandatory for rendering the template
        default: Default value if the field is not provided
        choices: List of valid choices for fields of type 'CHOICE'
        min_value: Minimum value for numerical types (if applicable)
        max_value: Maximum value for numerical types (if applicable)
    """
    name: str = Field(..., description="Field name")
    type: FieldType = Field(..., description="Field type")
    label: str = Field(..., description="Human-readable label")
    description: Optional[str] = Field(None, description="Field description")
    required: bool = Field(True, description="Whether field is required")
    default: Optional[Any] = Field(None, description="Default value")
    choices: Optional[List[str]] = Field(None, description="Available choices for choice type")
    min_value: Optional[float] = Field(None, description="Minimum value for numeric types")
    max_value: Optional[float] = Field(None, description="Maximum value for numeric types")


class SectionConfig(BaseModel):
    """Configuration for a document section.

    This model describes the setup for sections within a LaTeX document.
    Each section can have its own template file and specified fields.

    Attributes:
        name: Internal name identifier for the section
        title: Display title for the section in the document
        template_file: Optional path to a specific template file for the section
        fields: List of fields applicable to the section
        optional: Whether the section is optional in the document
    """
    name: str = Field(..., description="Section name")
    title: str = Field(..., description="Section title")
    template_file: Optional[str] = Field(None, description="Separate template file for section")
    fields: List[TemplateField] = Field(default_factory=list, description="Section-specific fields")
    optional: bool = Field(False, description="Whether section is optional")


class TemplateConfig(BaseModel):
    """Configuration for a LaTeX template.
    
    This comprehensive model holds metadata and structural information
    about a LaTeX template, its dependencies, fields, and sections.
    
    Attributes:
        name: The name of the template
        description: A brief explanation of what the template is for
        document_type: The LaTeX document class appropriate for this template
        author: Optional author information for the template
        version: Version number of the template
        fields: Fields available in the template for customization
        sections: Structural sections of the template document
        packages: LaTeX packages required by the template
        document_class: The LaTeX class used for the main document
        class_options: Options passed to the LaTeX document class
        tags: Keywords associated with the template for organization
        preview_image: Optional path to a preview image representing the template
    """
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    document_type: DocumentType = Field(..., description="Document type")
    author: Optional[str] = Field(None, description="Template author")
    version: str = Field("1.0.0", description="Template version")
    
    # Template variables
    fields: List[TemplateField] = Field(default_factory=list, description="Template fields")
    
    # Document structure
    sections: List[SectionConfig] = Field(default_factory=list, description="Document sections")
    
    # LaTeX-specific settings
    packages: List[str] = Field(default_factory=list, description="Required LaTeX packages")
    document_class: str = Field("article", description="LaTeX document class")
    class_options: List[str] = Field(default_factory=list, description="Document class options")
    
    # Metadata
    tags: List[str] = Field(default_factory=list, description="Template tags")
    preview_image: Optional[str] = Field(None, description="Preview image path")
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        
    def model_dump_yaml(self) -> str:
        """Export as YAML string.
        
        Uses the PyYAML library to convert the template configuration into a YAML-formatted
        string. This method is useful for serializing the config model when creating or
        updating template configuration files.
        
        Returns:
            str: The YAML string representation of the config model
        """
        import yaml
        return yaml.dump(self.model_dump(), default_flow_style=False, allow_unicode=True)
