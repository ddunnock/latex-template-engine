"""Command-line interface for the LaTeX Template Engine.

This module implements the CLI commands for the LaTeX template engine using
the Click library for command-line parsing and Rich for enhanced output
formatting. The CLI provides a comprehensive interface for template
management and document generation.

Commands:
    list-templates: Display all available templates in a formatted table
    generate: Generate a LaTeX document from a template with variables
    info: Show detailed information about a specific template
    init: Initialize a new template directory with example templates

The CLI is designed to be user-friendly with:
- Rich console output with tables and colors
- Comprehensive help text for all commands
- Error handling with informative messages
- Support for both YAML and JSON variable files
"""

from pathlib import Path
from typing import Optional
import json
import yaml

# Click for command-line interface functionality
import click
# Rich for enhanced console output
from rich.console import Console
from rich.table import Table
from rich.text import Text

# Import core engine and configuration components
from ..core.engine import TemplateEngine
from ..config.schema import TemplateConfig

# Initialize Rich console for formatted output
console = Console()


@click.group()
@click.version_option()
def cli():
    """LaTeX Template Engine - Generate LaTeX documents from Jinja2 templates.
    
    This is the main CLI entry point that sets up the command group.
    All subcommands are registered under this group.
    """
    pass


@cli.command()
@click.option('--template-dir', '-t', type=click.Path(exists=True, path_type=Path),
              help='Directory containing templates')
def list_templates(template_dir: Optional[Path]):
    """List all available templates.
    
    Scans the template directory for .tex files and displays them in a
    formatted table showing template names and their full paths.
    
    Args:
        template_dir: Optional directory to search for templates.
                     If not provided, uses the default template directory.
    """
    # Initialize the template engine with the specified or default directory
    engine = TemplateEngine(template_dir)
    templates = engine.list_templates()
    
    # Handle case where no templates are found
    if not templates:
        console.print("[yellow]No templates found.[/yellow]")
        return
    
    # Create and populate a Rich table for template display
    table = Table(title="Available Templates")
    table.add_column("Name", style="cyan")
    table.add_column("Path", style="dim")
    
    # Add each template to the table
    for template in templates:
        template_path = engine.template_dir / f"{template}.tex.j2"
        table.add_row(template, str(template_path))
    
    # Display the table using Rich console
    console.print(table)


@cli.command()
@click.argument('template_name')
@click.argument('output_path', type=click.Path(path_type=Path))
@click.option('--variables', '-v', type=click.Path(exists=True, path_type=Path),
              help='YAML/JSON file containing template variables')
@click.option('--template-dir', '-t', type=click.Path(exists=True, path_type=Path),
              help='Directory containing templates')
def generate(template_name: str, output_path: Path, variables: Optional[Path], 
             template_dir: Optional[Path]):
    """Generate a LaTeX document from a template.

    This command generates a LaTeX document by applying the specified
    variables to a chosen template. The output is written to the specified
    output path.

    Args:
        template_name: Name of the template to render.
        output_path: Path to save the generated output document.
        variables: Optional path to a YAML/JSON file with template variables.
        template_dir: Optional directory containing templates.
    """
    # Initialize engine with given or default template directory
    engine = TemplateEngine(template_dir)
    
    # Load variables from file if provided
    vars_dict = {}
    if variables:
        if variables.suffix.lower() in ['.yaml', '.yml']:
            with open(variables, 'r') as f:
                vars_dict = yaml.safe_load(f)
        elif variables.suffix.lower() == '.json':
            with open(variables, 'r') as f:
                vars_dict = json.load(f)
        else:
            raise click.BadParameter("Variables file must be YAML or JSON")
    
    try:
        # Generate the document
        content = engine.generate_document(template_name, vars_dict, output_path)
        console.print(f"[green]Generated document: {output_path}[/green]")
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Error generating document: {e}[/red]")
        raise click.Abort()


