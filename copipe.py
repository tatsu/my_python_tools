#!/usr/bin/env python3
"""
copipe - Concatenate and copy file contents from a directory to clipboard.

This script reads files from a given directory (recursively if specified),
filters them by extension (if provided), and copies the contents to the
clipboard. Each file's content is prefixed with its path (relative to the
base directory), and files are separated by a blank line.

Usage:
    copipe.py [directory] [-r] [-e EXT [EXT ...]] [-v]

Arguments:
    directory             Directory to scan (default: current directory)

Options:
    -r, --recursive       Recursively search subdirectories.
    -e, --extension EXT   Specify one or more file extensions (e.g., .py .txt).
                          If not specified, all files are included.
    -v, --verbose         Print output to stdout in addition to copying.
"""

import os
import argparse
import pyperclip


def collect_files(base_dir, recursive=False, extensions=None):
    """
    Collect matching files from the base directory.

    Args:
        base_dir (str): The directory to search.
        recursive (bool): Whether to search subdirectories.
        extensions (list[str] or None): Extensions to filter (e.g., ['.py']).

    Returns:
        list[str]: List of relative file paths.
    """
    matched_files = []
    for root, _, files in os.walk(base_dir):
        for filename in files:
            if extensions:
                if not any(filename.endswith(ext) for ext in extensions):
                    continue
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
        "-e", "--extension",
        nargs="+",
        help="Filter by file extension(s) (e.g., .py .txt)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print output to stdout"
    )

    args = parser.parse_args()
    base_dir = os.path.abspath(args.directory)
    extensions = args.extension

    files = collect_files(base_dir, recursive=args.recursive,
                          extensions=extensions)
    output = build_output(base_dir, files)

    if args.verbose:
        print(output)

    pyperclip.copy(output)
    print("Copied to clipboard.")


if __name__ == "__main__":
    main()
