# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2025-07-12

### Added
- **Project Folder Structure**
  - Added `projects/` folder for organized LaTeX document management
  - Automatic asset symlink creation for consistent resource access
  - New readme section in documentation for project organization and workflows

- **CLI Enhancements**
  - Added `uccs-workflow` command for structured document generation
  - Added `compile` command for compiling existing `.tex` files

- **Code Quality Improvements**
  - Fixed flake8 issues for cleaner, more maintainable code
  - Ensured black and isort compliance across all files

### Updated
- Documentation to reflect changes in project organization and CLI commands
- CHANGELOG to include new features

## [0.2.0] - 2025-07-12

### Added
- **Interactive CLI Interface**
  - New `latex-engine interactive` command for guided document creation
  - User-friendly prompts for template selection and field input
  - Support for all field types: string, multiline, integer, float, boolean, choice, list
  - Real-time validation with min/max value constraints
  - Configuration preview before document generation
  - Automatic LaTeX compilation with PDF generation
  - Cross-platform PDF opening (macOS support included)

- **Enhanced Template Management**
  - Improved template listing with rich table formatting
  - Better error handling for missing templates and configurations
  - Automatic file naming based on document title
  - File overwrite protection with user confirmation

- **Documentation**
  - Comprehensive Interactive CLI Guide (`docs/interactive-guide.md`)
  - Configuration Reference documentation (`docs/configuration.md`)
  - Updated README with interactive features prominently featured
  - Best practices for creating user-friendly templates

- **Code Quality**
  - Full flake8 compliance with custom configuration
  - 100% mypy type checking coverage for new interactive module
  - Comprehensive error handling and user feedback
  - Improved code formatting and organization

### Fixed
- Fixed YAML configuration generation to avoid Python object references
- Improved template syntax validation and error reporting
- Enhanced CLI help text and command descriptions
- Better handling of optional and required template fields

### Changed
- Updated README to prioritize interactive mode for beginners
- Enhanced CLI output with better formatting and colors
- Improved template configuration loading with proper validation
- Streamlined document generation workflow

## [0.1.0] - 2025-07-11

### Added
- **Core LaTeX Template Engine**
  - `TemplateEngine` class with Jinja2 integration for LaTeX template processing
  - `Template` wrapper class for enhanced template management and rendering
  - Configuration schema with Pydantic models for template validation
  - Support for YAML-based template configuration files

- **Command Line Interface (CLI)**
  - `latex-engine` CLI tool with Click framework
  - Template rendering command with file input/output options
  - Rich console output with colored formatting and progress indicators
  - Comprehensive error handling and user feedback

- **Project Structure**
  - Modern Python package structure with Poetry for dependency management
  - Modular architecture with separate core, config, and CLI modules
  - Comprehensive type hints throughout the codebase
  - Well-organized source code in `src/latex_template_engine/` package

- **Templates and Examples**
  - Sample LaTeX templates (`example.tex`, `uccs_report.tex`)
  - YAML configuration examples (`uccs_sample.yaml`, `uccs_report.yaml`)
  - Template examples for academic report formatting

- **Development Infrastructure**
  - GitHub Actions CI/CD workflow (`.github/workflows/ci.yml`)
  - Poetry configuration with development dependencies
  - Testing framework with pytest
  - Code quality tools (black, isort, flake8, mypy)
  - Pre-commit hooks configuration

- **Editor Plugin Framework**
  - Plugin directory structure for Neovim and VS Code integrations
  - README documentation for plugin development
  - Extensible architecture for future editor integrations

- **Documentation**
  - Comprehensive README with project overview, features, and development guide
  - Detailed code documentation with 100% docstring coverage
  - Enhancement documentation (`docs/COMMENTING_ENHANCEMENT.md`)
  - Plugin development guides

- **Dependencies**
  - Jinja2 (^3.1.2) for template processing
  - PyYAML (^6.0) for configuration file parsing
  - Click (^8.1.7) for CLI interface
  - Rich (^13.7.0) for enhanced console output
  - Watchdog (^3.0.0) for file system monitoring
  - Pydantic (^2.5.0) for data validation
  - Full development toolchain with testing and linting tools

- **Testing**
  - Unit tests for core engine functionality
  - Test configuration and example test cases
  - Pytest configuration with coverage support

### Technical Details
- Python 3.9+ support with modern type annotations
- Comprehensive inline comments explaining complex logic and design choices
- Modular design with clear separation of concerns
- Extensible plugin architecture for editor integrations
- Robust error handling and validation throughout
- Memory-efficient template processing with lazy loading

[Unreleased]: https://github.com/ddunnock/latex-template-engine/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/ddunnock/latex-template-engine/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/ddunnock/latex-template-engine/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/ddunnock/latex-template-engine/releases/tag/v0.1.0
