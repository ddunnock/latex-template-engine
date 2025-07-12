# Configuration Reference

This document outlines all available configuration options for creating LaTeX templates using the LaTeX Template Engine.

## Overview

Templates are defined by two components:

1. **Template File** (`.tex.j2`) - Defines the LaTeX structure using Jinja2 templating.
2. **Configuration File** (`.yaml`) - Defines metadata and input fields.

Each template supports various field types and options that determine how the template engine processes the LaTeX document.

## Configuration Structure

### Document Information

- **name**: The name of the template
- **description**: A brief summary of the template's purpose and features
- **document_type**: The LaTeX document class (e.g., "article", "report")
- **author**: The name of the template creator
- **version**: The template version number (ideally following semantic versioning)

### Fields

Used to define variables for the template. Fields can be required or optional, and some can have default values.

#### Field Attributes

- **name**: The internal variable name (used in the template file)
- **type**: The field type (e.g., "string", "boolean", "choice")
- **label**: A user-friendly name for use in interfaces
- **description**: Detailed explanation of what the field is for
- **required**: Boolean indicating if the field is mandatory
- **default**: The default value if not provided (optional)
- **choices**: A list of allowed values for "choice" type fields (optional)
- **min_value**: Minimum allowed value for "integer" or "float" types
- **max_value**: Maximum allowed value for "integer" or "float" types

### Field Types

- **string**: Text input (single-line)
- **multiline**: Text input (multi-line)
- **integer**: Whole numbers
- **float**: Decimal numbers
- **boolean**: True or False
- **choice**: Dropdown selection (choose from a list)
- **list**: Ordered list of items
- **dict**: Key-value mapping (nested structure)

### Document Structure

You can define sections and subsections using structured fields. Typically organized as:

```yaml
sections:
  - name: "Introduction"
    title: "Introduction"
    optional: false
    fields:
      - name: "introduction_text"
        type: "multiline"
        label: "Introduction Text"
        required: true
  - name: "Conclusion"
    title: "Conclusion"
    optional: true
    fields:
      - name: "conclusion_text"
        type: "multiline"
        label: "Conclusion Text"
        required: false
```

### Packages

List the required LaTeX packages to use with your document. These packages need to be installed in your LaTeX distribution.

```yaml
packages:
  - "geometry"
  - "graphicx"
  - "hyperref"
```

### Document Class Options

Configure LaTeX document class options like font size and paper dimensions:

```yaml
document_class: "article"
class_options:
  - "11pt"
  - "a4paper"
```

### Tags

Provide tags to categorize and label the template for easy discovery:

```yaml
tags:
  - "academic"
  - "presentation"
  - "minimal"
```

### Metadata

Custom metadata tags can be added to the configuration for additional context, such as:

- **license**: The license under which the template is shared
- **contributors**: Names or contact information for template contributors

```yaml
license: "MIT"
contributors:
  - "Jane Doe (jane@example.com)"
  - "John Smith"
```

## Best Practices

1. **Simplify Fields**: Limit the number of fields to what is necessary.
2. **Use Defaults**: Provide default values for optional fields to simplify user input.
3. **Organize Sections**: Use sections to logically group fields.
4. **Comprehensive Labels**: Ensure labels are user-friendly for the template audience.
5. **Versioning**: Maintain a version history and update the version number with each change.

## Example Configuration File

```yaml
name: "Research Paper Template"
description: "Template for formatting research papers"
document_type: "article"
author: "Research Templates Inc."
version: "1.2.0"

fields:
  - name: "title"
    type: "string"
    label: "Document Title"
    description: "Main title of the research paper"
    required: true
    
  - name: "abstract"
    type: "multiline"
    label: "Abstract"
    description: "Summary of the research paper"
    required: true
    
  - name: "authors"
    type: "list"
    label: "Authors"
    description: "List of authors involved in the paper"
    required: true
    
  - name: "version"
    type: "string"
    label: "Version"
    description: "The document version"
    default: "1.0"

sections:
  - name: "introduction"
    title: "Introduction"
    fields:
      - name: "introduction_text"
        type: "multiline"
        label: "Introduction Text"
        required: true

  - name: "methodology"
    title: "Methodology"
    optional: true
    fields:
      - name: "method_text"
        type: "multiline"
        label: "Methodology"

packages:
  - "geometry"
  - "graphicx"

class_options:
  - "12pt"
  - "letterpaper"

tags:
  - "journal paper"
  - "research"
  - "academic"

license: "Creative Commons"
contributors:
  - "Alice Researcher"
  - "Bob Scholar"
```
