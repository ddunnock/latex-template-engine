# LaTeX Template Engine

[![CI/CD](https://github.com/ddunnock/latex-template-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/ddunnock/latex-template-engine/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-blue.svg)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy.readthedocs.io/)

A modern LaTeX template engine with Jinja2 templating that simplifies creating and managing LaTeX documents through a powerful command-line interface and structured template system.

## ✨ Features

### Current (v0.3.0)
- ✅ **Core Template Engine**: Full Jinja2 integration with LaTeX-optimized delimiters
- ✅ **Interactive CLI**: Guided document creation perfect for LaTeX novices
- ✅ **CLI Interface**: Complete command-line tool for template management and document generation
- ✅ **Template Library**: Professional templates including academic reports
- ✅ **Configuration Schema**: Pydantic-based validation for template configurations
- ✅ **Rich Output**: Beautiful formatted CLI output with tables and colors
- ✅ **Type Safety**: Full mypy type checking for robust development
  - ✅ **Project Management**: Automated asset link creation and seamless organization
   - ✅ **Structured Workflows**: New command `uccs-workflow` for structured document creation
   - ✅ **Direct Compilation**: Compile `.tex` files directly with `compile` command

### Planned
- 🔄 Neovim plugin with graphical interface
- 🔄 VS Code extension
- 🔄 Live preview integration
- 🔄 Template marketplace/sharing
- 🔄 Advanced document structure management

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ddunnock/latex-template-engine.git
cd latex-template-engine

# Install with Poetry (recommended)
poetry install
# Install pre-commit hooks
poetry run pre-commit install

# Activate the virtual environment
poetry shell

# Or install with pip (development mode)
pip install -e .
```

### Basic Usage

```bash
# Interactive mode (recommended for beginners)
latex-engine interactive

# Structured document creation (UCCS Workflow)
latex-engine uccs-workflow

# List available templates
latex-engine list-templates

# Get information about a template
latex-engine info uccs_report

# Initialize new template directory with examples
latex-engine init --template-dir my-templates

# Generate a document from template
latex-engine generate uccs_report output.tex --variables data.yaml

# Compile a `.tex` file directly
latex-engine compile path/to/document.tex
```

## 📖 Usage Guide

### 0. Interactive Mode (Recommended for Beginners)

The interactive CLI provides a guided experience for creating LaTeX documents:

```bash
latex-engine interactive
```

This will:
1. **Show available templates** in a table format
2. **Guide you through field input** with helpful prompts
3. **Preview your configuration** before generation
4. **Generate the LaTeX document** automatically
5. **Optionally compile to PDF** if LaTeX is installed

Perfect for LaTeX novices who want to create professional documents without writing LaTeX code directly.

> 📚 **See the full [Interactive CLI Guide](docs/interactive-guide.md) for detailed walkthrough and examples.**

### 1. Working with Templates

#### List Available Templates
```bash
latex-engine list-templates
```
Displays all `.tex.j2` template files in a formatted table.

#### Get Template Information
```bash
latex-engine info <template-name>
```
Shows detailed information about a template including:
- Metadata (name, description, author, version)
- Available fields and their types
- Required vs optional parameters

#### Initialize Template Directory
```bash
latex-engine init [--template-dir PATH]
```
Creates a new template directory with example templates and configurations.

### 2. Generating Documents

#### Basic Generation
```bash
latex-engine generate <template-name> <output-path>
```

#### With Variables File
```bash
latex-engine generate <template-name> <output-path> --variables data.yaml
```

#### With Custom Template Directory
```bash
latex-engine generate <template-name> <output-path> \
  --template-dir ./my-templates \
  --variables data.yaml
```

### 3. Template Structure

Templates use `.tex.j2` extension and Jinja2 syntax with LaTeX-optimized delimiters:

- **Variables**: `<<variable_name>>`
- **Blocks**: `<% block_name %>....<% endblock %>`
- **Comments**: `<# comment #>`

#### Example Template (`example.tex.j2`):
```latex
\documentclass[<<document_class_options>>]{<<document_class>>}

<% for package in packages %>
\usepackage{<<package>>}
<% endfor %>

\title{<<title>>}
\author{<<author>>}
\date{<<date>>}

\begin{document}
\maketitle

<% if abstract %>
\begin{abstract}
<<abstract>>
\end{abstract}
<% endif %>

\section{Introduction}
<<introduction>>

<% for section in sections %>
\section{<<section.title>>}
<<section.content>>
<% endfor %>

\end{document}
```

### 4. Configuration Files

Each template can have a corresponding `.yaml` configuration file defining:

```yaml
name: "Template Name"
description: "Template description"
document_type: "article"  # or "report", "book", etc.
author: "Author Name"
version: "1.0.0"

fields:
  - name: "title"
    type: "string"
    label: "Document Title"
    description: "The main title"
    required: true
    
  - name: "date"
    type: "date"
    label: "Date"
    default: "\\today"
    required: false

packages:
  - "geometry"
  - "amsmath"
  - "graphicx"

document_class: "article"
class_options: ["12pt", "letterpaper"]
tags: ["academic", "report"]
```

### 5. Variables Files

Supports both YAML and JSON for providing template variables:

**YAML Example** (`data.yaml`):
```yaml
title: "My Academic Report"
author: "John Doe"
date: "2024-01-15"
abstract: "This is the abstract content..."
introduction: "This document presents..."
sections:
  - title: "Methodology"
    content: "The methodology section..."
  - title: "Results"
    content: "The results show..."
```

**JSON Example** (`data.json`):
```json
{
  "title": "My Academic Report",
  "author": "John Doe",
  "date": "2024-01-15",
  "abstract": "This is the abstract content...",
  "introduction": "This document presents...",
  "sections": [
    {
      "title": "Methodology",
      "content": "The methodology section..."
    },
    {
      "title": "Results",
      "content": "The results show..."
    }
  ]
}
```

## 🏗️ Project Structure

```
latex-template-engine/
├── src/latex_template_engine/     # Core Python package
│   ├── cli/                       # Command-line interface
│   ├── config/                    # Configuration schemas
│   └── core/                      # Template engine core
├── templates/                     # Built-in Jinja2 templates (*.tex.j2)
├── docs/                          # Documentation
├── tests/                         # Test suite
├── pyproject.toml                 # Project configuration
├── projects/                      # Organized LaTeX documents
└── README.md                      # This file
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=latex_template_engine --cov-report=html

# Run specific test
poetry run pytest tests/test_engine.py::test_list_templates
```

### Code Quality

```bash
# Format code
poetry run black src/ tests/
poetry run isort src/ tests/

# Lint code
poetry run flake8 src/ tests/

# Type checking
poetry run mypy src/

# Run all quality checks
poetry run black --check src/ tests/ && \
poetry run isort --check-only src/ tests/ && \
poetry run flake8 src/ tests/ && \
poetry run mypy src/
```

### Testing CLI Commands

```bash
# Test help
poetry run latex-engine --help

# Test template listing
poetry run latex-engine list-templates

# Test template info
poetry run latex-engine info uccs_report

# Test init command
poetry run latex-engine init --template-dir test-templates

# Test UCCS workflow
poetry run latex-engine uccs-workflow
```

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:

- **[Getting Started](docs/getting-started.md)** - Installation and basic usage
- **[Template Creation](docs/template-creation.md)** - How to create custom templates
- **[Configuration Reference](docs/configuration.md)** - Complete configuration options
- **[API Reference](docs/api-reference.md)** - Python API documentation
- **[Examples](docs/examples.md)** - Real-world usage examples

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](docs/contributing.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Jinja2](https://jinja.palletsprojects.com/) for the powerful templating engine
- [Click](https://click.palletsprojects.com/) for the excellent CLI framework
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
