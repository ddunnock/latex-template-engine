# Neovim Plugin for LaTeX Template Engine

This directory will contain the Neovim plugin for the LaTeX Template Engine.

## Planned Features

- **Template Selection**: Browse and select from available templates
- **Graphical Form Interface**: Dynamic forms based on template configuration
- **Live Preview**: Integration with existing LaTeX preview tools
- **Section Management**: Add/remove sections dynamically
- **Variable Management**: Edit template variables through forms

## Architecture

```
nvim/
├── lua/
│   └── latex_template_engine/
│       ├── init.lua              # Main plugin entry point
│       ├── config.lua            # Configuration management
│       ├── ui/                   # User interface components
│       │   ├── forms.lua         # Dynamic form generation
│       │   ├── picker.lua        # Template picker
│       │   └── preview.lua       # Preview integration
│       ├── core/                 # Core functionality
│       │   ├── engine.lua        # Interface to Python engine
│       │   ├── templates.lua     # Template management
│       │   └── variables.lua     # Variable handling
│       └── utils/                # Utility functions
│           ├── json.lua          # JSON handling
│           └── files.lua         # File operations
├── plugin/                       # Plugin initialization
│   └── latex_template_engine.vim
└── doc/                          # Documentation
    └── latex_template_engine.txt
```

## Dependencies

- Neovim 0.8+
- Python 3.8+ with latex-template-engine installed
- Optional: telescope.nvim for enhanced UI
- Optional: plenary.nvim for utilities

## Installation

Coming soon...
