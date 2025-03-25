#!/usr/bin/env python3
"""
gitdiffcb - Copy the result of `git diff` to the clipboard.

This script runs `git diff` in the current working directory and copies
its output to the clipboard. If the directory is not a Git repository,
an error message is shown. The pager is disabled regardless of git config.

Usage:
    gitdiffcb.py [-v]

Options:
    -v, --verbose   Print the diff result to stdout.
"""

import os
import subprocess
import sys
import argparse
import pyperclip


def is_git_repository(path):
    """
    Check whether the given path is inside a Git repository.

    Args:
        path (str): The directory path to check.

    Returns:
        bool: True if inside a Git repo, False otherwise.
    """
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_git_diff(path):
    """
    Run `git diff` with pager disabled and return the output.

    Args:
        path (str): The directory where the git command is run.

    Returns:
        str: The diff output as a string.
    """
    result = subprocess.run(
        ["git", "--no-pager", "diff"],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout


def main():
    parser = argparse.ArgumentParser(
        description="Copy `git diff` output to clipboard."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print diff output to stdout"
    )
    args = parser.parse_args()

    current_dir = os.getcwd()

    if not is_git_repository(current_dir):
        print("Error: Not a Git repository.", file=sys.stderr)
        sys.exit(1)

    diff_output = get_git_diff(current_dir)

    pyperclip.copy(diff_output)

    if args.verbose:
        print(diff_output)

    print("Copied `git diff` to clipboard.")


if __name__ == "__main__":
    main()
