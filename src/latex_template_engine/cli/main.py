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

import json
from pathlib import Path
from typing import Optional

# Click for command-line interface functionality
import click
import yaml

# Rich for enhanced console output
from rich.console import Console
from rich.table import Table

# Import core engine and configuration components
from ..assets.manager import AssetManager
from ..core.engine import TemplateEngine
from ..interactive import InteractiveSession

# Initialize Rich console for formatted output
console = Console()


def _open_pdf(pdf_path: Path) -> None:
    """Open PDF file with the system default viewer."""
    import platform
    import subprocess

    try:
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(pdf_path)])
        elif system == "Windows":
            subprocess.run(["start", str(pdf_path)], shell=True)
        elif system == "Linux":
            subprocess.run(["xdg-open", str(pdf_path)])
        else:
            console.print(f"[yellow]Please open {pdf_path} manually[/yellow]")
    except Exception as e:
        console.print(
            f"[yellow]Could not open PDF automatically: {e}[/yellow]\n"
            f"[dim]PDF location: {pdf_path}[/dim]"
        )


@click.group()
@click.version_option()
def cli() -> None:
    """LaTeX Template Engine - Generate LaTeX documents from Jinja2 templates.

    This is the main CLI entry point that sets up the command group.
    All subcommands are registered under this group.
    """
    pass


@cli.command()
@click.option(
    "--template-dir",
    "-t",
    type=click.Path(exists=True, path_type=Path),
    help="Directory containing templates",
)
def list_templates(template_dir: Optional[Path]) -> None:
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
@click.argument("template_name")
@click.argument("output_path", type=click.Path(path_type=Path))
@click.option(
    "--variables",
    "-v",
    type=click.Path(exists=True, path_type=Path),
    help="YAML/JSON file containing template variables",
)
@click.option(
    "--template-dir",
    "-t",
    type=click.Path(exists=True, path_type=Path),
    help="Directory containing templates",
)
def generate(
    template_name: str,
    output_path: Path,
    variables: Optional[Path],
    template_dir: Optional[Path],
) -> None:
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
        if variables.suffix.lower() in [".yaml", ".yml"]:
            with open(variables, "r") as f:
                vars_dict = yaml.safe_load(f)
        elif variables.suffix.lower() == ".json":
            with open(variables, "r") as f:
                vars_dict = json.load(f)
        else:
            raise click.BadParameter("Variables file must be YAML or JSON")

    try:
        # Generate the document
        engine.generate_document(template_name, vars_dict, output_path)
        console.print(f"[green]Generated document: {output_path}[/green]")
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Error generating document: {e}[/red]")
        raise click.Abort()


@cli.command()
@click.argument("template_name")
@click.option(
    "--template-dir",
    "-t",
    type=click.Path(exists=True, path_type=Path),
    help="Directory containing templates",
)
def info(template_name: str, template_dir: Optional[Path]) -> None:
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
                        field.description or "",
                    )

                # Display the fields table
                console.print(fields_table)
        else:
            console.print(
                f"[yellow]Template {template_name} has no configuration "
                f"file.[/yellow]"
            )

    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@cli.command()
@click.option(
    "--module",
    prompt="Module number",
    help="The module number for the assignment",
)
@click.option(
    "--type",
    prompt="Assignment type (e.g., casestudy, homework)",
    help="Type of assignment",
)
@click.option(
    "--title",
    prompt="Assignment title",
    help="Title of the assignment",
)
def uccs_workflow(module: str, type: str, title: str) -> None:
    """Workflow to generate and organize LaTeX files for your UCCS ME-SYSE progression.

    Automatically generates LaTeX files with proper naming and saves them to
    ./projects/uccs-me-syse/classes/EMGT5510/2025_summer/.

    Args:
        module: The module number for the assignment.
        type: Type of assignment.
        title: Title of the assignment.
    """
    import subprocess

    # Use local projects folder structure
    base_path = Path.cwd() / "projects/uccs-me-syse/classes/EMGT5510/2025_summer"
    base_path.mkdir(parents=True, exist_ok=True)

    # Create symlink to assets if it doesn't exist
    assets_link = base_path / "assets"
    if not assets_link.exists():
        assets_source = Path.cwd() / "assets"
        if assets_source.exists():
            assets_link.symlink_to(assets_source)
            console.print("[dim]Created assets symlink[/dim]")

    # Create filename following your existing naming convention
    safe_title = title.replace(" ", "").replace(".", "").lower()
    filename = f"EMGT5510_Module-{module}_{type.lower()}{safe_title}"
    tex_file = base_path / f"{filename}.tex"
    pdf_file = base_path / f"{filename}.pdf"

    # Start interactive session to use existing templates
    session = InteractiveSession()

    # Ask user to select template
    console.print("[bold blue]Starting UCCS Workflow[/bold blue]")
    console.print(f"Will save to: {tex_file}")
    console.print("\nSelect a template to use:")

    # Get templates and let user choose
    templates = session.engine.list_templates()
    if not templates:
        console.print("[red]No templates found![/red]")
        return

    # Display template options
    for i, template_name in enumerate(templates, 1):
        console.print(f"  {i}. {template_name}")

    while True:
        try:
            choice = click.prompt("Choose template", type=int)
            if 1 <= choice <= len(templates):
                selected_template = templates[choice - 1]
                break
            else:
                console.print("[red]Invalid choice. Please try again.[/red]")
        except (ValueError, click.Abort):
            console.print("[red]Invalid input. Please enter a number.[/red]")

    # Generate document using selected template
    loaded_template = session.engine.load_template(selected_template)

    # Collect field values
    field_values = {}
    if loaded_template.config and loaded_template.config.fields:
        console.print(f"\n[bold]Template: {loaded_template.config.name}[/bold]")
        console.print(f"Description: {loaded_template.config.description}\n")

        for field in loaded_template.config.fields:
            field_values[field.name] = session._get_field_value(field)

    # Generate the document
    session.engine.generate_document(selected_template, field_values, tex_file)
    console.print(f"[green]Generated LaTeX file: {tex_file}[/green]")

    # Compile the document
    console.print("\nCompiling LaTeX document...")
    result = subprocess.run(
        ["tectonic", str(tex_file)], capture_output=True, text=True, cwd=base_path
    )

    if result.returncode == 0:
        console.print(f"[green]✓ Generated PDF: {pdf_file}[/green]")

        # Ask if user wants to open the PDF
        if click.confirm("Open the generated PDF?"):
            subprocess.run(["open", str(pdf_file)])
    else:
        console.print(f"[red]Error compiling LaTeX: {result.stderr}[/red]")
        console.print("[yellow]LaTeX file saved but compilation failed.[/yellow]")


