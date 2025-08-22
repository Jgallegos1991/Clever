import os
import json

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
        ingested_count = 0
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                # We want to ignore hidden files like .DS_Store
                if file.startswith('.'):
                    continue
                
                file_path = os.path.join(root, file)
                if self.ingest_file(file_path):
                    ingested_count += 1
        print(f"Ingestion complete. Added {ingested_count} new sources to memory.")
    
    def ingest_file(self, file_path):
        """
        Reads a single file and adds its content to the database via the DatabaseManager.
        """
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return False
        
        try:
            # For now, we attempt to read all files as text.
            # We can add handlers for .docx, .pdf etc. later.
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return False
        
        # --- CHANGE 3: Use the refactored database manager ---
        # We now use the add_source method, which is designed for this purpose.
        # It stores the filename, the full path, and the content.
        filename = os.path.basename(file_path)
        db_manager.add_source(filename, file_path, content)
        
        # We could use nlp_processor here to get a summary or keywords in the future,
        # but for now, the primary goal is to get the source content into the database.
        # analysis = nlp_processor.process(content[:500]) # Example: analyze first 500 chars
        
        print(f"Successfully ingested: {filename}")
        return True

# --------------------------
# Example usage
# --------------------------
if __name__ == "__main__":
    # --- CHANGE 4: Use the path from the config file ---
    # This makes the script more robust and consistent with the rest of the app.
    ingestor = FileIngestor(base_dir=config.SYNC_DIR)
    ingestor.ingest_all_files()