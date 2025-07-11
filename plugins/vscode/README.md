# VS Code Extension for LaTeX Template Engine

This directory will contain the VS Code extension for the LaTeX Template Engine.

## Planned Features

- **Template Gallery**: Visual browser for available templates
- **Form-based Configuration**: Rich forms for template variables
- **Integrated Preview**: Live LaTeX preview with template updates
- **Workspace Integration**: Template management within VS Code workspace
- **Section Wizard**: Guided section creation and management

## Architecture

```
vscode/
├── src/
│   ├── extension.ts              # Main extension entry point
│   ├── templates/                # Template management
│   │   ├── manager.ts            # Template operations
│   │   ├── picker.ts             # Template selection UI
│   │   └── gallery.ts            # Template gallery view
│   ├── ui/                       # User interface
│   │   ├── forms.ts              # Dynamic form generation
│   │   ├── webview.ts            # Webview management
│   │   └── panels.ts             # Side panel integration
│   ├── core/                     # Core functionality
│   │   ├── engine.ts             # Python engine interface
│   │   ├── config.ts             # Configuration handling
│   │   └── preview.ts            # Preview integration
│   └── utils/                    # Utilities
│       ├── python.ts             # Python process management
│       └── files.ts              # File operations
├── media/                        # Static assets
│   ├── icons/                    # Extension icons
│   └── styles/                   # CSS styles
├── package.json                  # Extension manifest
├── tsconfig.json                 # TypeScript configuration
└── webpack.config.js             # Build configuration
```

## Dependencies

- VS Code 1.60+
- Node.js 16+
- Python 3.8+ with latex-template-engine installed

## Installation

Coming soon...
