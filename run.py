#!/usr/bin/env python3
"""
Quick launcher script for AI Documentation Agent.

This script provides a convenient way to run the agent from the project root.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the agent
from src.ai_agent import main

if __name__ == "__main__":
    main()
