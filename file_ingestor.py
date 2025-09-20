import os
import hashlib
import pypdf as PyPDF2  # Use pypdf (modern fork) but alias as PyPDF2 for clarity
import re

# --- CHANGE 1: Import the shared instances and config ---
from database import db_manager
from nlp_processor import nlp_processor
from evolution_engine import get_evolution_engine
import config

class FileIngestor:
    """Ingest files (PDF/text) into the single database with NLP enrichment.

    Why: Centralizes knowledge ingestion to keep Clever's context fresh.
    Where: Used by sync watchers, CLI ops, or manual runs.
    How: Recursively scans a directory, extracts text, runs NLP, hashes content,
    and upserts into the unified database; triggers evolution learning when meaningful.
    """

    def __init__(self, base_dir: str):
        self.base_dir = os.path.expanduser(base_dir)
        if not os.path.isdir(self.base_dir):
            print(f"Warning: Ingestion directory not found at '{self.base_dir}'")

    def ingest_all_files(self):
        """Recursively process all non-hidden files under base directory."""
        print(f"Starting ingestion process for directory: {self.base_dir}")
        inserted = updated = unchanged = failed = 0
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                # Ignore hidden files like .DS_Store
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
            f"Ingestion complete. inserted={inserted} updated={updated} "
            f"unchanged={unchanged} failed={failed}"
        )
    
    def clean_pdf_text(self, text: str) -> str:
        """Normalize extracted PDF text.
        Why: Remove artefacts + normalize whitespace before NLP.
        How: Regex collapse, strip page markers, filter symbols, condense blanks.
        """
        if not text:
            return ""
        cleaned = re.sub(r"\s+", " ", text)
        cleaned = re.sub(r"--- Page \d+ ---\s*", "\n\n", cleaned)
        cleaned = re.sub(r"[^\w\s.,!?;:()\[\]{}\"'\-]", "", cleaned)
        cleaned = re.sub(r"\n\s*\n", "\n\n", cleaned)
        return cleaned.strip()
    
    def ingest_file(self, file_path: str) -> str:
        """Ingest a single file (PDF or text) into the knowledge source table.
        
        Why: Enables incremental updates when the sync watcher detects a change
             rather than reprocessing the entire directory tree.
        Where: Called by SyncEventHandler.trigger_ingestion and can be used by
               ad-hoc maintenance scripts or tests.
        How: Determines file type, extracts / cleans content, performs optional
             NLP enrichment, hashes content to detect changes, upserts into the
             database, and (on meaningful updates) triggers evolution learning.
        
        Args:
            file_path: Absolute or relative path to the file to ingest.
        
        Returns:
            str: One of "inserted", "updated", "unchanged", "empty", or "failed".
        
        Connects to:
            - database.py via db_manager.add_or_update_source
            - evolution_engine.py for autonomous learning triggers
            - nlp_processor for local NLP enrichment (entities / keywords)
        """
        try:
            file_path = os.path.abspath(file_path)
            if not os.path.isfile(file_path):
                return "failed"
            filename = os.path.basename(file_path)
            stat = os.stat(file_path)
            size = stat.st_size
            modified_ts = stat.st_mtime

            entities: list = []
            keywords: list = []

            # Extract content + lightweight NLP
            if filename.lower().endswith('.pdf'):
                content, entities, keywords = self.process_pdf(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if nlp_processor and content.strip():
                    try:
                        analysis = nlp_processor.process_text(content)
                        entities = analysis.get('entities', [])
                        keywords = analysis.get('keywords', [])
                    except Exception as e:
                        print(f"NLP analysis failed for {filename}: {e}")

            if not content.strip():
                print(f"No content extracted from {filename}")
                return "empty"

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

            # Trigger Evolution Learning for meaningful content
            if status in ["inserted", "updated"] and len(content) > 100:
                try:
                    # For now we just log an interaction-like event into the evolution engine
                    evolution_engine = get_evolution_engine()
                    evolution_engine.log_interaction({
                        'source_file': filename,
                        'ingest_status': status,
                        'entities': entities,
                        'keywords': keywords,
                        'content_chars': len(content)
                    })
                except Exception as e:
                    print(f"Evolution logging failed for {filename}: {e}")

            print(f"{status}: {filename} (id={id_})")
            return status
        except Exception as e:
            print(f"Ingestion failed for {file_path}: {e}")
            return "failed"
    
    def process_pdf(self, pdf_path: str):
        """Extract text & basic NLP metadata from a PDF file."""
        content = []
        entities: list = []
        keywords: list = []
        try:
            with open(pdf_path, 'rb') as fh:
                reader = PyPDF2.PdfReader(fh)
                for i, page in enumerate(reader.pages):
                    txt = page.extract_text() or ''
                    if txt.strip():
                        content.append(f"\n--- Page {i+1} ---\n{txt}")
        except Exception as e:
            print(f"PDF read error {pdf_path}: {e}")
            return "", entities, keywords
        merged = self.clean_pdf_text(''.join(content))
        if nlp_processor and merged.strip():
            try:
                analysis = nlp_processor.process_text(merged)
                if hasattr(analysis, '__dict__'):
                    ad = vars(analysis)
                    entities = ad.get('entities', [])
                    keywords = ad.get('keywords', [])
            except Exception as e:
                print(f"NLP analysis failed for PDF: {e}")
        return merged, entities, keywords
    

# --------------------------
# Example usage
# --------------------------
if __name__ == "__main__":
    # --- CHANGE 4: Use the path from the config file ---
    # This makes the script more robust and consistent with the rest of the app.
    ingestor = FileIngestor(base_dir=config.SYNC_DIR)
    ingestor.ingest_all_files()