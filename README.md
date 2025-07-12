# LaTeX Template Engine

A modern LaTeX template engine with Jinja2 templating, providing graphical interfaces for both Neovim and VS Code to create and manage LaTeX documents.

## 🎯 Goals

- **Template Generation**: Create custom LaTeX templates using Jinja2 templating
- **Editor Integration**: Neovim and VS Code plugins with graphical interfaces
- **Dynamic Content**: Add new sections to documents through the interface
- **Extensible**: Support for multiple document types and academic formats

## 🏗️ Architecture

```
latex-template-engine/
├── src/latex_template_engine/     # Core Python package
├── templates/                     # Jinja2 LaTeX templates (*.tex.j2)
├── schemas/                       # Template configuration schemas
├── plugins/                       # Editor plugins
│   ├── nvim/                     # Neovim plugin
│   └── vscode/                   # VS Code extension
├── examples/                     # Example templates and configs
└── tests/                        # Test suite
```

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/ddunnock/latex-template-engine.git
cd latex-template-engine

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run CLI
latex-engine --help
```

## 📋 Features

### Current
- [ ] Core template engine with Jinja2
- [ ] CLI interface for template generation
- [ ] Basic LaTeX template library
- [ ] Configuration schema validation

### Planned
- [ ] Neovim plugin with graphical interface
- [ ] VS Code extension
- [ ] Live preview integration
- [ ] Template marketplace/sharing
- [ ] Advanced document structure management

## 🛠️ Development

```bash
# Install development dependencies
poetry install --with dev

# Run tests
pytest

# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Pre-commit hooks
pre-commit install
```

## 📚 Documentation

See the `docs/` directory for detailed documentation on:
- Template creation
- Plugin development
- API reference
- Configuration options
