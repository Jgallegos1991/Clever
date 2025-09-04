import os
import json
import hashlib
import time

# --- CHANGE 1: Import the shared instances and config ---
from database import db_manager
from nlp_processor import nlp_processor
import config

class FileIngestor:
    # --- CHANGE 2: Simplified constructor ---
    # It no longer needs to create its own instances of the database or NLP processor.
    # It will use the shared instances imported above.
    def __init__(self, base_dir):
        self.base_dir = os.path.expanduser(base_dir)
        if not os.path.isdir(self.base_dir):
            print(f"Warning: Ingestion directory not found at '{self.base_dir}'")
            
    def ingest_all_files(self):
        """Walks through the base directory and ingests each file."""
        print(f"Starting ingestion process for directory: {self.base_dir}")
        inserted = updated = unchanged = failed = 0
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                # We want to ignore hidden files like .DS_Store
                if file.startswith('.'):
                    continue
                
                file_path = os.path.join(root, file)
                try:
                    status = self.ingest_file(file_path)
                    if status == "inserted":
                        inserted += 1
                    elif status == "updated":
                        updated += 1
                    elif status == "unchanged":
                        unchanged += 1
                    else:
                        failed += 1
                except Exception as e:
                    print(f"Error ingesting {file_path}: {e}")
                    failed += 1
        print(
            f"Ingestion complete. inserted={inserted} updated={updated} unchanged={unchanged} failed={failed}"
        )
    
    def ingest_file(self, file_path):
        """
        Reads a single file and adds its content to the database via the DatabaseManager.
        """
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return "failed"
        
        # Compute metadata early for quick-skip check
        filename = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        modified_ts = os.path.getmtime(file_path)

        # Quick-skip: if DB has same size and mtime, assume unchanged (avoids read/hash)
        existing = db_manager.get_source_by_path(file_path)
        if existing and existing.size == size and existing.modified_ts == modified_ts:
            print(f"unchanged: {filename} (fast-skip)")
            return "unchanged"

        # Read content and compute hash
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return "failed"

        content_hash = hashlib.sha256(content.encode("utf-8", errors="ignore")).hexdigest()

        # Upsert into DB; skip if unchanged
        id_, status = db_manager.add_or_update_source(
            filename,
            file_path,
            content,
            content_hash=content_hash,
            size=size,
            modified_ts=modified_ts,
        )
        
        print(f"{status}: {filename} (id={id_})")
        return status

# --------------------------
# Example usage
# --------------------------
if __name__ == "__main__":
    # --- CHANGE 4: Use the path from the config file ---
    # This makes the script more robust and consistent with the rest of the app.
    ingestor = FileIngestor(base_dir=config.SYNC_DIR)
    ingestor.ingest_all_files()