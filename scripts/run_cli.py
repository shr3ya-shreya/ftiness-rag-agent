#!/usr/bin/env python3
"""CLI runner script for Cursor IDE"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.api_wrapper import start_cli

if __name__ == "__main__":
    start_cli()
