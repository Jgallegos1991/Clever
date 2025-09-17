#!/usr/bin/env python3
"""
Enhanced File Ingestor with PDF Support

Intelligently processes PDFs, text files, and other documents for
Clever's knowledge base.
"""

import os
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple
Intelligently processes PDFs, text files, and other documents for Clever's knowledge base.
"""

import os
import json
import hashlib
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging

# Core dependencies
from database import db_manager
from nlp_processor import nlp_processor
import config

# PDF processing (optional dependency)
try:
    import pypdf as PyPDF2  # Import pypdf with PyPDF2 alias for compatibility
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("📚 PDF support not available. Install with: pip install pypdf")
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("📚 PDF support not available. Install with: pip install PyPDF2")

logger = logging.getLogger(__name__)

class EnhancedFileIngestor:
    """Enhanced file ingestor with PDF support and intelligent chunking."""
    
    def __init__(self, base_dirs: List[str] = None):
        """Initialize with multiple directories to monitor."""
        if base_dirs is None:
            base_dirs = [config.SYNC_DIR, "./Clever_Learn"]
            
        self.base_dirs = [os.path.expanduser(d) for d in base_dirs]
        self.supported_extensions = {'.txt', '.md', '.py', '.js', '.json', '.csv'}
        if PDF_SUPPORT:
            self.supported_extensions.add('.pdf')
            
        # Ensure directories exist
        for dir_path in self.base_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            if not os.path.isdir(dir_path):
                logger.warning(f"Directory not accessible: {dir_path}")
    
    def ingest_all_files(self) -> Dict[str, int]:
        """Walk through all base directories and ingest supported files."""
        print(f"🔄 Starting enhanced ingestion for: {self.base_dirs}")
        
        stats = {"inserted": 0, "updated": 0, "unchanged": 0, "failed": 0, "skipped": 0}
        
        for base_dir in self.base_dirs:
            if not os.path.exists(base_dir):
                logger.warning(f"Skipping non-existent directory: {base_dir}")
                continue
                
            print(f"📁 Processing directory: {base_dir}")
            
            for root, _, files in os.walk(base_dir):
                for file in files:
                    if file.startswith('.'):
                        continue  # Skip hidden files
                        
                    file_path = os.path.join(root, file)
                    file_ext = Path(file).suffix.lower()
                    
                    if file_ext not in self.supported_extensions:
                        stats["skipped"] += 1
                        continue
                    
                    try:
                        status = self.ingest_file(file_path)
                        stats[status] += 1
                        
                    except Exception as e:
                        logger.error(f"Error processing {file_path}: {e}")
                        stats["failed"] += 1
        
        print(f"✅ Ingestion complete: {stats}")
        return stats
    
    def ingest_file(self, file_path: str) -> str:
        """Process a single file and add to knowledge base."""
        if not os.path.exists(file_path):
            return "failed"
        
        filename = os.path.basename(file_path)
        file_ext = Path(file_path).suffix.lower()
        size = os.path.getsize(file_path)
        modified_ts = os.path.getmtime(file_path)
        
        # Quick skip for unchanged files
        existing = db_manager.get_source_by_path(file_path)
        if existing and existing.size == size and existing.modified_ts == modified_ts:
            return "unchanged"
        
        # Extract content based on file type
        try:
            if file_ext == '.pdf' and PDF_SUPPORT:
                content, metadata = self._extract_pdf_content(file_path)
            else:
                content, metadata = self._extract_text_content(file_path)
                
            if not content.strip():
                print(f"⚠️  Empty content: {filename}")
                return "failed"
                
        except Exception as e:
            logger.error(f"Content extraction failed for {file_path}: {e}")
            return "failed"
        
        # Chunk large documents
        chunks = self._chunk_content(content, filename, metadata)
        
        # Process each chunk
        results = []
        for i, chunk in enumerate(chunks):
            chunk_filename = f"{filename}" if len(chunks) == 1 else f"{filename}_chunk_{i+1}"
            
            content_hash = hashlib.sha256(chunk.encode("utf-8", errors="ignore")).hexdigest()
            
            try:
                id_, status = db_manager.add_or_update_source(
                    chunk_filename,
                    file_path,
                    chunk,
                    content_hash=content_hash,
                    size=len(chunk),
                    modified_ts=modified_ts,
                )
                results.append(status)
                
            except Exception as e:
                logger.error(f"Database insertion failed for {chunk_filename}: {e}")
                results.append("failed")
        
        # Determine overall status
        if all(r == "unchanged" for r in results):
            print(f"📄 unchanged: {filename}")
            return "unchanged"
        elif any(r in ["inserted", "updated"] for r in results):
            chunks_info = f" ({len(chunks)} chunks)" if len(chunks) > 1 else ""
            print(f"📚 processed: {filename}{chunks_info}")
            return "updated" if any(r == "updated" for r in results) else "inserted"
        else:
            return "failed"
    
    def _extract_pdf_content(self, file_path: str) -> Tuple[str, Dict]:
        """Extract text content from PDF file."""
        content = ""
        metadata = {"type": "pdf", "pages": 0}
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            metadata["pages"] = len(pdf_reader.pages)
            
            # Extract metadata if available
            if pdf_reader.metadata:
                metadata.update({
                    "title": pdf_reader.metadata.get('/Title', ''),
                    "author": pdf_reader.metadata.get('/Author', ''),
                    "subject": pdf_reader.metadata.get('/Subject', ''),
                })
            
            # Extract text from all pages
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        content += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                except Exception as e:
                    logger.warning(f"Failed to extract page {page_num + 1} from {file_path}: {e}")
        
        return content, metadata
    
    def _extract_text_content(self, file_path: str) -> Tuple[str, Dict]:
        """Extract content from text-based files."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        metadata = {
            "type": "text",
            "extension": Path(file_path).suffix.lower()
        }
        
        return content, metadata
    
    def _chunk_content(self, content: str, filename: str, metadata: Dict) -> List[str]:
        """Intelligently chunk large content into manageable pieces."""
        # Configuration
        MAX_CHUNK_SIZE = 4000  # characters per chunk
        MIN_CHUNK_SIZE = 500   # minimum chunk size
        OVERLAP_SIZE = 200     # overlap between chunks
        
        if len(content) <= MAX_CHUNK_SIZE:
            return [content]
        
        chunks = []
        start = 0
        
        while start < len(content):
            end = start + MAX_CHUNK_SIZE
            
            # If this isn't the last chunk, try to find a good break point
            if end < len(content):
                # Look for paragraph breaks first
                paragraph_break = content.rfind('\n\n', start, end)
                if paragraph_break > start + MIN_CHUNK_SIZE:
                    end = paragraph_break
                else:
                    # Look for sentence endings
                    sentence_break = content.rfind('. ', start, end)
                    if sentence_break > start + MIN_CHUNK_SIZE:
                        end = sentence_break + 1
                    else:
                        # Look for any line break
                        line_break = content.rfind('\n', start, end)
                        if line_break > start + MIN_CHUNK_SIZE:
                            end = line_break
            
            chunk = content[start:end].strip()
            if chunk:
                # Add metadata header to first chunk
                if start == 0 and metadata:
                    header = f"Document: {filename}\n"
                    if metadata.get("title"):
                        header += f"Title: {metadata['title']}\n"
                    if metadata.get("author"):
                        header += f"Author: {metadata['author']}\n"
                    if metadata.get("pages"):
                        header += f"Pages: {metadata['pages']}\n"
                    header += "\n"
                    chunk = header + chunk
                
                chunks.append(chunk)
            
            # Move start position with overlap
            start = max(end - OVERLAP_SIZE, start + 1)
            if start >= len(content):
                break
        
        return chunks


