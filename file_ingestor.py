import os
import json
import hashlib
import time
import PyPDF2
import re

# --- CHANGE 1: Import the shared instances and config ---
from database import db_manager
from nlp_processor import nlp_processor
from evolution_engine import get_evolution_engine
import config

class FileIngestor:
    """
    File processing and knowledge base ingestion system for Clever AI.
    
    Why: Converts various file formats into structured knowledge base entries
         with NLP analysis to enable intelligent search and reasoning.
    Where: Core component used by sync watchers, CLI tools, and automation
           systems to process files from sync directories.
    How: Extracts content from text and PDF files, performs NLP analysis,
         computes metadata hashes, and stores structured data in database.
    """
    
    def __init__(self, base_dir):
        """
        Initialize file ingestor for specified base directory.
        
        Why: Sets up ingestion scope for a specific directory to enable
             batch processing and automatic file monitoring capabilities.
        Where: Called by sync systems, CLI tools, and scheduled processes
               that need to process files from specific locations.
        How: Expands user path and validates directory existence, using
             shared database and NLP processor instances for efficiency.
        
        Args:
            base_dir: Directory path to process for file ingestion
        """
        self.base_dir = os.path.expanduser(base_dir)
        if not os.path.isdir(self.base_dir):
            print(f"Warning: Ingestion directory not found at '{self.base_dir}'")
            
    def ingest_all_files(self):
        """
        Process all files in base directory recursively for knowledge base ingestion.
        
        Why: Enables batch processing of entire directory structures to build
             comprehensive knowledge base from file collections.
        Where: Called by CLI ingest commands and batch processing operations
               to populate knowledge base with existing file content.
        How: Walks directory tree, filters hidden files, processes each file
             through ingest_file, aggregates and reports processing statistics.
        """
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
                    raise  # Re-raise to maintain error visibility
        print(
            f"Ingestion complete. inserted={inserted} updated={updated} unchanged={unchanged} failed={failed}"
        )
    
    def ingest_file(self, file_path):
        """
        Process single file for knowledge base ingestion with NLP analysis and metadata tracking.
        
        Why: Converts individual files into searchable knowledge base entries
             with intelligent content analysis and change detection.
        Where: Called by file watchers, batch processors, and manual ingestion
               operations to handle specific file updates.
        How: Extracts content by file type (PDF/text), performs NLP analysis,
             computes content hashes, handles metadata updates, integrates with evolution engine.
             
        Args:
            file_path: Path to the file to process and ingest
            
        Returns:
            str: Status of ingestion - "inserted", "updated", "unchanged", or "failed"
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

        # Extract content based on file type
        content = ""
        entities = []
        keywords = []
        
        if filename.lower().endswith('.pdf'):
            content, entities, keywords = self.process_pdf(file_path)
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Basic NLP analysis for text files
            if nlp_processor and content.strip():
                analysis = nlp_processor.process(content)
                if hasattr(analysis, '__dict__'):
                    analysis_dict = vars(analysis)
                    entities = analysis_dict.get('entities', [])
                    keywords = analysis_dict.get('keywords', [])

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
        Extract and analyze content from PDF files with NLP processing.
        
        Why: Enables knowledge base ingestion from PDF documents with
             structured text extraction and intelligent content analysis.
        Where: Called by ingest_file when processing PDF file types to
               convert document content into searchable text format.
        How: Uses PyPDF2 to extract text by page, applies text cleaning,
             performs NLP analysis for entities and keywords extraction.
             
        Args:
            pdf_path: File system path to the PDF document to process
            
        Returns:
            Tuple[str, List, List]: (cleaned_content, entities, keywords)
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
                    analysis = nlp_processor.process(content)
                    if hasattr(analysis, '__dict__'):
                        analysis_dict = vars(analysis)
                        entities = analysis_dict.get('entities', [])
                        keywords = analysis_dict.get('keywords', [])
                
        except Exception as e:
            print(f"PDF processing error: {e}")
            raise  # Re-raise instead of swallowing
            
        return content, entities, keywords
    
    def clean_pdf_text(self, text):
        """
        Normalize and clean extracted PDF text for consistent processing.
        
        Why: PDF text extraction often contains formatting artifacts and
             irregular spacing that needs normalization for quality analysis.
        Where: Called by process_pdf after text extraction to prepare
               content for NLP processing and database storage.
        How: Applies regex patterns to remove excessive whitespace,
             normalize line breaks, and standardize text formatting.
             
        Args:
            text: Raw text extracted from PDF document
            
        Returns:
            str: Cleaned and normalized text ready for analysis
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