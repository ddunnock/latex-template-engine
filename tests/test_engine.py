"""Tests for the template engine."""

import shutil
import tempfile
from pathlib import Path

import pytest

from latex_template_engine.config.schema import TemplateConfig
from latex_template_engine.core.engine import TemplateEngine


@pytest.fixture
def temp_template_dir():
    """Create a temporary directory with test templates."""
    temp_dir = Path(tempfile.mkdtemp())

    # Create a simple test template
    test_template = """\\documentclass{article}
\\title{<<title>>}
\\author{<<author>>}
\\begin{document}
\\maketitle
<<content>>
\\end{document}"""

    (temp_dir / "test.tex.j2").write_text(test_template)

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)


def test_engine_initialization(temp_template_dir):
    """Test that the engine initializes correctly."""
    engine = TemplateEngine(temp_template_dir)
    assert engine.template_dir == temp_template_dir


def test_list_templates(temp_template_dir):
    """Test template listing functionality."""
    engine = TemplateEngine(temp_template_dir)
    templates = engine.list_templates()
    assert "test" in templates


def test_load_template(temp_template_dir):
    """Test template loading."""
    engine = TemplateEngine(temp_template_dir)
    template = engine.load_template("test")
    assert template is not None
    assert template.jinja_template is not None


def test_generate_document(temp_template_dir):
    """Test document generation."""
    engine = TemplateEngine(temp_template_dir)

    variables = {
        "title": "Test Document",
        "author": "Test Author",
        "content": "This is test content.",
    }

    content = engine.generate_document("test", variables)

    assert "Test Document" in content
    assert "Test Author" in content
    assert "This is test content." in content
    assert "\\documentclass{article}" in content


def test_generate_document_with_output(temp_template_dir):
    """Test document generation with file output."""
    engine = TemplateEngine(temp_template_dir)
    output_path = temp_template_dir / "output.tex"

    variables = {
        "title": "Test Document",
        "author": "Test Author",
        "content": "This is test content.",
    }

    content = engine.generate_document("test", variables, output_path)

    assert output_path.exists()
    assert output_path.read_text() == content


def test_template_not_found(temp_template_dir):
    """Test handling of missing templates."""
    engine = TemplateEngine(temp_template_dir)

    with pytest.raises(FileNotFoundError):
        engine.load_template("nonexistent")
