# Project Mole

## Overview
Python package for code analysis and execution tracing. Provides CLI tools for analyzing Python code structure and dependencies.

## Features
- CLI interface for tracing Python file execution
- Import dependency resolution
- Module hierarchy visualization
- Verbose debugging mode
- PyPI package distribution

## Installation
```bash
# Install from PyPI
pip install pmole

# Install locally from source
pip install .
```

## Usage
```bash
# Trace a Python file's execution
pmole trace path/to/file.py

# Enable verbose output
pmole trace path/to/file.py -v
```

## License
MIT - See [LICENSE](LICENSE) for details.
