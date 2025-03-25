#!/usr/bin/env python3
"""
catcb - Concatenate and copy file contents from a directory to clipboard.

This script reads files from a given directory (recursively if specified),
filters them by name or extension (if provided), and copies the contents to
the clipboard. Each file's content is prefixed with its relative path, and
files are separated by a blank line.

Usage:
    catcb.py [directory] [-r] [-f NAME [NAME ...]] [-v]

Arguments:
    directory             Directory to scan (default: current directory)

Options:
    -r, --recursive       Recursively search subdirectories.
    -f, --file NAME       Specify file names or extensions (e.g., .py README.md).
                          If not specified, all files are included.
    -v, --verbose         Print output to stdout.
"""

import os
import argparse
import pyperclip


def matches_filter(filename, filters):
    """
    Check if the filename matches any of the given filters.

    Args:
        filename (str): The file's base name.
        filters (list[str]): List of extensions or filenames.

    Returns:
        bool: True if filename matches, False otherwise.
    """
    if not filters:
        return True
    return any(
        filename == f or filename.endswith(f)
        for f in filters
    )


def collect_files(base_dir, recursive=False, filters=None):
    """
    Collect matching files from the base directory.

    Args:
        base_dir (str): The directory to search.
        recursive (bool): Whether to search subdirectories.
        filters (list[str] or None): File name or extension filters.

    Returns:
        list[str]: List of relative file paths.
    """
    matched_files = []
    for root, _, files in os.walk(base_dir):
        for filename in files:
            if matches_filter(filename, filters):
                filepath = os.path.join(root, filename)
                relpath = os.path.relpath(filepath, base_dir)
                matched_files.append(relpath)
        if not recursive:
            break
    return matched_files


def build_output(base_dir, file_paths):
    """
    Build a single string output from the given files.

    Args:
        base_dir (str): Base directory path.
        file_paths (list[str]): List of relative file paths.

    Returns:
        str: Combined file contents.
    """
    contents = []
    for relpath in sorted(file_paths):
        full_path = os.path.join(base_dir, relpath)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            header = f"{relpath}:"
            contents.append(f"{header}\n{file_content}")
        except Exception as e:
            contents.append(f"{relpath}: [Error reading file: {e}]")
    return "\n\n".join(contents)


def main():
    parser = argparse.ArgumentParser(
        description="Concatenate and copy files to clipboard."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to scan (default: current directory)"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Recursively search subdirectories"
    )
    parser.add_argument(
        "-f", "--file",
        nargs="+",
        help="Filter by file name(s) or extension(s) (e.g., .py README.md)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print output to stdout"
    )

    args = parser.parse_args()
    base_dir = os.path.abspath(args.directory)
    filters = args.file

    files = collect_files(base_dir, recursive=args.recursive, filters=filters)
    output = build_output(base_dir, files)

    if args.verbose:
        print(output)

    pyperclip.copy(output)
    print("Copied to clipboard.")


if __name__ == "__main__":
    main()
