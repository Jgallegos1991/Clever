"""
FileIngestor ingest_file tests

Why: Ensure single-file ingestion behaves deterministically for inserted/unchanged/updated
Where: Unit tests under tests/ to keep ingestion stable and prevent regressions
How: Use a temporary directory with small text files and assert status transitions

Connects to:
    - file_ingestor.py: FileIngestor.ingest_file
    - database.py: db_manager.add_or_update_source
"""

from pathlib import Path
import tempfile

from file_ingestor import FileIngestor
import database
import config


def test_ingest_file_insert_and_unchanged(tmp_path: Path):
    # Arrange: temp file with content
    p = tmp_path / "sample.txt"
    p.write_text("hello world", encoding="utf-8")

    ing = FileIngestor(base_dir=str(tmp_path))

    # Act: first ingest should insert
    status1 = ing.ingest_file(str(p))

    # Assert inserted
    assert status1 in ("inserted", "updated")  # updated acceptable if pre-existed row

    # Act again without changes -> unchanged
    status2 = ing.ingest_file(str(p))
    assert status2 == "unchanged"


def test_ingest_file_updated_on_change(tmp_path: Path):
    # Arrange
    p = tmp_path / "sample2.txt"
    p.write_text("v1", encoding="utf-8")

    ing = FileIngestor(base_dir=str(tmp_path))
    status1 = ing.ingest_file(str(p))
    assert status1 in ("inserted", "updated")

    # Modify content -> should update
    p.write_text("v2 changed", encoding="utf-8")
    status2 = ing.ingest_file(str(p))
    assert status2 == "updated"
