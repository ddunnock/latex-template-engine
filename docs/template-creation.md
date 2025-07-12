# Template Creation Guide

This guide covers everything you need to know about creating custom LaTeX templates for the LaTeX Template Engine.

## Template Basics

### Template Files

Templates consist of two parts:

1. **Template File** (`.tex.j2`): The Jinja2 LaTeX template
2. **Configuration File** (`.yaml`): Metadata and field definitions

### Template Delimiters

The engine uses LaTeX-optimized Jinja2 delimiters to avoid conflicts:

- **Variables**: `<<variable_name>>`
- **Blocks**: `<% block_name %>....<% endblock %>`
- **Comments**: `<# This is a comment #>`

## Creating Your First Template

### 1. Start with the Basic Structure

Create `my-template.tex.j2`:

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

<<content>>

\end{document}
```

### 2. Create the Configuration File

Create `my-template.yaml`:

```yaml
name: "My Custom Template"
description: "A simple custom template for documents"
document_type: "article"
author: "Your Name"
version: "1.0.0"

fields:
  - name: "title"
    type: "string"
    label: "Document Title"
    description: "The main title of the document"
    required: true
    
  - name: "author"
    type: "string"
    label: "Author"
    description: "The document author"
    required: true
    
  - name: "date"
    type: "string"
    label: "Date"
    description: "Document date"
    default: "\\today"
    required: false
    
  - name: "abstract"
    type: "string"
    label: "Abstract"
    description: "Optional document abstract"
    required: false
    
  - name: "content"
    type: "string"
    label: "Main Content"
    description: "The main document content"
    required: true

packages:
  - "geometry"
  - "amsmath"

document_class: "article"
class_options: ["12pt", "letterpaper"]
tags: ["simple", "custom"]
```

### 3. Test Your Template

Create a test variables file `test-data.yaml`:

```yaml
title: "Test Document"
author: "Test Author"
content: "This is the main content of the document."
```

Generate and test:

```bash
latex-engine generate my-template test-output.tex \
  --template-dir . \
  --variables test-data.yaml
```

## Advanced Template Features

### Conditional Content

Use Jinja2 conditionals for optional sections:

```latex
<% if include_toc %>
\tableofcontents
\newpage
<% endif %>

<% if abstract %>
\begin{abstract}
<<abstract>>
\end{abstract}
<% endif %>

<% if include_references and references %>
\bibliographystyle{<<bibliography_style or "plain">>}
\bibliography{<<bibliography_file>>}
<% endif %>
```

### Loops for Dynamic Content

#### Simple Lists

```latex
<% if packages %>
<% for package in packages %>
\usepackage{<<package>>}
<% endfor %>
<% endif %>
```

#### Complex Sections

```latex
<% for section in sections %>
\section{<<section.title>>}
<<section.content>>

<% if section.subsections %>
<% for subsection in section.subsections %>
\subsection{<<subsection.title>>}
<<subsection.content>>
<% endfor %>
<% endif %>
<% endfor %>
```

#### Tables

```latex
<% if data_table %>
\begin{table}[h]
\centering
\begin{tabular}{<<table_columns or "lcc">>}
\hline
<% for header in data_table.headers %>
<<header>><% if not loop.last %> & <% endif %>
<% endfor %> \\
\hline
<% for row in data_table.rows %>
<% for cell in row %>
<<cell>><% if not loop.last %> & <% endif %>
<% endfor %> \\
<% endfor %>
\hline
\end{tabular}
\caption{<<data_table.caption or "Data Table">>}
\label{tab:<<data_table.label or "data">>}
\end{table}
<% endif %>
```

### Macros and Functions

Define reusable template snippets:

```latex
<# Macro for creating a figure #>
<% macro figure(path, caption, label, width="0.8") %>
\begin{figure}[h]
\centering
\includegraphics[width=<<width>>\textwidth]{<<path>>}
\caption{<<caption>>}
\label{fig:<<label>>}
\end{figure}
<% endmacro %>

<# Use the macro #>
<% for figure in figures %>
<<figure(figure.path, figure.caption, figure.label, figure.width)>>
<% endfor %>
```

## Configuration Reference

### Field Types

The configuration supports these field types:

#### String Fields
```yaml
- name: "title"
  type: "string"
  label: "Document Title"
  description: "The main title"
  required: true
  default: "Untitled Document"
```

#### Boolean Fields
```yaml
- name: "include_toc"
  type: "boolean"
  label: "Include Table of Contents"
  description: "Whether to include a TOC"
  default: true
  required: false
```

#### Choice Fields
```yaml
- name: "document_style"
  type: "choice"
  label: "Document Style"
  description: "Choose the document style"
  choices: ["modern", "classic", "minimal"]
  default: "modern"
  required: true
```

#### List Fields
```yaml
- name: "sections"
  type: "list"
  label: "Document Sections"
  description: "List of main sections"
  required: true
```

#### Numeric Fields
```yaml
- name: "margin_size"
  type: "float"
  label: "Margin Size"
  description: "Document margins in inches"
  min_value: 0.5
  max_value: 2.0
  default: 1.0
  required: false
```

### Document Types

Supported document types:
- `article`: Standard articles and papers
- `report`: Longer reports with chapters
- `book`: Book-length documents
- `letter`: Formal letters
- `beamer`: Presentations

### Package Management

Specify required LaTeX packages:

```yaml
packages:
  - "geometry"      # Page layout
  - "amsmath"       # Math support
  - "graphicx"      # Images
  - "hyperref"      # Links
  - "biblatex"      # Bibliography
  - "xcolor"        # Colors
  - "tikz"          # Diagrams