@cli.command()
@click.argument("tex_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--engine",
    "-e",
    type=click.Choice(["tectonic", "xelatex", "pdflatex", "lualatex"]),
    default="tectonic",
    help="LaTeX engine to use for compilation",
)
@click.option(
    "--open",
    "-o",
    is_flag=True,
    help="Open the generated PDF after compilation",
)
@click.option(
    "--auto-fallback",
    "-a",
    is_flag=True,
    help="Automatically try other engines if the selected one fails",
)
def compile(tex_file: Path, engine: str, open: bool, auto_fallback: bool) -> None:
    """Compile a LaTeX file to PDF.

    Args:
        tex_file: Path to the LaTeX file to compile.
        engine: LaTeX engine to use for compilation.
        open: Whether to open the PDF after compilation.
    """
    import subprocess

    pdf_file = tex_file.with_suffix(".pdf")

    if auto_fallback:
        # Try engines in order of preference with fallback
        # Tectonic can handle full paths, others need just the filename
        engines = [
            ("tectonic", ["tectonic", str(tex_file)]),
            ("xelatex", ["xelatex", "-interaction=nonstopmode", tex_file.name]),
            ("pdflatex", ["pdflatex", "-interaction=nonstopmode", tex_file.name]),
            ("lualatex", ["lualatex", "-interaction=nonstopmode", tex_file.name]),
        ]

        # Move selected engine to front if it's not tectonic
        if engine != "tectonic":
            engines = [
                (engine, [engine, "-interaction=nonstopmode", tex_file.name])
            ] + engines
            # Remove duplicate
            engines = list(dict.fromkeys(engines))

        # Try each engine until one works
        for engine_name, command in engines:
            try:
                console.print(
                    f"[blue]Compiling {tex_file} with {engine_name}...[/blue]"
                )
                result = subprocess.run(
                    command, capture_output=True, text=True, cwd=tex_file.parent
                )

                if result.returncode == 0:
                    console.print(
                        f"[green]✓ PDF generated with {engine_name}: {pdf_file}[/green]"
                    )
                    if open:
                        _open_pdf(pdf_file)
                    return
                else:
                    console.print(
                        f"[yellow]{engine_name} failed, trying next engine...[/yellow]"
                    )
                    if engine_name == "tectonic":
                        console.print(f"[dim]Error: {result.stderr.strip()}[/dim]")

            except FileNotFoundError:
                console.print(
                    f"[dim]{engine_name} not found, trying next engine...[/dim]"
                )
                continue
            except Exception as e:
                console.print(
                    f"[yellow]{engine_name} error: {e}, trying next engine...[/yellow]"
                )
                continue

        # If no engine worked
        console.print("[red]LaTeX compilation failed with all engines![/red]")
        console.print(
            "[yellow]Please install one of the following LaTeX engines:[/yellow]"
        )
        console.print(
            "  • Tectonic (recommended): https://tectonic-typesetting.github.io/"
        )
        console.print("  • XeLaTeX (supports Unicode): Part of TeX Live/MiKTeX")
        console.print("  • pdfLaTeX (traditional): Part of TeX Live/MiKTeX")
        console.print("  • LuaLaTeX (modern): Part of TeX Live/MiKTeX")
        raise click.Abort()
    else:
        # Single engine compilation
        try:
            console.print(f"[blue]Compiling {tex_file} with {engine}...[/blue]")

            # Define command for selected engine
            # Tectonic can handle full paths, others need just the filename
            if engine == "tectonic":
                command = ["tectonic", str(tex_file)]
            else:
                command = [engine, "-interaction=nonstopmode", tex_file.name]

            # Run the compilation command
            result = subprocess.run(
                command, capture_output=True, text=True, cwd=tex_file.parent
            )

            if result.returncode == 0:
                console.print(f"[green]✓ PDF generated: {pdf_file}[/green]")
                if open:
                    _open_pdf(pdf_file)
            else:
                console.print(f"[red]Error compiling LaTeX with {engine}![/red]")
                console.print(f"[dim]{result.stderr.strip()}[/dim]")
                if engine != "tectonic":
                    console.print(
                        "[yellow]Consider trying with --auto-fallback "
                        "to try other engines.[/yellow]"
                    )
                raise click.Abort()

        except FileNotFoundError:
            console.print(f"[red]LaTeX engine '{engine}' not found.[/red]")
            console.print(
                "[yellow]Please ensure the engine is installed and accessible "
                "in your PATH.[/yellow]"
            )
            if not auto_fallback:
                console.print(
                    "[yellow]Or use --auto-fallback to try other engines "
                    "automatically.[/yellow]"
                )
            raise click.Abort()
        except Exception as e:
            console.print(f"[red]Unexpected error during compilation: {e}[/red]")
            raise click.Abort()


