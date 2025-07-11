"""Configuration schemas and utilities.

This module provides Pydantic-based configuration schemas for the LaTeX
template engine. It defines the structure and validation rules for
template metadata, field definitions, and document configurations.

The configuration system is designed to be:
- Type-safe through Pydantic validation
- Serializable to/from YAML for human-readable configuration files
- Extensible for future template features
- Editor-friendly for generating UI forms

Main Components:
    TemplateConfig: Root configuration model for templates
    TemplateField: Model for individual template variables
    SectionConfig: Model for document section definitions
    DocumentType: Enum of supported LaTeX document classes
    FieldType: Enum of supported variable types

Usage:
    These schemas are used throughout the engine to validate template
    configurations, generate editor interfaces, and ensure consistency
    between templates and their metadata.
"""

# Import all configuration models and enums
from .schema import TemplateConfig, TemplateField, SectionConfig, DocumentType, FieldType

# Define public API for the config module
__all__ = ["TemplateConfig", "TemplateField", "SectionConfig", "DocumentType", "FieldType"]
