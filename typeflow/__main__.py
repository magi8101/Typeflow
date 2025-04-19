"""
Command-line interface for TypeFlow.
"""

import argparse
import logging
import sys

from . import __version__, enable, disable, configure

def main():
    """Main entry point for TypeFlow command-line interface."""
    parser = argparse.ArgumentParser(description="TypeFlow: Seamless type conversion in Python")
    parser.add_argument("--version", action="store_true", help="Show version information")
    parser.add_argument("--enable", action="store_true", help="Enable TypeFlow globally")
    parser.add_argument("--disable", action="store_true", help="Disable TypeFlow globally")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"TypeFlow version {__version__}")
        sys.exit(0)
    
    if args.enable:
        if args.verbose:
            configure(verbose=True, log_level=logging.INFO)
        enable()
        print("TypeFlow has been enabled globally")
        sys.exit(0)
    
    if args.disable:
        disable()
        print("TypeFlow has been disabled globally")
        sys.exit(0)
    
    # Default behavior if no arguments provided
    parser.print_help()

if __name__ == "__main__":
    main()
