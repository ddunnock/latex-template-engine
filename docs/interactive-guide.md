# Interactive CLI Guide

The LaTeX Template Engine includes an interactive CLI interface that makes it easy for LaTeX novices to create professional documents without writing LaTeX code directly.

## Getting Started

### Starting the Interactive Interface

```bash
# Use templates from default directory
latex-engine interactive

# Use templates from a specific directory
latex-engine interactive --template-dir /path/to/templates
```

### Workflow Overview

The interactive interface guides you through these steps:

1. **Template Selection** - Choose from available templates
2. **Field Input** - Enter content for each template field
3. **Preview** - Review your configuration
4. **Generation** - Create the LaTeX document
5. **Compilation** - Optionally compile to PDF

## Step-by-Step Walkthrough

### 1. Template Selection

The interface displays all available templates in a table format:

```
┌─────────────────────────────────────────────────┐
│                Available Templates              │
├──────┬─────────────────┬──────────────┬─────────┤
│ ID   │ Name            │ Description  │ Type    │
├──────┼─────────────────┼──────────────┼─────────┤
│ 1    │ Example Template│ A simple...  │ article │
└──────┴─────────────────┴──────────────┴─────────┘

Select template by ID [1]:
```

Simply enter the number corresponding to your desired template.

### 2. Field Input

For each field defined in the template, you'll be prompted to enter information:

```
Document Title
The title of the document
Enter document title: My Research Paper

Author
The author of the document  
Enter author: John Doe
```

#### Field Types

- **String**: Single-line text input
- **Multiline**: Multi-line text (press Ctrl+D when done)
- **Integer**: Whole numbers with optional min/max validation
- **Float**: Decimal numbers with optional min/max validation
- **Boolean**: Yes/no questions
- **Choice**: Select from predefined options
- **List**: Enter multiple items (one per line, empty line to finish)

#### Input Tips

- **Skip optional fields**: Press Enter to skip optional fields
- **Default values**: Default values are shown in brackets `[default]`
- **Cancel input**: Press Ctrl+C to skip a field
- **Multiline text**: For multiline fields, press Ctrl+D when finished

### 3. Configuration Preview

Before generating the document, you'll see a preview:

```
Configuration Preview:
┌─────────────┬─────────────────────┐
│ Field       │ Value               │
├─────────────┼─────────────────────┤
│ title       │ My Research Paper   │
│ author      │ John Doe            │
│ date        │ \\today             │
│ abstract    │                     │
│ introduction│ This is my intro... │
└─────────────┴─────────────────────┘

Generate LaTeX document with this configuration? [Y/n]:
```

Review your inputs and confirm to proceed.

### 4. Document Generation

If you confirm, the interface will:

1. Generate the LaTeX file
2. Ask for confirmation if a file with the same name exists
3. Show the output path

```
✓ Document generated successfully!
Output: my_research_paper.tex

Compile LaTeX document now? [Y/n]:
```

### 5. PDF Compilation (Optional)

If you have LaTeX installed (pdflatex), the interface can compile your document:

```
Compiling my_research_paper.tex...
✓ PDF generated: my_research_paper.pdf

Open PDF? [Y/n]:
```

On macOS, it will automatically open the PDF in your default viewer.

## Advanced Features

### File Naming

- The output filename is automatically generated from the document title
- Spaces are replaced with underscores
- If a file exists, you'll be prompted to overwrite or choose a new name

### Error Handling

The interface handles common errors gracefully:

- **Missing templates**: Shows a helpful message if no templates are found
- **Invalid input**: Re-prompts for valid input when validation fails
- **Compilation errors**: Shows LaTeX compilation errors if they occur
- **Missing LaTeX**: Warns if pdflatex is not installed

### Keyboard Shortcuts

- **Ctrl+C**: Cancel current input or exit
- **Ctrl+D**: Finish multiline input
- **Enter**: Use default value or continue
- **Tab**: (in some terminals) Auto-completion

## Creating LaTeX-Friendly Templates

For the best user experience, design your templates with these principles:

### 1. Clear Field Descriptions

```yaml
fields:
  - name: "abstract"
    type: "string"
    label: "Abstract"
    description: "A brief summary of your research (150-300 words)"
    required: false
```

### 2. Sensible Defaults

```yaml
fields:
  - name: "date"
    type: "string"
    label: "Document Date"
    description: "Date to appear on the document"
    required: false
    default: "\\today"  # Uses LaTeX's current date
```

### 3. Choice Fields for Common Options

```yaml
fields:
  - name: "bibliography_style"
    type: "choice"
    label: "Bibliography Style"
    description: "Citation format for references"
    required: true
    choices: ["apa", "ieee", "mla", "chicago"]
    default: "apa"
```

### 4. Validation for Numbers

```yaml
fields:
  - name: "font_size"
    type: "integer"
    label: "Font Size (pt)"
    description: "Document font size in points"
    required: false
    default: 12
    min_value: 8
    max_value: 20
```

## Troubleshooting

### No Templates Found

```bash
# Initialize example templates
latex-engine init

# Or specify a template directory
latex-engine interactive --template-dir /path/to/templates
```

### LaTeX Compilation Fails

1. Check that LaTeX is installed: `which pdflatex`
2. Review the error message for missing packages
3. Install required packages with your LaTeX distribution
4. Try compiling manually: `pdflatex document.tex`

### Template Configuration Errors

- Ensure YAML files are properly formatted
- Check that field types are valid (`string`, `integer`, etc.)
- Verify that required fields are marked correctly

## Integration with Editors

### VS Code

1. Open the integrated terminal (Ctrl+`)
2. Run `latex-engine interactive`
3. Generated `.tex` files will appear in your workspace
4. Use LaTeX Workshop extension for syntax highlighting

### Neovim

1. Open a terminal in Neovim (`:terminal`)
2. Run `latex-engine interactive`
3. Use `:e generated_file.tex` to open the result
4. Configure TeXpresso or VimTeX for live preview

## Example Session

Here's a complete example session:

```bash
$ latex-engine interactive

╭──────────────────────────────╮
│ LaTeX Template Engine        │
│ Interactive Document Creator │
╰──────────────────────────────╯

Available Templates
┌──────┬─────────────────┬─────────────┬─────────┐
│ ID   │ Name            │ Description │ Type    │
├──────┼─────────────────┼─────────────┼─────────┤
│ 1    │ Example Template│ A simple... │ article │
└──────┴─────────────────┴─────────────┴─────────┘

Select template by ID [1]: 1

Loaded template: Example Template
A simple example template

Configuring Example Template

Document Title
The title of the document
Enter document title: My Research Paper

Author  
The author of the document
Enter author: Jane Smith

Date
The date of the document
Enter date [\\today]: 

Abstract
Optional abstract for the document
Enter abstract: This paper explores...

Introduction
Introduction section content
Enter introduction: LaTeX is a powerful...

Configuration Preview:
┌─────────────┬──────────────────┐
│ Field       │ Value            │
├─────────────┼──────────────────┤
│ title       │ My Research Paper│
│ author      │ Jane Smith       │
│ date        │ \\today          │
│ abstract    │ This paper...    │
│ introduction│ LaTeX is a...    │
└─────────────┴──────────────────┘

Generate LaTeX document with this configuration? [Y/n]: y

✓ Document generated successfully!
Output: my_research_paper.tex

Compile LaTeX document now? [Y/n]: y

Compiling my_research_paper.tex...
✓ PDF generated: my_research_paper.pdf

Open PDF? [Y/n]: y
```

The interactive interface provides a user-friendly way to create professional LaTeX documents without requiring extensive LaTeX knowledge.
