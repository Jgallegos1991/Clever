from __future__ import annotations

import argparse
from typing import Optional

import config
from file_ingestor import FileIngestor
from database import db_manager


def cmd_ingest(path: Optional[str]):
    p = path or config.SYNC_DIR
    FileIngestor(p).ingest_all_files()


def cmd_list():
    for s in db_manager.list_sources():
        print(f"{s.id}\t{s.filename}\t{s.size or len(s.content)}\t{s.path}")


def cmd_search(query: str):
    for s in db_manager.search_sources(query):
        print(f"{s.id}\t{s.filename}\t{s.size or len(s.content)}\t{s.path}")


def cmd_show(source_id: int, content: bool):
    s = db_manager.get_source(source_id)
    if not s:
        print("not found")
        return
    print(f"id={s.id}\nfilename={s.filename}\npath={s.path}\nsize={s.size or len(s.content)}\nhash={s.content_hash}\nmodified_ts={s.modified_ts}")
    if content:
        print("\n--- content ---\n")
        print(s.content)


def main():
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
