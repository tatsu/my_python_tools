#!/usr/bin/env python3
"""
catcb - Concatenate and copy file contents from a directory to clipboard.

This script reads files from a given directory (recursively if specified),
filters them by glob patterns or names, and copies the contents to the
clipboard. You can also preview matching files before copying.

Usage:
    catcb.py [directory] [-r] [-f PATTERN ...] [-x PATTERN ...] [--preview] [-v]

Arguments:
    directory             Directory to scan (default: current directory)

Options:
    -r, --recursive       Recursively search subdirectories.
    -f, --file PATTERN    Include files matching glob patterns (e.g., *.py).
                          If not specified, all files are included.
    -x, --exclude PATTERN Exclude files matching glob patterns (e.g., test_*.py).
    --preview             Only print matching file list (no output or clipboard).
    -v, --verbose         Print file content output to stdout.
"""

import os
import argparse
import fnmatch
import pyperclip


def matches_any_pattern(path, patterns):
    """
    Check if a path matches any glob pattern or directory exclusion.

    Args:
        path (str): The relative path to match.
        patterns (list[str]): List of glob patterns or directory names.

    Returns:
        bool: True if any pattern matches the path.
    """
    for pattern in patterns:
        # If the pattern is a directory name (no wildcard, no slash), treat as dir exclusion
        if os.path.sep not in pattern and '*' not in pattern and '?' not in pattern:
            if path.startswith(pattern.rstrip('/') + '/'):
                return True
        # Otherwise, treat as glob
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def collect_files(base_dir, recursive=False, includes=None, excludes=None):
    """
    Collect files matching include/exclude patterns.

    Args:
        base_dir (str): Base directory to scan.
        recursive (bool): Search subdirectories if True.
        includes (list[str]): Glob patterns to include (match filename).
        excludes (list[str]): Glob patterns to exclude (match relpath).

    Returns:
        list[str]: Matching file paths (relative to base_dir).
    """
    matched_files = []
    for root, _, files in os.walk(base_dir):
        for filename in files:
            full_path = os.path.join(root, filename)
            relpath = os.path.relpath(full_path, base_dir)

            # Include filter on filename
            if includes and not matches_any_pattern(filename, includes):
                continue

            # Exclude filter on relative path
            if excludes and matches_any_pattern(relpath, excludes):
                continue

            matched_files.append(relpath)

        if not recursive:
            break
    return matched_files


def build_output(base_dir, file_paths):
    """Read and format file contents with header."""
    contents = []
    for relpath in sorted(file_paths):
        full_path = os.path.join(base_dir, relpath)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            contents.append(f"{relpath}:\n{file_content}")
        except Exception as e:
            contents.append(f"{relpath}: [Error reading file: {e}]")
    return "\n\n".join(contents)


def main():
    parser = argparse.ArgumentParser(description="Concatenate files to clipboard.")
    parser.add_argument("directory", nargs="?", default=".",
                        help="Directory to scan (default: current directory)")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Recursively search subdirectories")
    parser.add_argument("-f", "--file", nargs="+",
                        help="Include glob patterns (e.g., *.py README.md)")
    parser.add_argument("-x", "--exclude", nargs="+",
                        help="Exclude glob patterns (e.g., test_*.py *.bak)")
    parser.add_argument("--preview", action="store_true",
                        help="Only print list of matched files")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print output to stdout")

    args = parser.parse_args()
    base_dir = os.path.abspath(args.directory)

    files = collect_files(base_dir, recursive=args.recursive,
                          includes=args.file, excludes=args.exclude)

    if args.preview:
        print("Matched files:")
        for f in sorted(files):
            print(f)
        print(f"\nTotal: {len(files)} file(s) matched.")
        return

    output = build_output(base_dir, files)

    if args.verbose:
        print(output)

    pyperclip.copy(output)
    print("Copied to clipboard.")


if __name__ == "__main__":
    main()
