#!/usr/bin/env python3
"""
Convert file-inventory.json to file-inventory.md

Why: Automates the conversion of JSON-based file inventory into a human-readable Markdown report for project documentation and auditing.
Where: Used by developers and CI scripts to generate up-to-date file-inventory.md from the latest repository analysis.
How: Loads JSON, computes statistics, groups files, and writes a formatted Markdown summary with tables and breakdowns.

Connects to:
    - file-inventory.md: Target output file for documentation
    - file-inventory.json: Source data for conversion (if exists)
    - Makefile: Typically called by make file-inventory command
"""
import json
import os
from collections import defaultdict


def load_inventory(json_path):
    """
    Load the file inventory from JSON
    
    Why: Reads structured file data for further processing and reporting
    Where: Used by main() and create_markdown()
    How: Opens and parses the JSON file into Python objects
    """
    with open(json_path, "r") as f:
        return json.load(f)


def group_by_language(files):
    """
    Group files by language
    
    Why: Enables language-based statistics and breakdowns in the report
    Where: Used by create_markdown() for summary and detailed tables
    How: Iterates file list and groups by 'lang' field
    """
    by_lang = defaultdict(list)
    for file_data in files:
        lang = file_data.get("lang", "unknown")
        by_lang[lang].append(file_data)
    return dict(by_lang)


def group_by_directory(files):
    """
    Group files by top-level directory
    
    Why: Provides directory-based organization for inventory reporting
    Where: Used by create_markdown() for directory summary tables
    How: Splits file paths and groups by first segment
    """
    by_dir = defaultdict(list)
    for file_data in files:
        path = file_data.get("path", "")
        if "/" in path:
            top_dir = path.split("/")[0]
        else:
            top_dir = "."  # root files
        by_dir[top_dir].append(file_data)
    return dict(by_dir)


def calculate_stats(files):
    """
    Calculate overall statistics
    
    Why: Summarizes file count, lines of code, and language breakdowns
    Where: Used by create_markdown() for summary section
    How: Aggregates counts and LOC by language and overall
    """
    total_files = len(files)
    total_loc = sum(file_data.get("loc", 0) for file_data in files)

    # Count by language
    lang_counts = defaultdict(int)
    lang_loc = defaultdict(int)

    for file_data in files:
        lang = file_data.get("lang", "unknown")
        lang_counts[lang] += 1
        lang_loc[lang] += file_data.get("loc", 0)

    return {
        "total_files": total_files,
        "total_loc": total_loc,
        "lang_counts": dict(lang_counts),
        "lang_loc": dict(lang_loc),
    }


def format_number(num):
    """
    Format numbers with commas for readability
    
    Why: Improves readability of statistics in Markdown tables
    Where: Used throughout create_markdown() for all numeric output
    How: Uses Python string formatting with commas
    """
    return f"{num:,}"