@cli.command()
@click.option(
    "--template-dir",
    "-t",
    type=click.Path(exists=True, path_type=Path),
    help="Directory containing templates",
)
def interactive(template_dir: Optional[Path]) -> None:
    """Start interactive document creator.

    Launches an interactive CLI session that guides users through
    template selection, field input, and document generation.
    Perfect for LaTeX novices who want a guided experience.

    Args:
        template_dir: Optional directory containing templates.
    """
    session = InteractiveSession(template_dir)
    session.start()


@cli.command()
@click.option(
    "--action",
    "-a",
    type=click.Choice(["setup", "list"]),
    default="setup",
    help="Asset management action: setup fonts/images or list existing assets",
)
def assets(action: str) -> None:
    """Manage fonts, images, and other template assets.

    This command allows you to import fonts and images into the project
    structure, making them available for use in templates.

    Args:
        action: Either 'setup' to import new assets or 'list' to show existing ones.
    """
    asset_manager = AssetManager()

    if action == "setup":
        console.print("[bold blue]Asset Setup[/bold blue]")
        console.print("Setting up fonts and images for templates...\n")

        asset_config = asset_manager.setup_assets_interactive()

        if asset_config:
            console.print("\n[green]✓ Asset setup complete![/green]")
            asset_manager.list_assets()
        else:
            console.print("[yellow]Asset setup cancelled[/yellow]")

    elif action == "list":
        asset_manager.list_assets()


@cli.command()
@click.option(
    "--template-dir",
    "-t",
    type=click.Path(path_type=Path),
    help="Directory to create templates in",
)
def init(template_dir: Optional[Path]) -> None:
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
    example_template = r"""\documentclass[<<document_class_options>>]{<<\
        document_class>>}

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

\end{document}"""

    # Save the example template to a file
    (template_dir / "example.tex.j2").write_text(example_template)

    # Create a proper YAML configuration without Python object references
    config_dict = {
        "name": "Example Template",
        "description": "A simple example template",
        "document_type": "article",
        "author": "LaTeX Template Engine",
        "version": "1.0.0",
        "fields": [
            {
                "name": "title",
                "type": "string",
                "label": "Document Title",
                "description": "The title of the document",
                "required": True,
            },
            {
                "name": "author",
                "type": "string",
                "label": "Author",
                "description": "The author of the document",
                "required": True,
            },
            {
                "name": "date",
                "type": "string",
                "label": "Date",
                "description": "The date of the document",
                "required": False,
                "default": "\\today",
            },
            {
                "name": "abstract",
                "type": "string",
                "label": "Abstract",
                "description": "Optional abstract for the document",
                "required": False,
            },
            {
                "name": "introduction",
                "type": "string",
                "label": "Introduction",
                "description": "Introduction section content",
                "required": True,
            },
        ],
        "packages": ["geometry", "amsmath", "amsfonts"],
        "document_class": "article",
        "class_options": ["12pt", "letterpaper"],
        "tags": ["academic", "article", "example"],
    }

    # Save the example config to a YAML file
    config_file = template_dir / "example.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)

    # Confirm creation with console output
    msg = f"[green]Initialized template directory: {template_dir}[/green]"
    console.print(msg)
    template_file = template_dir / "example.tex.j2"
    console.print(f"[dim]Created example template: {template_file}[/dim]")
    console.print(f"[dim]Created example config: {config_file}[/dim]")


def main() -> None:
    """Entry point for the CLI.

    This function is the main entry point for executing the CLI commands.
    It sets up the Click command group and delegates to the appropriate
    command based on the arguments provided by the user.
    """
    cli()


if __name__ == "__main__":
    # Executes the CLI when the module is run as a script
    main()
