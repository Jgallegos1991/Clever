from __future__ import annotations

import argparse
from typing import Optional

import config
from file_ingestor import FileIngestor
from database import db_manager


def cmd_ingest(path: Optional[str]):
    """
    Execute file ingestion for specified path or default sync directory.

    Why: Provides command-line interface for manually triggering file
         ingestion when automatic sync is not sufficient or available.
    Where: CLI command handler for 'ingest' subcommand, used for manual
         knowledge base updates from file system sources.
    How: Uses provided path or defaults to config.SYNC_DIR, creates
         FileIngestor instance and processes all files in directory.

    Args:
        path: Optional directory path to ingest, defaults to config.SYNC_DIR
    """
    p = path or config.SYNC_DIR
    FileIngestor(p).ingest_all_files()


def cmd_list():
    """
    Display list of all sources in the Clever AI knowledge base.

    Why: Provides visibility into ingested content for debugging and
         manual knowledge base management operations.
    Where: CLI command handler for 'list' subcommand, used to inspect
         current database contents and file inventory.
    How: Queries database manager for all sources, formats and prints
         tabular output with ID, filename, size, and path information.
    """
    for s in db_manager.list_sources():
        print(f"{s.id}\t{s.filename}\t{s.size or len(s.content)}\t{s.path}")


def cmd_search(query: str):
    """
    Search knowledge base content for sources matching query string.

    Why: Enables command-line content discovery and knowledge base
         exploration for research and debugging purposes.
    Where: CLI command handler for 'search' subcommand, used to locate
           specific content within ingested sources.
    How: Passes query to database manager's search functionality,
         displays matching sources in tabular format with metadata.

    Args:
        query: Search string to match against source content and metadata
    """
    for s in db_manager.search_sources(query):
        print(f"{s.id}\t{s.filename}\t{s.size or len(s.content)}\t{s.path}")


def cmd_show(source_id: int, content: bool):
    """
    Display detailed information for a specific source by ID.

    Why: Provides detailed inspection of individual knowledge base entries
         for debugging and content verification purposes.
    Where: CLI command handler for 'show' subcommand, used to examine
           specific source metadata and optionally view full content.
    How: Retrieves source by ID from database manager, displays formatted
         metadata, optionally includes full content text if requested.

    Args:
        source_id: Unique identifier for the source to display
        content: Whether to include full source content in output
    """
    s = db_manager.get_source(source_id)
    if not s:
        print("not found")
        return
    print(
        f"id={s.id}\nfilename={s.filename}\npath={s.path}\nsize={s.size or len(s.content)}\nhash={s.content_hash}\nmodified_ts={s.modified_ts}"
    )
    if content:
        print("\n--- content ---\n")
        print(s.content)


def main():
    """
    Main CLI entry point with argument parsing and command dispatch.

    Why: Provides command-line interface for Clever AI database operations
         and file management without requiring Flask server to be running.
    Where: Entry point for the 'clever' CLI tool, enabling direct interaction
           with knowledge base and ingestion systems.
    How: Sets up argparse with subcommands for ingest, list, search, show
         operations, parses arguments and dispatches to appropriate handlers.
    """
    ap = argparse.ArgumentParser(prog="clever")
    sp = ap.add_subparsers(dest="cmd", required=True)

    sp_ingest = sp.add_parser("ingest")
    sp_ingest.add_argument("path", nargs="?")

    sp_list = sp.add_parser("list")

    sp_search = sp.add_parser("search")
    sp_search.add_argument("query")

    sp_show = sp.add_parser("show")
    sp_show.add_argument("id", type=int)
    sp_show.add_argument("--content", action="store_true")

    args = ap.parse_args()
    if args.cmd == "ingest":
        cmd_ingest(args.path)
    elif args.cmd == "list":
        cmd_list()
    elif args.cmd == "search":
        cmd_search(args.query)
    elif args.cmd == "show":
        cmd_show(args.id, args.content)


if __name__ == "__main__":
    main()
