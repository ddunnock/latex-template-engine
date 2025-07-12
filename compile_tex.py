#!/usr/bin/env python3
"""
Simple standalone LaTeX compilation script for testing.
"""

import subprocess
import sys
from pathlib import Path

def compile_latex(tex_file_path, engine="tectonic", open_pdf=False):
    """Compile a LaTeX file to PDF."""
    tex_file = Path(tex_file_path)
    
    if not tex_file.exists():
        print(f"Error: File {tex_file} does not exist")
        return False
    
    tex_dir = tex_file.parent
    tex_filename = tex_file.name
    pdf_file = tex_dir / f"{tex_file.stem}.pdf"
    
    print(f"Compiling {tex_filename} with {engine}...")
    
    # Compile based on chosen engine
    if engine == "tectonic":
        result = subprocess.run(
            ["tectonic", str(tex_file)], 
            capture_output=True, 
            text=True
        )
    else:
        result = subprocess.run(
            [engine, tex_filename], 
            capture_output=True, 
            text=True, 
            cwd=tex_dir
        )
    
    if result.returncode == 0:
        print(f"✓ Generated PDF: {pdf_file}")
        
        if open_pdf:
            subprocess.run(["open", str(pdf_file)])
        
        return True
    else:
        print(f"Error compiling LaTeX:")
        print(result.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compile_tex.py <tex_file> [engine] [--open]")
        print("Engines: tectonic (default), xelatex, pdflatex, lualatex")
        sys.exit(1)
    
    tex_file = sys.argv[1]
    engine = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "tectonic"
    open_pdf = "--open" in sys.argv
    
    success = compile_latex(tex_file, engine, open_pdf)
    sys.exit(0 if success else 1)