@cli.command()
@click.argument('template_name')
@click.option('--template-dir', '-t', type=click.Path(exists=True, path_type=Path),
              help='Directory containing templates')
def info(template_name: str, template_dir: Optional[Path]):
    """Show information about a template.

    Displays detailed information about the specified template, including
    metadata, fields, and configuration details.

    Args:
        template_name: Name of the template to inspect.
        template_dir: Optional directory containing templates.
    """
    # Initialize the template engine
    engine = TemplateEngine(template_dir)
    
    try:
        # Load the specified template
        template = engine.load_template(template_name)
        
        # Check if the template configuration exists
        if template.config:
            config = template.config
            
            # Create and populate a Rich table for template metadata
            table = Table(title=f"Template: {config.name}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="white")
            
            # Add template metadata to the table
            table.add_row("Description", config.description)
            table.add_row("Document Type", config.document_type)
            table.add_row("Version", config.version)
            if config.author:
                table.add_row("Author", config.author)
            
            # Display the metadata table
            console.print(table)
            
            # If fields exist, create and display a table for them
            if config.fields:
                fields_table = Table(title="Template Fields")
                fields_table.add_column("Name", style="cyan")
                fields_table.add_column("Type", style="yellow")
                fields_table.add_column("Required", style="red")
                fields_table.add_column("Description", style="dim")
                
                # Populate the fields table
                for field in config.fields:
                    fields_table.add_row(
                        field.name,
                        field.type,
                        "Yes" if field.required else "No",
                        field.description or ""
                    )
                
                # Display the fields table
                console.print(fields_table)
        else:
            console.print(f"[yellow]Template {template_name} has no configuration file.[/yellow]")
            
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@cli.command()
@click.option('--template-dir', '-t', type=click.Path(path_type=Path),
              help='Directory to create templates in')
def init(template_dir: Optional[Path]):
    """Initialize a new template directory with examples.

    Sets up a new template directory and populates it with example LaTeX
    templates and configuration files.

    Args:
        template_dir: Directory path to create template-related files in.
                      Defaults to './templates' if not specified.
    """
    # Default to creating a 'templates' directory if none is specified
    if template_dir is None:
        template_dir = Path.cwd() / "templates"
    
    # Ensure the directory exists
    template_dir.mkdir(exist_ok=True)
    
    # Define an example LaTeX template
    example_template = r'''\documentclass[<<document_class_options>>]{<<document_class>>}

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

\end{document}'''
    
    # Save the example template to a file
    (template_dir / "example.tex.j2").write_text(example_template)
    
    # Define an example configuration
    example_config = TemplateConfig(
        name="Example Template",
        description="A simple example template",
        document_type="article",
        author="LaTeX Template Engine",
        fields=[
            {"name": "title", "type": "string", "label": "Document Title", "required": True},
            {"name": "author", "type": "string", "label": "Author", "required": True},
            {"name": "date", "type": "date", "label": "Date", "default": "\\today"},
            {"name": "abstract", "type": "string", "label": "Abstract", "required": False},
            {"name": "introduction", "type": "string", "label": "Introduction", "required": True},
        ],
        packages=["geometry", "amsmath", "amsfonts"],
        document_class="article",
        class_options=["12pt", "letterpaper"],
        tags=["academic", "article", "example"]
    )
    
    # Save the example config to a YAML file
    (template_dir / "example.yaml").write_text(example_config.model_dump_yaml())
    
    # Confirm creation with console output
    console.print(f"[green]Initialized template directory: {template_dir}[/green]")
    console.print(f"[dim]Created example template: {template_dir / 'example.tex.j2'}[/dim]")
    console.print(f"[dim]Created example config: {template_dir / 'example.yaml'}[/dim]")


def main():
    """Entry point for the CLI.

    This function is the main entry point for executing the CLI commands.
    It sets up the Click command group and delegates to the appropriate
    command based on the arguments provided by the user.
    """
    cli()


if __name__ == '__main__':
    # Executes the CLI when the module is run as a script
    main()
