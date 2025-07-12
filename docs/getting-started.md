# Getting Started

This guide will help you get up and running with the LaTeX Template Engine quickly.

## Prerequisites

- Python 3.9 or higher
- Poetry (recommended) or pip
- Basic knowledge of LaTeX and command-line tools

## Installation

### Method 1: Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/ddunnock/latex-template-engine.git
cd latex-template-engine

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Method 2: Using pip

```bash
# Clone the repository
git clone https://github.com/ddunnock/latex-template-engine.git
cd latex-template-engine

# Install in development mode
pip install -e .

# Or install from PyPI (when published)
pip install latex-template-engine
```

## First Steps

### 1. Verify Installation

```bash
# Check if the CLI is working
latex-engine --help

# Should output:
# Usage: latex-engine [OPTIONS] COMMAND [ARGS]...
# 
# LaTeX Template Engine - Generate LaTeX documents from Jinja2 templates.
# ...
```

### 2. Explore Available Templates

```bash
# List all available templates
latex-engine list-templates
```

You should see a table showing the built-in templates:
- `example`: A simple example template
- `uccs_report`: Professional academic report template

### 3. Get Template Information

```bash
# Get detailed information about a template
latex-engine info uccs_report
```

This shows:
- Template metadata (name, description, author, version)
- Available fields and their types
- Required vs optional parameters

### 4. Initialize Your Own Template Directory

```bash
# Create a new template directory with examples
latex-engine init --template-dir my-templates

# This creates:
# my-templates/
# ├── example.tex.j2      # Example template
# └── example.yaml        # Example configuration
```

### 5. Generate Your First Document

Create a variables file `data.yaml`:

```yaml
title: "My First Document"
author: "Your Name"
date: "2024-01-15"
introduction: "This is my first document generated with the LaTeX Template Engine."
sections:
  - title: "Section 1"
    content: "Content for the first section."
  - title: "Section 2" 
    content: "Content for the second section."
```

Generate the document:

```bash
# Generate using built-in template
latex-engine generate example my-document.tex --variables data.yaml

# Or using your custom template directory
latex-engine generate example my-document.tex \
  --template-dir my-templates \
  --variables data.yaml
```

### 6. Compile the LaTeX Document

```bash
# Compile the generated LaTeX file
pdflatex my-document.tex

# For documents with references, run multiple times:
pdflatex my-document.tex
bibtex my-document
pdflatex my-document.tex
pdflatex my-document.tex
```

## Project Organization

The template engine supports organized project structures for different courses and semesters:

### Folder Structure

```
projects/
├── uccs-me-syse/           # UCCS ME-SYSE program documents
│   └── classes/
│       └── EMGT5510/       # Leadership for Engineers
│           └── 2025_summer/
│               ├── assets/  # Symlink to root assets/ folder
│               ├── *.tex    # Generated LaTeX files
│               └── *.pdf    # Compiled PDFs
└── [other-courses]/        # Future courses
```

### UCCS Workflow

For UCCS ME-SYSE students, use the specialized workflow:

```bash
# Generate documents with proper naming and organization
latex-engine uccs-workflow
```

This command will:
1. Prompt for module number, assignment type, and title
2. Create the proper folder structure
3. Set up asset symlinks automatically
4. Generate the LaTeX document using your chosen template
5. Compile to PDF
6. Optionally open the result

### Manual Compilation

You can also compile existing LaTeX files:

```bash
# Compile with tectonic (default)
latex-engine compile path/to/file.tex

# Compile with different engine
latex-engine compile path/to/file.tex --engine=xelatex

# Compile and open PDF
latex-engine compile path/to/file.tex --open
```

## Common Workflows

### Academic Report Workflow

1. **Get template information**:
   ```bash
   latex-engine info uccs_report
   ```

2. **Create variables file** based on the template fields:
   ```yaml
   student_name: "John Doe"
   course_code: "EMGT5510"
   course_title: "Advanced Project Management"
   instructor_name: "Dr. Smith"
   semester: "2024 Spring"
   title: "Project Management Analysis"
   # ... other required fields
   ```

3. **Generate the document**:
   ```bash
   latex-engine generate uccs_report report.tex --variables report-data.yaml
   ```

4. **Compile to PDF**:
   ```bash
   pdflatex report.tex
   ```

### Custom Template Development

1. **Start with the example**:
   ```bash
   latex-engine init --template-dir custom-templates
   cd custom-templates
   ```

2. **Modify the template** (`example.tex.j2`) to fit your needs

3. **Update the configuration** (`example.yaml`) to define your fields

4. **Test your template**:
   ```bash
   latex-engine generate example test.tex \
     --template-dir . \
     --variables test-data.yaml
   ```

## Troubleshooting

### Common Issues

**Template not found**:
- Check the template name with `latex-engine list-templates`
- Ensure you're in the correct directory or use `--template-dir`

**Variables file errors**:
- Verify YAML/JSON syntax
- Check required fields with `latex-engine info <template-name>`
- Ensure all required fields are provided

**LaTeX compilation errors**:
- Check that all required LaTeX packages are installed
- Review the generated `.tex` file for syntax issues
- Ensure variable values don't contain special LaTeX characters

### Getting Help

- Use `latex-engine --help` for general help
- Use `latex-engine <command> --help` for command-specific help
- Check the [troubleshooting section](troubleshooting.md) for common issues
- Review the [examples](examples.md) for working templates

## Next Steps

- Read the [Template Creation Guide](template-creation.md) to create custom templates
- Explore the [Configuration Reference](configuration.md) for advanced options
- Check out the [Examples](examples.md) for real-world use cases
- Learn about the [Python API](api-reference.md) for programmatic usage
