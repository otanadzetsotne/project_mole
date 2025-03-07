#!/usr/bin/env python3
"""
Command line interface for pmole package.
"""

import argparse
import os
import sys
from typing import List, Optional
from pathlib import Path
from pmole.parser import process_file


def trace(args: Optional[List[str]] = None) -> int:
    """
    Trace execution of a Python file.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:] if None)
        
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    parser = argparse.ArgumentParser(
        prog="pmole",
        description="Project Mole - Python code analysis tool"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Define 'trace' command
    trace_parser = subparsers.add_parser("trace", help="Trace Python file execution")
    trace_parser.add_argument(
        "filepath", 
        help="Path to the Python file to trace"
    )
    # Add verbose flag
    trace_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output for debugging"
    )
    
    # Parse arguments
    parsed_args = parser.parse_args(args if args is not None else sys.argv[1:])
    
    # Handle no command provided
    if not parsed_args.command:
        parser.print_help()
        return 1
    
    # Handle trace command
    if parsed_args.command == "trace":
        return handle_trace(parsed_args.filepath, parsed_args.verbose)
    
    return 0


def handle_trace(filepath: str, verbose: bool = False) -> int:
    """
    Handle the trace command logic.
    
    Args:
        filepath: Path to the Python file to trace
        verbose: Enable verbose debugging output
    """
    # Save original environment variable
    original_verbose = os.environ.get('PMOLE_VERBOSE', None)
    
    try:
        if verbose:
            os.environ['PMOLE_VERBOSE'] = '1'
            print(f"🚀 Starting trace with verbose mode for: {filepath}")
            
        # Validate file exists
        if not os.path.exists(filepath):
            print(f"Error: File '{filepath}' does not exist", file=sys.stderr)
            return 1
        
        # Validate file is a Python file
        if not filepath.endswith(".py"):
            print(f"Warning: '{filepath}' doesn't appear to be a Python file")

        processed = set()
        contents = []
        base_dir = Path.cwd()  # Get the current working directory (pwd)
        print(f"🔍 Base directory: {base_dir}")
        
        # Process initial file
        process_file(filepath, processed, contents, base_dir)
        
        # Generate final output
        result = "\n\n\n".join(contents)
        print(result)
        return 0

    except Exception as e:
        print(f"Error during processing: {e}", file=sys.stderr)
        return 1

    finally:
        # Restore original environment value
        if original_verbose is not None:
            os.environ['PMOLE_VERBOSE'] = original_verbose
        elif 'PMOLE_VERBOSE' in os.environ:
            del os.environ['PMOLE_VERBOSE']


if __name__ == "__main__":
    sys.exit(trace()) 