def create_markdown(files, output_path):
    """
    Create markdown file from inventory data
    
    Why: Generates the Markdown report for project file inventory
    Where: Called by main() after loading JSON
    How: Computes stats, builds tables, writes to output file
    """

    stats = calculate_stats(files)
    by_lang = group_by_language(files)
    by_dir = group_by_directory(files)

    markdown_content = []

    # Header
    markdown_content.append("# File Inventory")
    markdown_content.append("")
    markdown_content.append(
        "This document provides an overview of all files in the project repository."
    )
    markdown_content.append("")

    # Summary Statistics
    markdown_content.append("## Summary Statistics")
    markdown_content.append("")
    markdown_content.append(f"- **Total Files**: {format_number(stats['total_files'])}")
    markdown_content.append(
        f"- **Total Lines of Code**: {format_number(stats['total_loc'])}"
    )
    markdown_content.append(f"- **Languages/File Types**: {len(stats['lang_counts'])}")
    markdown_content.append("")

    # Top Languages by File Count
    markdown_content.append("## Top Languages by File Count")
    markdown_content.append("")
    sorted_lang_counts = sorted(
        stats["lang_counts"].items(), key=lambda x: x[1], reverse=True
    )

    markdown_content.append("| Language | Files | Lines of Code |")
    markdown_content.append("|----------|-------|---------------|")

    for lang, count in sorted_lang_counts[:20]:  # Top 20
        loc = stats["lang_loc"].get(lang, 0)
        markdown_content.append(
            f"| {lang} | {format_number(count)} | {format_number(loc)} |"
        )

    markdown_content.append("")

    # Directory Structure Overview
    markdown_content.append("## Directory Structure Overview")
    markdown_content.append("")

    sorted_dirs = sorted(by_dir.items(), key=lambda x: len(x[1]), reverse=True)

    markdown_content.append("| Directory | Files | Total LOC |")
    markdown_content.append("|-----------|-------|-----------|")

    for dir_name, dir_files in sorted_dirs[:20]:  # Top 20 directories
        dir_loc = sum(f.get("loc", 0) for f in dir_files)
        markdown_content.append(
            f"| {dir_name} | {format_number(len(dir_files))} | {format_number(dir_loc)} |"
        )

    markdown_content.append("")

    # Core Project Files (excluding .venv and similar)
    markdown_content.append("## Core Project Files")
    markdown_content.append("")
    markdown_content.append("Files in the root directory and main project folders:")
    markdown_content.append("")

    core_files = []
    for file_data in files:
        path = file_data.get("path", "")
        # Include root files and exclude .venv, __pycache__, etc.
        if not path.startswith(".venv/") and not path.startswith("__pycache__/"):
            core_files.append(file_data)

    # Sort by path
    core_files.sort(key=lambda x: x.get("path", ""))

    markdown_content.append("| File | Language | LOC | Purpose |")
    markdown_content.append("|------|----------|-----|---------|")

    for file_data in core_files[:100]:  # Limit to avoid huge tables
        path = file_data.get("path", "")
        lang = file_data.get("lang", "")
        loc = file_data.get("loc", 0)
        purpose = file_data.get("purpose", "").strip()
        if not purpose:
            purpose = "-"

        markdown_content.append(
            f"| `{path}` | {lang} | {format_number(loc)} | {purpose} |"
        )

    markdown_content.append("")

    # Detailed Breakdown by Language
    markdown_content.append("## Detailed Breakdown by Language")
    markdown_content.append("")

    for lang in sorted(by_lang.keys()):
        if lang in [".venv", "__pycache__"]:  # Skip these
            continue

        lang_files = by_lang[lang]
        total_lang_loc = sum(f.get("loc", 0) for f in lang_files)

        markdown_content.append(f"### {lang.upper()} Files")
        markdown_content.append("")
        markdown_content.append(f"- **Count**: {format_number(len(lang_files))}")
        markdown_content.append(f"- **Total LOC**: {format_number(total_lang_loc)}")
        markdown_content.append("")

        # Show top files for this language (excluding .venv)
        core_lang_files = [
            f for f in lang_files if not f.get("path", "").startswith(".venv/")
        ]
        if core_lang_files:
            core_lang_files.sort(key=lambda x: x.get("loc", 0), reverse=True)

            markdown_content.append("**Notable files:**")
            markdown_content.append("")

            for file_data in core_lang_files[:10]:  # Top 10
                path = file_data.get("path", "")
                loc = file_data.get("loc", 0)
                purpose = file_data.get("purpose", "").strip()

                if purpose:
                    markdown_content.append(
                        f"- `{path}` ({format_number(loc)} LOC) - {purpose}"
                    )
                else:
                    markdown_content.append(f"- `{path}` ({format_number(loc)} LOC)")

            markdown_content.append("")

    # Footer
    markdown_content.append("---")
    markdown_content.append("")
    markdown_content.append(
        "*This file inventory was generated automatically from the repository analysis.*"
    )

    # Write to file
    with open(output_path, "w") as f:
        f.write("\n".join(markdown_content))

    print(f"Markdown file created: {output_path}")
    print(
        f"Processed {stats['total_files']} files with {format_number(stats['total_loc'])} total lines of code"
    )


def main():
    """
    Main entry point for inventory conversion script
    
    Why: Orchestrates loading, processing, and Markdown generation for file inventory
    Where: Called when script is run directly or by CI
    How: Loads JSON, calls create_markdown(), prints status
    """
    json_path = "docs/file-inventory.json"
    output_path = "file-inventory.md"

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return

    print(f"Loading inventory from {json_path}...")
    files = load_inventory(json_path)

    print(f"Creating markdown file at {output_path}...")
    create_markdown(files, output_path)


if __name__ == "__main__":
    main()
