#!/usr/bin/env python3
# hexcore/terminal.py — Configure 24-bit truecolor environment support (modular version)

"""
This module provides CLI flags to enable or disable truecolor support
by modifying the user's ~/.bashrc file with appropriate environment variables.

Supported Flags:
    --enable-truecolor    → Appends truecolor export variables to ~/.bashrc
    --disable-truecolor   → Removes truecolor export lines from ~/.bashrc

Usage Examples (as CLI):
    $ hexcore --enable-truecolor
    $ hexcore --disable-truecolor

Usage Examples (as importable module):
    from hexcore import terminal
    terminal.enable_truecolor_support()
"""

import os
import argparse


def enable_truecolor_support():
    """
    Appends necessary environment variables to ~/.bashrc for 24-bit truecolor support:
        export COLORTERM=truecolor
        export TERM=xterm-256color
    """
    bashrc_path = os.path.expanduser("~/.bashrc")

    if not os.path.exists(bashrc_path):
        open(bashrc_path, "w").close()

    with open(bashrc_path, "r") as file:
        content = file.read()

    lines_to_add = []

    if "COLORTERM=truecolor" not in content:
        lines_to_add.append("export COLORTERM=truecolor\n")

    if "TERM=xterm-256color" not in content:
        lines_to_add.append("export TERM=xterm-256color\n")

    if lines_to_add:
        with open(bashrc_path, "a") as file:
            file.writelines(lines_to_add)
        print("✔ Truecolor configuration added to ~/.bashrc")
        print("   Please run 'source ~/.bashrc' or restart your terminal to apply changes.")
    else:
        print("ℹ Truecolor environment variables are already present.")


def disable_truecolor_support():
    """
    Removes the truecolor environment variable lines from ~/.bashrc if they exist.
    """
    bashrc_path = os.path.expanduser("~/.bashrc")

    if not os.path.exists(bashrc_path):
        print("ℹ No ~/.bashrc file found. Nothing to remove.")
        return

    with open(bashrc_path, "r") as file:
        lines = file.readlines()

    new_lines = [
        line for line in lines
        if "COLORTERM=truecolor" not in line and "TERM=xterm-256color" not in line
    ]

    if len(new_lines) != len(lines):
        with open(bashrc_path, "w") as file:
            file.writelines(new_lines)
        print("✔ Truecolor configuration removed from ~/.bashrc")
        print("   Please run 'source ~/.bashrc' or restart your terminal to apply changes.")
    else:
        print("ℹ No truecolor environment variables found in ~/.bashrc")


def add_arguments(parser: argparse.ArgumentParser):
    """
    Register CLI flags for truecolor configuration management.

    Flags:
        --enable-truecolor     Enable 24-bit color support via environment variables
        --disable-truecolor    Remove 24-bit color environment settings from ~/.bashrc
    """
    group = parser.add_argument_group("Terminal Environment")
    group.add_argument(
        "--enable-truecolor",
        action="store_true",
        help="Enable 24-bit color support by appending env vars to ~/.bashrc"
    )
    group.add_argument(
        "--disable-truecolor",
        action="store_true",
        help="Remove truecolor-related environment settings from ~/.bashrc"
    )


def handle_arguments(args) -> bool:
    """
    Handles --enable-truecolor and --disable-truecolor actions.

    Validates that both are not used simultaneously.

    Returns:
        True if either flag was triggered, False otherwise.
    """
    if args.enable_truecolor and args.disable_truecolor:
        print("Error: --enable-truecolor and --disable-truecolor cannot be used together.")
        return True

    if args.enable_truecolor:
        enable_truecolor_support()
        return True

    if args.disable_truecolor:
        disable_truecolor_support()
        return True

    return False


def run(cli_args=None):
    """
    Run terminal configuration logic from CLI parser (optional).

    Example (called from hexcore/main.py):
        terminal.run()
    """
    parser = argparse.ArgumentParser(
        prog="hexcore-terminal",
        description="Manage truecolor terminal support for 24-bit color output."
    )
    add_arguments(parser)
    args = parser.parse_args(cli_args)
    if not handle_arguments(args):
        parser.print_help()