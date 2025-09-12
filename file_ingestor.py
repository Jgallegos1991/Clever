import os
import json
import hashlib
import time
import pypdf as PyPDF2  # Import pypdf with PyPDF2 alias for compatibility
import re

# --- CHANGE 1: Import the shared instances and config ---
from database import db_manager
from nlp_processor import nlp_processor
from evolution_engine import get_evolution_engine
import config

class FileIngestor:
    """
    FileIngestor class for ingesting files and extracting knowledge

    Why: Ensures Clever is resilient, adaptive, and nearly invisible—always
    operating in the background, never cutting short on capability, and ready
    to evolve with the user. Centralizes file ingestion logic for robust,
    automated knowledge extraction and database updates.
    Where: Connects to shared DatabaseManager (db_manager), NLP processor
    (nlp_processor), and evolution engine (get_evolution_engine).
    How: Walks through files in a directory, processes each file (PDF/text),
    extracts content and metadata, performs NLP analysis, and updates the
    database. Triggers evolution learning for meaningful content, all while
    maintaining seamless, resilient operation.

    Connects to:
        - database.py: Uses db_manager for database operations
        - nlp_processor.py: Uses nlp_processor for NLP analysis
        - evolution_engine.py: Triggers evolution learning
        - config.py: Uses config for directory paths
    """
    def __init__(self, base_dir):
        """
        Initialize FileIngestor with a base directory
        
        Why: Sets up the ingestion root for scanning files
        Where: Used by ingest_all_files and main script entry
        How: Expands user path, checks directory existence, stores path
        
        Args:
            base_dir: Path to the directory to ingest
        """
        self.base_dir = os.path.expanduser(base_dir)
        if not os.path.isdir(self.base_dir):
            print(
                f"Warning: Ingestion directory not found at '{self.base_dir}'"
            )
            
    def ingest_all_files(self):
        """
        Walk through the base directory and ingest each file
        
    Why: Automates bulk ingestion for knowledge extraction and
    database updates
        Where: Entry point for file ingestion, called by main script
    How: Recursively scans directory, processes each file, tracks status,
    handles errors
        """
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
    
    def ingest_file(self, file_path):
        """
        Ingest a single file and add its content to the database
        
        Why: Enables granular ingestion and knowledge extraction for each file
        Where: Called by ingest_all_files for every file found
    How: Checks file existence, extracts content (PDF/text), performs NLP,
    computes hash, upserts to DB, triggers evolution learning
        
        Args:
            file_path: Path to the file to ingest
        Returns:
            Status string: 'inserted', 'updated', 'unchanged', or 'failed'
        Connects to:
            - db_manager.add_or_update_source: Database upsert
            - nlp_processor.process: NLP analysis
            - get_evolution_engine().process_pdf_knowledge: Evolution learning
        """
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return "failed"
        # Compute metadata early for quick-skip check
        filename = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        modified_ts = os.path.getmtime(file_path)

    # Quick-skip: if DB has same size and mtime, assume unchanged
    # (avoids read/hash)
        existing = db_manager.get_source_by_path(file_path)
        if (
            existing
            and existing.size == size
            and existing.modified_ts == modified_ts
        ):
            print(f"unchanged: {filename} (fast-skip)")
            return "unchanged"

        # Extract content based on file type
        content = ""
        entities = []
        keywords = []
        
        try:
            if filename.lower().endswith('.pdf'):
                content, entities, keywords = self.process_pdf(file_path)
            else:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                # Basic NLP analysis for text files
                if nlp_processor and content.strip():
                    try:
                        analysis = nlp_processor.process(content)
                        if hasattr(analysis, '__dict__'):
                            analysis_dict = vars(analysis)
                            entities = analysis_dict.get('entities', [])
                            keywords = analysis_dict.get('keywords', [])
                    except Exception as e:
                        print(f"NLP analysis failed for {filename}: {e}")
                        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return "failed"

        if not content.strip():
            print(f"No content extracted from {filename}")
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
        
        # Trigger Evolution Learning for meaningful content
        if status in ["inserted", "updated"] and len(content) > 100:
            try:
                evolution_engine = get_evolution_engine()
                
                # Process for autonomous learning
                learning_results = evolution_engine.process_pdf_knowledge(
                    filename, content, entities, keywords
                )
                
                if learning_results['concepts_learned'] > 0 or learning_results['connections_formed'] > 0:
                    print(f"🧠 Clever learned from {filename}: "
                          f"{learning_results['concepts_learned']} concepts, "
                          f"{learning_results['connections_formed']} connections")
                    
                    if learning_results['evolution_triggered']:
                        print(f"✨ Evolution cascade triggered by {filename}!")
                        
            except Exception as e:
                print(f"Evolution learning failed for {filename}: {e}")
        
        print(f"{status}: {filename} (id={id_})")
        return status
    
    def process_pdf(self, pdf_path):
        """
        Extract content, entities, and keywords from a PDF file
        
        Why: Enables knowledge extraction from PDF documents for ingestion
        Where: Called by ingest_file for PDF files
        How: Reads PDF pages, cleans text, performs NLP analysis for entities/keywords
        
        Args:
            pdf_path: Path to the PDF file
        Returns:
            Tuple: (content, entities, keywords)
        Connects to:
            - nlp_processor.process: NLP analysis
        """
        content = ""
        entities = []
        keywords = []
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text.strip():
                        content += f"\n--- Page {page_num + 1} ---\n{page_text}"
                # Enhanced text cleaning
                content = self.clean_pdf_text(content)
                # Extract entities and keywords using NLP
                if nlp_processor and content.strip():
                    try:
                        analysis = nlp_processor.process(content)
                        if hasattr(analysis, '__dict__'):
                            analysis_dict = vars(analysis)
                            entities = analysis_dict.get('entities', [])
                            keywords = analysis_dict.get('keywords', [])
                    except Exception as e:
                        print(f"NLP analysis failed for PDF: {e}")
        except Exception as e:
            print(f"PDF processing error: {e}")
        return content, entities, keywords
    
    def clean_pdf_text(self, text):
        """
        Clean and normalize PDF text for ingestion
        
        Why: Improves quality of extracted text for NLP and database storage
        Where: Used by process_pdf after extracting raw text
        How: Removes excessive whitespace, page markers, artifacts, normalizes line breaks
        
        Args:
            text: Raw text extracted from PDF
        Returns:
            Cleaned and normalized text string
        """
        if not text:
            return ""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove page headers/footers patterns
        text = re.sub(r'--- Page \d+ ---\s*', '\n\n', text)
        # Remove common PDF artifacts
        text = re.sub(r'[^\w\s.,!?;:()\[\]{}"\'-]', '', text)
        # Normalize line breaks
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

# --------------------------
# Example usage
# --------------------------
if __name__ == "__main__":
    # --- CHANGE 4: Use the path from the config file ---
    # This makes the script more robust and consistent with the rest of the app.
    ingestor = FileIngestor(base_dir=config.SYNC_DIR)
    ingestor.ingest_all_files()