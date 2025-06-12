#!/usr/bin/env python3
"""
Main entry point for the Multi-Agent System
Allows running: python -m local-agent [command]
"""

import sys
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    from scripts.run import main
    main() 