#!/usr/bin/env python3
"""Build the dependency-free static site without requiring Node on the VPS."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
output = root / 'dist'
if output.exists():
    shutil.rmtree(output)
shutil.copytree(root / 'src-static', output)
print(f'Built static site at {output}')
