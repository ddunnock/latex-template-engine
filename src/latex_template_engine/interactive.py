"""Interactive CLI interface for creating LaTeX documents from templates."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import click
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, FloatPrompt, IntPrompt, Prompt
from rich.table import Table

from .assets.manager import AssetManager
from .config.schema import TemplateConfig
from .core.engine import TemplateEngine


class InteractiveSession:
    """Manages an interactive session for creating LaTeX documents."""

    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize the interactive session."""
        self.console = Console()
        self.engine = TemplateEngine(template_dir)
        self.template_config: Optional[TemplateConfig] = None
        self.template_variables: Dict[str, Any] = {}
        self.user_data: Dict[str, Any] = {}
        self.asset_manager = AssetManager()

    def start(self) -> None:
        """Start the interactive session."""
        self.console.print(
            Panel.fit(
                "[bold blue]LaTeX Template Engine[/bold blue]\n"
                "Interactive Document Creator",
                border_style="blue",
            )
        )

        # Step 1: Choose action
        action = self._choose_action()
        if action == "setup":
            self._setup_assets()
            return
        elif action == "list":
            self.asset_manager.list_assets()
            return
        elif action != "create":
            return

        # Step 2: Choose template
        template_name = self._choose_template()
        if not template_name:
            return

        # Step 3: Load template configuration
        self._load_template_config(template_name)

        # Step 4: Collect user input
        self._collect_user_input()

        # Step 5: Preview configuration
        if self._preview_and_confirm():
            # Step 6: Generate document
            self._generate_document(template_name)

    def _choose_action(self) -> str:
        """Let user choose what they want to do."""
        self.console.print("\n[bold]What would you like to do?[/bold]")

        actions = [
            ("create", "Create a new document from template"),
            ("setup", "Set up fonts and images for templates"),
            ("list", "List available assets"),
            ("exit", "Exit"),
        ]

        table = Table()
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Action", style="magenta")
        table.add_column("Description", style="green")

        for i, (action, description) in enumerate(actions, 1):
            table.add_row(str(i), action.title(), description)

        self.console.print(table)

        try:
            choice = IntPrompt.ask("Select action by ID", default=1, show_default=True)
            if 1 <= choice <= len(actions):
                return actions[choice - 1][0]
            else:
                self.console.print("[red]Invalid choice![/red]")
                return "exit"
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Cancelled by user[/yellow]")
            return "exit"

    def _setup_assets(self) -> None:
        """Set up fonts and images for templates."""
        asset_config = self.asset_manager.setup_assets_interactive()

        if asset_config:
            self.console.print("\n[green]✓ Asset setup complete![/green]")
            self.console.print("Assets are now available for use in templates.")

            # Show summary
            self.asset_manager.list_assets()

            if Confirm.ask("\nWould you like to create a document now?", default=True):
                # Continue to document creation
                template_name = self._choose_template()
                if template_name:
                    self._load_template_config(template_name)
                    self._collect_user_input()
                    if self._preview_and_confirm():
                        self._generate_document(template_name)
        else:
            self.console.print("[yellow]Asset setup cancelled[/yellow]")

    def _choose_template(self) -> Optional[str]:
        """Let user choose from available templates."""
        templates = self.engine.list_templates()

        if not templates:
            self.console.print("[red]No templates found![/red]")
            return None

        # Display templates in a table
        table = Table(title="Available Templates")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Type", style="yellow")

        for i, template in enumerate(templates, 1):
            # Load config to get metadata
            try:
                config_path = self.engine.template_dir / f"{template}.yaml"
                with open(config_path) as f:
                    config_data = yaml.safe_load(f)

                table.add_row(
                    str(i),
                    config_data.get("name", template),
                    config_data.get("description", "No description"),
                    config_data.get("document_type", "unknown"),
                )
            except FileNotFoundError:
                table.add_row(str(i), template, "No config found", "unknown")

        self.console.print(table)

        # Get user choice
        try:
            choice = IntPrompt.ask(
                "Select template by ID", default=1, show_default=True
            )
            if 1 <= choice <= len(templates):
                return templates[choice - 1]
            else:
                self.console.print("[red]Invalid choice![/red]")
                return None
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Cancelled by user[/yellow]")
            return None

    def _load_template_config(self, template_name: str) -> None:
        """Load the template configuration."""
        try:
            config_path = self.engine.template_dir / f"{template_name}.yaml"
            with open(config_path) as f:
                config_data = yaml.safe_load(f)

            # Extract template config fields (metadata)
            template_config_fields = {
                "name": config_data.get("name", template_name),
                "description": config_data.get("description", "No description"),
                "document_type": config_data.get("document_type", "article"),
                "author": config_data.get("author"),
                "version": config_data.get("version", "1.0.0"),
                "fields": config_data.get("fields", []),
                "sections": config_data.get("sections", []),
                "packages": config_data.get("packages", []),
                "document_class": config_data.get("document_class", "article"),
                "class_options": config_data.get("class_options", []),
                "tags": config_data.get("tags", []),
                "preview_image": config_data.get("preview_image"),
            }
            self.template_config = TemplateConfig(**template_config_fields)

            # Load template variables (everything except config metadata)
            excluded_keys = {
                "name",
                "description",
                "document_type",
                "author",
                "version",
                "fields",
                "sections",
                "packages",
                "document_class",
                "class_options",
                "tags",
                "preview_image",
            }
            self.template_variables = {
                k: v for k, v in config_data.items() if k not in excluded_keys
            }

            self.console.print(
                f"\n[green]Loaded template:[/green] {self.template_config.name}"
            )
            self.console.print(f"[dim]{self.template_config.description}[/dim]")

        except Exception as e:
            self.console.print(f"[red]Error loading template config: {e}[/red]")
            raise

    def _collect_user_input(self) -> None:
        """Collect input for all template fields."""
        if not self.template_config:
            return

        self.console.print(f"\n[bold]Configuring {self.template_config.name}[/bold]")

        for field in self.template_config.fields:
            self.console.print(f"\n[cyan]{field.label}[/cyan]")
            if field.description:
                self.console.print(f"[dim]{field.description}[/dim]")

            value = self._get_field_value(field)
            if value is not None:
                # Handle nested field names like "student.name", "course.id"
                self._set_nested_value(self.user_data, field.name, value)

        # Update template variables with asset paths
        self.user_data = self.asset_manager.update_template_variables(self.user_data)

        # Handle dynamic problem creation for homework template
        if self.template_config and self.template_config.name == "homework":
            self._collect_problem_details()

    def _set_nested_value(self, data: Dict[str, Any], key: str, value: Any) -> None:
        """Set a nested value in a dictionary using dot notation.

        Args:
            data: The dictionary to modify
            key: The nested key (e.g., "student.name", "course.id")
            value: The value to set
        """
        keys = key.split(".")
        current = data

        # Navigate to the parent of the final key
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        # Set the final value
        current[keys[-1]] = value

    def _collect_problem_details(self) -> None:
        """Collect details for each problem in the homework assignment."""
        num_problems = self.user_data.get("num_problems", 4)

        self.console.print("\n[bold blue]Problem Details[/bold blue]")
        self.console.print(f"Please provide details for {num_problems} problems.\n")

        problems = []
        for i in range(1, num_problems + 1):
            self.console.print(f"[bold cyan]Problem {i}[/bold cyan]")

            # Get problem title
            title = Prompt.ask(f"Enter title for Problem {i}", default=f"Problem {i}")

            # Get problem description
            description = Prompt.ask(
                f"Enter problem description for Problem {i}",
                default=f"Problem {i} description goes here.",
            )

            problems.append(
                {
                    "title": title,
                    "description": description,
                    "answer": None,  # Will be filled in by the student
                }
            )

            self.console.print(f"[green]✓ Problem {i} details saved[/green]\n")

        self.user_data["problems"] = problems

    def _get_field_value(self, field: Any) -> Any:
        """Get a value for a specific field based on its type."""
        if field.type == "string":
            return self._get_string_value(field)
        elif field.type == "multiline":
            return self._get_multiline_value(field)
        elif field.type == "integer":
            return self._get_integer_value(field)
        elif field.type == "float":
            return self._get_float_value(field)
        elif field.type == "boolean":
            return self._get_boolean_value(field)
        elif field.type == "choice":
            return self._get_choice_value(field)
        elif field.type == "list":
            return self._get_list_value(field)
        else:
            # Fallback to string
            return self._get_string_value(field)

    def _get_string_value(self, field: Any) -> Optional[str]:
        """Get string input from user."""
        default = getattr(field, "default", None)
        required = getattr(field, "required", False)

        if not required and default is None:
            default = ""

        try:
            value = Prompt.ask(
                f"Enter {field.label.lower()}",
                default=default,
                show_default=bool(default),
            )
            return value if value or not required else None
        except KeyboardInterrupt:
            return None

    def _get_multiline_value(self, field: Any) -> Optional[str]:
        """Get multiline input from user."""
        self.console.print(
            "[dim]Enter text (press Ctrl+D when done, Ctrl+C to skip):[/dim]"
        )
        lines = []
        try:
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
            return "\\n".join(lines) if lines else None
        except KeyboardInterrupt:
            return None

    def _get_integer_value(self, field: Any) -> Optional[int]:
        """Get integer input from user."""
        default = getattr(field, "default", None)
        min_val = getattr(field, "min_value", None)
        max_val = getattr(field, "max_value", None)

        try:
            value = IntPrompt.ask(
                f"Enter {field.label.lower()}",
                default=default,
                show_default=bool(default is not None),
            )

            if min_val is not None and value < min_val:
                self.console.print(f"[red]Value must be at least {min_val}[/red]")
                return self._get_integer_value(field)

            if max_val is not None and value > max_val:
                self.console.print(f"[red]Value must be at most {max_val}[/red]")
                return self._get_integer_value(field)

            return value
        except KeyboardInterrupt:
            return None

    def _get_float_value(self, field: Any) -> Optional[float]:
        """Get float input from user."""
        default = getattr(field, "default", None)
        min_val = getattr(field, "min_value", None)
        max_val = getattr(field, "max_value", None)

        try:
            value = FloatPrompt.ask(
                f"Enter {field.label.lower()}",
                default=default,
                show_default=bool(default is not None),
            )

            if min_val is not None and value < min_val:
                self.console.print(f"[red]Value must be at least {min_val}[/red]")
                return self._get_float_value(field)

            if max_val is not None and value > max_val:
                self.console.print(f"[red]Value must be at most {max_val}[/red]")
                return self._get_float_value(field)

            return value
        except KeyboardInterrupt:
            return None

    def _get_boolean_value(self, field: Any) -> Optional[bool]:
        """Get boolean input from user."""
        default = getattr(field, "default", None)

        try:
            return Confirm.ask(
                f"{field.label}?",
                default=default,
                show_default=bool(default is not None),
            )
        except KeyboardInterrupt:
            return None

    def _get_choice_value(self, field: Any) -> Optional[str]:
        """Get choice input from user."""
        choices = getattr(field, "choices", [])
        if not choices:
            return self._get_string_value(field)

        self.console.print("Available choices:")
        for i, choice in enumerate(choices, 1):
            self.console.print(f"  {i}. {choice}")

        try:
            choice_idx = IntPrompt.ask(
                f"Select {field.label.lower()} by number", default=1, show_default=True
            )
            if 1 <= choice_idx <= len(choices):
                return str(choices[choice_idx - 1])
            else:
                self.console.print("[red]Invalid choice![/red]")
                return self._get_choice_value(field)
        except KeyboardInterrupt:
            return None

    def _get_list_value(self, field: Any) -> Optional[List[str]]:
        """Get list input from user."""
        self.console.print(
            f"Enter items for {field.label.lower()}"
            " (one per line, empty line to finish):"
        )
        items: List[str] = []

        try:
            while True:
                item = Prompt.ask(f"Item {len(items) + 1}", default="")
                if not item:
                    break
                items.append(item)
            return items if items else None
        except KeyboardInterrupt:
            return None

    def _preview_and_confirm(self) -> bool:
        """Show preview of configuration and ask for confirmation."""
        self.console.print("\n[bold]Configuration Preview:[/bold]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        for key, value in self.user_data.items():
            if isinstance(value, list):
                value_str = ", ".join(str(v) for v in value)
            else:
                value_str = str(value)
            table.add_row(key, value_str)

        self.console.print(table)

        return Confirm.ask(
            "\nGenerate LaTeX document with this configuration?", default=True
        )

    def _generate_document(self, template_name: str) -> None:
        """Generate the final LaTeX document."""
        try:
            # Generate output filename
            output_name = (
                self.user_data.get("title", "document").lower().replace(" ", "_")
            )
            output_path = Path(f"{output_name}.tex")

            # Check if file exists
            if output_path.exists():
                if not Confirm.ask(
                    f"File {output_path} exists. Overwrite?", default=False
                ):
                    output_path = Path(
                        Prompt.ask(
                            "Enter new filename", default=f"{output_name}_new.tex"
                        )
                    )

            # Merge template variables with user data
            # User data takes precedence over template defaults
            merged_data = {**self.template_variables, **self.user_data}

            # Generate document
            self.engine.generate_document(template_name, merged_data, output_path)

            self.console.print("\n[green]✓ Document generated successfully![/green]")
            self.console.print(f"[green]Output:[/green] {output_path}")

            # Optionally compile
            if Confirm.ask("Compile LaTeX document now?", default=True):
                self._compile_document(output_path)

        except Exception as e:
            self.console.print(f"[red]Error generating document: {e}[/red]")

    def _compile_document(self, tex_path: Path) -> None:
        """Compile the LaTeX document using available engines."""
        import subprocess

        # Define compilation engines in order of preference
        engines = [
            ("tectonic", ["tectonic", str(tex_path)]),
            ("xelatex", ["xelatex", "-interaction=nonstopmode", str(tex_path)]),
            ("pdflatex", ["pdflatex", "-interaction=nonstopmode", str(tex_path)]),
            ("lualatex", ["lualatex", "-interaction=nonstopmode", str(tex_path)]),
        ]

        # Try each engine until one works
        for engine_name, command in engines:
            try:
                self.console.print(
                    f"[yellow]Compiling {tex_path} with {engine_name}...[/yellow]"
                )

                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    cwd=tex_path.parent,
                )

                if result.returncode == 0:
                    pdf_path = tex_path.with_suffix(".pdf")
                    self.console.print(
                        f"[green]✓ PDF generated with {engine_name}:[/green] {pdf_path}"
                    )

                    if Confirm.ask("Open PDF?", default=True):
                        self._open_pdf(pdf_path)
                    return
                else:
                    self.console.print(
                        f"[yellow]{engine_name} failed, trying next engine...[/yellow]"
                    )
                    if engine_name == "tectonic" or "--verbose" in str(result.stderr):
                        self.console.print(f"[dim]Error: {result.stderr.strip()}[/dim]")

            except FileNotFoundError:
                self.console.print(
                    f"[dim]{engine_name} not found, trying next engine...[/dim]"
                )
                continue
            except Exception as e:
                self.console.print(
                    f"[yellow]{engine_name} error: {e}, trying next engine...[/yellow]"
                )
                continue

        # If no engine worked
        self.console.print(
            "[red]LaTeX compilation failed![/red]\n"
            "[yellow]Please install one of the following LaTeX engines:[/yellow]\n"
            "  • Tectonic (recommended): https://tectonic-typesetting.github.io/\n"
            "  • XeLaTeX (supports Unicode): Part of TeX Live/MiKTeX\n"
            "  • pdfLaTeX (traditional): Part of TeX Live/MiKTeX\n"
            "  • LuaLaTeX (modern): Part of TeX Live/MiKTeX"
        )

    def _open_pdf(self, pdf_path: Path) -> None:
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
                self.console.print(f"[yellow]Please open {pdf_path} manually[/yellow]")
        except Exception as e:
            self.console.print(
                f"[yellow]Could not open PDF automatically: {e}[/yellow]\n"
                f"[dim]PDF location: {pdf_path}[/dim]"
            )


@click.command()
@click.option(
    "--template-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Directory containing templates",
)
def interactive(template_dir: Optional[Path]) -> None:
    """Start interactive LaTeX document creator."""
    session = InteractiveSession(template_dir)
    session.start()


if __name__ == "__main__":
    interactive()
