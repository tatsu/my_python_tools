#!/usr/bin/env python3
"""
gitdiffcb - Copy the result of `git diff` to the clipboard.

This script runs `git diff` (or `git diff --cached` if --staged is specified)
in the current working directory and copies its output to the clipboard.
If the directory is not a Git repository, an error message is shown.
The pager is disabled regardless of git config.

Usage:
    gitdiffcb.py [--staged] [-v]

Options:
    --staged         Show only staged (cached) changes.
    -v, --verbose    Print the diff result to stdout.
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


def get_git_diff(path, staged=False):
    """
    Run `git diff` (or `git diff --cached`) with pager disabled and return output.

    Args:
        path (str): Directory where the git command is run.
        staged (bool): Whether to get staged changes.

    Returns:
        str: The diff output as a string.
    """
    cmd = ["git", "--no-pager", "diff"]
    if staged:
        cmd.append("--cached")

    result = subprocess.run(
        cmd,
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
        "--staged",
        action="store_true",
        help="Show staged (cached) changes only"
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

    diff_output = get_git_diff(current_dir, staged=args.staged)

    if not diff_output.strip():
        print("No changes found.")
        return

    pyperclip.copy(diff_output)

    if args.verbose:
        print(diff_output)

    print("Copied `git diff{}` to clipboard.".format(
        " --cached" if args.staged else ""
    ))


if __name__ == "__main__":
    main()