```

### Class Options

Common document class options:

```yaml
class_options:
  - "12pt"          # Font size
  - "letterpaper"   # Paper size
  - "onecolumn"     # Column layout
  - "oneside"       # Single-sided
  - "final"         # Final version
```

## Real-World Examples

### Academic Paper Template

```latex
\documentclass[<<font_size or "12pt">>, <<paper_size or "letterpaper">>]{article}

% Required packages
\usepackage[margin=<<margin or "1in">>]{geometry}
\usepackage{amsmath, amsfonts, amssymb}
\usepackage{graphicx}
\usepackage{cite}
\usepackage{hyperref}

% Title and authors
\title{<<title>>}
\author{
<% for author in authors %>
<<author.name>><% if author.affiliation %>\thanks{<<author.affiliation>>}<% endif %>
<% if not loop.last %> \and <% endif %>
<% endfor %>
}
\date{<<date or "\\today">>}

\begin{document}
\maketitle

<% if abstract %>
\begin{abstract}
<<abstract>>
\end{abstract}
<% endif %>

<% if keywords %>
\textbf{Keywords:} <<keywords>>
<% endif %>

<% for section in sections %>
\section{<<section.title>>}
<<section.content>>
<% endfor %>

<% if acknowledgments %>
\section*{Acknowledgments}
<<acknowledgments>>
<% endif %>

<% if bibliography_file %>
\bibliographystyle{<<bibliography_style or "plain">>}
\bibliography{<<bibliography_file>>}
<% endif %>

\end{document}
```

### Resume Template

```latex
\documentclass[<<font_size or "11pt">>]{article}

\usepackage[margin=0.75in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}

\pagestyle{empty}
\setlength{\parindent}{0pt}

\begin{document}

% Header
\begin{center}
{\Large \textbf{<<personal_info.name>>}} \\
\vspace{0.5em}
<<personal_info.email>> | <<personal_info.phone>>
<% if personal_info.website %> | \href{<<personal_info.website>>}{<<personal_info.website>>}<% endif %>
\end{center}

\vspace{1em}

% Experience
<% if experience %>
\textbf{EXPERIENCE}
\hrule
\vspace{0.5em}

<% for job in experience %>
\textbf{<<job.title>>} \hfill <<job.dates>> \\
\textit{<<job.company>>}, <<job.location>> \\
<% for item in job.responsibilities %>
\begin{itemize}[leftmargin=1em, itemsep=0pt]
\item <<item>>
\end{itemize}
<% endfor %>
\vspace{0.5em}
<% endfor %>
<% endif %>

% Education
<% if education %>
\textbf{EDUCATION}
\hrule
\vspace{0.5em}

<% for degree in education %>
\textbf{<<degree.degree>>} \hfill <<degree.year>> \\
\textit{<<degree.institution>>}, <<degree.location>>
<% if degree.gpa %> | GPA: <<degree.gpa>><% endif %>
\vspace{0.5em}
<% endfor %>
<% endif %>

% Skills
<% if skills %>
\textbf{SKILLS}
\hrule
\vspace{0.5em}

<% for category, skill_list in skills.items() %>
\textbf{<<category>>:} <<skill_list | join(", ")>> \\
<% endfor %>
<% endif %>

\end{document}
```

## Best Practices

### Template Design

1. **Keep it simple**: Start with basic functionality and add complexity gradually
2. **Use meaningful variable names**: Choose descriptive names like `author_name` not just `author`
3. **Provide defaults**: Use sensible defaults for optional fields
4. **Test thoroughly**: Test with various input combinations
5. **Document everything**: Add comments explaining complex logic

### Configuration Design

1. **Group related fields**: Use sections to organize related fields
2. **Validate inputs**: Use field types and constraints to prevent errors
3. **Provide examples**: Include example values in descriptions
4. **Use clear labels**: Make field labels user-friendly
5. **Tag appropriately**: Use tags to help users find templates

### Error Handling

Add defensive checks in templates:

```latex
<% if not title %>
<# Error: title is required #>
\title{MISSING TITLE}
<% else %>
\title{<<title>>}
<% endif %>
```

## Testing Templates

### Unit Testing

Create test cases for your templates:

```yaml
# test-cases.yaml
test_cases:
  - name: "minimal_required"
    description: "Test with only required fields"
    variables:
      title: "Test Title"
      author: "Test Author"
      content: "Test content"
    
  - name: "full_features"
    description: "Test with all optional features"
    variables:
      title: "Full Test"
      author: "Test Author"
      date: "2024-01-01"
      abstract: "Test abstract"
      content: "Test content"
      include_toc: true
```

### Automated Testing

Create a test script:

```bash
#!/bin/bash

for test_case in test-cases/*.yaml; do
    echo "Testing $test_case"
    latex-engine generate my-template "output/$(basename $test_case .yaml).tex" \
      --template-dir . \
      --variables "$test_case"
    
    # Try to compile
    cd output
    pdflatex "$(basename $test_case .yaml).tex"
    cd ..
done
```

## Template Distribution

### Sharing Templates

1. **Create a template package**:
   ```
   my-templates/
   ├── README.md
   ├── template1.tex.j2
   ├── template1.yaml
   ├── template2.tex.j2
   ├── template2.yaml
   └── examples/
       ├── example1.yaml
       └── example2.yaml
   ```

2. **Document usage**:
   - Include README with installation and usage instructions
   - Provide example variable files
   - List required LaTeX packages

3. **Version your templates**:
   - Use semantic versioning in configuration files
   - Track changes in a changelog
   - Test compatibility with different LaTeX distributions

## Next Steps

- Read the [Configuration Reference](configuration.md) for detailed options
- Check out [Examples](examples.md) for real-world templates
- Learn about the [API Reference](api-reference.md) for programmatic usage
- Explore the [Contributing Guide](contributing.md) to share your templates
