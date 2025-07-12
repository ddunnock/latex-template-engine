"""Asset manager for handling fonts, images, and other template resources.

This module provides functionality to:
- Import fonts and images from external sources
- Copy assets to the project structure
- Manage asset paths for templates
- Validate asset integrity
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table


class AssetManager:
    """Manages fonts, images, and other assets for LaTeX templates.

    The AssetManager provides a centralized way to handle template assets,
    ensuring they are properly organized and accessible to templates.
    """

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the asset manager.

        Args:
            project_root: Root directory of the project. If None, uses
                current directory.
        """
        self.project_root = project_root or Path.cwd()
        self.assets_dir = self.project_root / "assets"
        self.fonts_dir = self.assets_dir / "fonts"
        self.images_dir = self.assets_dir / "images"
        self.console = Console()

        # Ensure asset directories exist
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create asset directories if they don't exist."""
        self.assets_dir.mkdir(exist_ok=True)
        self.fonts_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)

    def setup_assets_interactive(self) -> Dict[str, str]:
        """Interactive setup of fonts and images for templates.

        Returns:
            Dict containing asset configuration with updated paths.
        """
        self.console.print("\n[bold blue]Asset Setup[/bold blue]")
        self.console.print("Let's set up the fonts and images for your templates.\n")

        config = {}

        # Handle fonts
        if Confirm.ask("Do you want to import fonts?", default=True):
            config.update(self._setup_fonts_interactive())

        # Handle images
        if Confirm.ask("Do you want to import images?", default=True):
            config.update(self._setup_images_interactive())

        return config

    def _setup_fonts_interactive(self) -> Dict[str, str]:
        """Interactive font setup."""
        self.console.print("\n[cyan]Font Setup[/cyan]")
        self.console.print(
            "Please provide paths to font files (or directory containing fonts)"
        )

        font_config = {}

        # Common font types for UCCS templates
        font_families = [
            ("main_font", "Main text font (e.g., FiraSans-Regular.otf)"),
            ("heading_font", "Heading font (e.g., FiraSans-Light.otf)"),
            ("bold_font", "Bold font (e.g., FiraSans-Bold.otf)"),
            ("italic_font", "Italic font (e.g., FiraSans-Italic.otf)"),
        ]

        for font_key, description in font_families:
            font_path = Prompt.ask(f"{description}", default="skip")

            if font_path.lower() != "skip":
                copied_path = self._import_font(font_path)
                if copied_path:
                    font_config[font_key] = str(
                        copied_path.relative_to(self.project_root)
                    )

        # Check if we have a font directory to import
        font_dir = Prompt.ask(
            "Or provide a directory path containing all font files", default="skip"
        )

        if font_dir.lower() != "skip":
            imported_fonts = self._import_font_directory(font_dir)
            if imported_fonts:
                font_config["font_directory"] = str(
                    self.fonts_dir.relative_to(self.project_root)
                )

        return font_config

    def _setup_images_interactive(self) -> Dict[str, str]:
        """Interactive image setup."""
        self.console.print("\n[cyan]Image Setup[/cyan]")
        self.console.print("Please provide paths to image files")

        image_config = {}

        # Common images for UCCS templates
        image_types = [
            ("logo", "University/Organization logo (e.g., uccs-logo.png)"),
            ("signature", "Signature image (optional)"),
            ("header_image", "Header/banner image (optional)"),
        ]

        for image_key, description in image_types:
            image_path = Prompt.ask(f"{description}", default="skip")

            if image_path.lower() != "skip":
                copied_path = self._import_image(image_path)
                if copied_path:
                    image_config[image_key] = str(
                        copied_path.relative_to(self.project_root)
                    )

        # Check if we have an image directory to import
        image_dir = Prompt.ask(
            "Or provide a directory path containing image files", default="skip"
        )

        if image_dir.lower() != "skip":
            imported_images = self._import_image_directory(image_dir)
            if imported_images:
                image_config["image_directory"] = str(
                    self.images_dir.relative_to(self.project_root)
                )

        return image_config

    def _import_font(self, font_path: str) -> Optional[Path]:
        """Import a single font file.

        Args:
            font_path: Path to the font file

        Returns:
            Path to the copied font file, or None if import failed
        """
        try:
            source = Path(font_path).expanduser().resolve()

            if not source.exists():
                self.console.print(f"[red]Font file not found: {source}[/red]")
                return None

            if not source.suffix.lower() in [".otf", ".ttf", ".woff", ".woff2"]:
                self.console.print(
                    f"[yellow]Warning: {source} may not be a valid font file[/yellow]"
                )

            destination = self.fonts_dir / source.name

            if destination.exists():
                if not Confirm.ask(
                    f"Font {source.name} already exists. Overwrite?", default=False
                ):
                    return destination

            shutil.copy2(source, destination)
            self.console.print(f"[green]✓ Imported font: {source.name}[/green]")
            return destination

        except Exception as e:
            self.console.print(f"[red]Error importing font {font_path}: {e}[/red]")
            return None

    def _import_image(self, image_path: str) -> Optional[Path]:
        """Import a single image file.

        Args:
            image_path: Path to the image file

        Returns:
            Path to the copied image file, or None if import failed
        """
        try:
            source = Path(image_path).expanduser().resolve()

            if not source.exists():
                self.console.print(f"[red]Image file not found: {source}[/red]")
                return None

            if not source.suffix.lower() in [
                ".png",
                ".jpg",
                ".jpeg",
                ".pdf",
                ".eps",
                ".svg",
            ]:
                self.console.print(
                    f"[yellow]Warning: {source} may not be a valid image file[/yellow]"
                )

            destination = self.images_dir / source.name

            if destination.exists():
                if not Confirm.ask(
                    f"Image {source.name} already exists. Overwrite?", default=False
                ):
                    return destination

            shutil.copy2(source, destination)
            self.console.print(f"[green]✓ Imported image: {source.name}[/green]")
            return destination

        except Exception as e:
            self.console.print(f"[red]Error importing image {image_path}: {e}[/red]")
            return None

    def _import_font_directory(self, font_dir: str) -> List[Path]:
        """Import all fonts from a directory.

        Args:
            font_dir: Path to directory containing fonts

        Returns:
            List of successfully imported font paths
        """
        try:
            source_dir = Path(font_dir).expanduser().resolve()

            if not source_dir.exists() or not source_dir.is_dir():
                self.console.print(f"[red]Font directory not found: {source_dir}[/red]")
                return []

            font_extensions = [".otf", ".ttf", ".woff", ".woff2"]
            font_files: List[Path] = []

            for ext in font_extensions:
                font_files.extend(source_dir.glob(f"*{ext}"))
                font_files.extend(source_dir.glob(f"*{ext.upper()}"))

            if not font_files:
                self.console.print(
                    f"[yellow]No font files found in {source_dir}[/yellow]"
                )
                return []

            imported = []
            for font_file in font_files:
                if self._import_font(str(font_file)):
                    imported.append(font_file)

            self.console.print(
                f"[green]✓ Imported {len(imported)} fonts from directory[/green]"
            )
            return imported

        except Exception as e:
            self.console.print(
                f"[red]Error importing font directory {font_dir}: {e}[/red]"
            )
            return []

    def _import_image_directory(self, image_dir: str) -> List[Path]:
        """Import all images from a directory.

        Args:
            image_dir: Path to directory containing images

        Returns:
            List of successfully imported image paths
        """
        try:
            source_dir = Path(image_dir).expanduser().resolve()

            if not source_dir.exists() or not source_dir.is_dir():
                self.console.print(
                    f"[red]Image directory not found: {source_dir}[/red]"
                )
                return []

            image_extensions = [".png", ".jpg", ".jpeg", ".pdf", ".eps", ".svg"]
            image_files: List[Path] = []

            for ext in image_extensions:
                image_files.extend(source_dir.glob(f"*{ext}"))
                image_files.extend(source_dir.glob(f"*{ext.upper()}"))

            if not image_files:
                self.console.print(
                    f"[yellow]No image files found in {source_dir}[/yellow]"
                )
                return []

            imported = []
            for image_file in image_files:
                if self._import_image(str(image_file)):
                    imported.append(image_file)

            self.console.print(
                f"[green]✓ Imported {len(imported)} images from directory[/green]"
            )
            return imported

        except Exception as e:
            self.console.print(
                f"[red]Error importing image directory {image_dir}: {e}[/red]"
            )
            return []

    def list_assets(self) -> None:
        """Display a table of all available assets."""
        self.console.print("\n[bold]Available Assets[/bold]")

        # Fonts table
        fonts = list(self.fonts_dir.glob("*"))
        if fonts:
            font_table = Table(title="Fonts")
            font_table.add_column("Filename", style="cyan")
            font_table.add_column("Size", style="dim")
            font_table.add_column("Type", style="green")

            for font in fonts:
                if font.is_file():
                    size = f"{font.stat().st_size / 1024:.1f} KB"
                    font_table.add_row(font.name, size, font.suffix.upper())

            self.console.print(font_table)

        # Images table
        images = list(self.images_dir.glob("*"))
        if images:
            image_table = Table(title="Images")
            image_table.add_column("Filename", style="cyan")
            image_table.add_column("Size", style="dim")
            image_table.add_column("Type", style="green")

            for image in images:
                if image.is_file():
                    size = f"{image.stat().st_size / 1024:.1f} KB"
                    image_table.add_row(image.name, size, image.suffix.upper())

            self.console.print(image_table)

        if not fonts and not images:
            self.console.print(
                "[yellow]No assets found. Run asset setup to import fonts "
                "and images.[/yellow]"
            )

    def get_asset_paths_for_config(self) -> Dict[str, str]:
        """Get relative asset paths for template configuration.

        Returns:
            Dict with asset paths relative to project root
        """
        return {
            "fonts_dir": str(self.fonts_dir.relative_to(self.project_root)),
            "images_dir": str(self.images_dir.relative_to(self.project_root)),
        }

    def update_template_variables(self, template_vars: Dict) -> Dict:
        """Update template variables with correct asset paths.

        Args:
            template_vars: Existing template variables

        Returns:
            Updated template variables with asset paths
        """
        if "config" not in template_vars:
            template_vars["config"] = {}

        # Update paths to use our asset directories
        template_vars["config"]["texmf_path"] = str(
            self.assets_dir.relative_to(self.project_root)
        )
        template_vars["config"]["fonts_path"] = str(
            self.fonts_dir.relative_to(self.project_root)
        )
        template_vars["config"]["images_path"] = str(
            self.images_dir.relative_to(self.project_root)
        )

        return template_vars