# Enhanced sync watcher integration
def watch_and_ingest():
    """Monitor directories and trigger ingestion on changes."""
    from sync_watcher import SyncEventHandler
    from watchdog.observers import Observer
    import time
    
    print("👁️  Starting enhanced file watcher...")
    
    class EnhancedSyncHandler(SyncEventHandler):
        def __init__(self):
            super().__init__()
            self.ingestor = EnhancedFileIngestor()
        
        def trigger_ingestion(self, file_path):
            """Override to use enhanced ingestor."""
            if Path(file_path).suffix.lower() in self.ingestor.supported_extensions:
                print(f"📚 Processing: {file_path}")
                try:
                    status = self.ingestor.ingest_file(file_path)
                    print(f"✅ Status: {status}")
                except Exception as e:
                    print(f"❌ Error: {e}")
    
    handler = EnhancedSyncHandler()
    observer = Observer()
    
    # Watch both Clever_Sync and Clever_Learn
    watch_dirs = ["./Clever_Sync", "./Clever_Learn", "./synaptic_hub_sync"]
    for watch_dir in watch_dirs:
        if os.path.exists(watch_dir):
            observer.schedule(handler, watch_dir, recursive=True)
            print(f"👁️  Watching: {watch_dir}")
    
    observer.start()
    print("🚀 Enhanced file watcher active. Drop PDFs in Clever_Learn/")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("🛑 File watcher stopped")
    
    observer.join()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "watch":
        watch_and_ingest()
    else:
        # Regular ingestion
        ingestor = EnhancedFileIngestor()
        ingestor.ingest_all_files()
