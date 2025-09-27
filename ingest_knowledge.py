import time
#!/usr/bin/env python3
"""Knowledge Ingestion Utility for Clever's Learning System

Why: Provides a simple way to ingest all files from the Clever_Learn directory
     into Clever's knowledge base for conversation enhancement.
Where: Standalone utility that can be run manually or scheduled.
How: Scans Clever_Learn directory, processes all text and markdown files,
     and stores them in the unified database for persona engine access.

Usage:
    python3 ingest_knowledge.py
    python3 ingest_knowledge.py --directory /path/to/files
    python3 ingest_knowledge.py --watch (starts file watcher)

Connects to:
    - database.py: Uses DatabaseManager for knowledge storage
    - persona.py: Ingested content becomes available for conversation
    - sync_watcher.py: Can trigger this for automatic ingestion
"""

import argparse

from database import DatabaseManager
from debug_config import get_debugger

debugger = get_debugger()

class KnowledgeIngestor:
    """Simplified knowledge ingestor focusing on text-based content"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize the knowledge ingestor
        
        Why: Set up database connection and configure processing options
        Where: Called when creating ingestor instance
        How: Initialize DatabaseManager with configured database path
        """
        self.db_path = db_path or config.DB_PATH
        self.db = DatabaseManager(self.db_path)
        self.supported_extensions = {'.txt', '.md', '.rst', '.log', '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml'}
        
    def ingest_file(self, file_path: Path) -> str:
        """
        Ingest a single file into the knowledge base
        
        Why: Process individual files and store their content for conversation use
        Where: Called for each file during directory ingestion
        How: Read file content, generate hash, store in database with metadata
        
        Returns:
            Status string: 'inserted', 'updated', 'unchanged', 'skipped', or 'failed'
        """
        try:
            if not file_path.exists() or not file_path.is_file():
                return 'skipped'
                
            if file_path.suffix.lower() not in self.supported_extensions:
                debugger.info('knowledge_ingestor', f'Skipping unsupported file: {file_path}')
                return 'skipped'
                
            # Read file content
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                debugger.warning('knowledge_ingestor', f'Failed to read {file_path}: {e}')
                return 'failed'
                
            if not content.strip():
                debugger.info('knowledge_ingestor', f'Empty file skipped: {file_path}')
                return 'skipped'
                
            # Generate content hash
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            # Get file stats
            stat = file_path.stat()
            
            # Store in database
            file_id, status = self.db.add_or_update_source(
                filename=file_path.name,
                path=str(file_path.absolute()),
                content=content,
                content_hash=content_hash,
                size=stat.st_size,
                modified_ts=stat.st_mtime
            )
            
            debugger.info('knowledge_ingestor', f'Processed {file_path.name}: {status}')
            return status
            
        except Exception:
            debugger.error('knowledge_ingestor', f'Failed to process {file_path}: {e}')
            return 'failed'
            
    def ingest_directory(self, directory: Path, recursive: bool = True) -> dict:
        """
        Ingest all supported files from a directory
        
        Why: Batch process entire directories of knowledge content
        Where: Main entry point for bulk knowledge ingestion
        How: Walk directory tree, process each supported file
        
        Returns:
            Dictionary with processing statistics
        """
        if not directory.exists() or not directory.is_dir():
            debugger.error('knowledge_ingestor', f'Directory not found: {directory}')
            return {'error': 'Directory not found'}
            
        stats = {
            'inserted': 0,
            'updated': 0, 
            'unchanged': 0,
            'skipped': 0,
            'failed': 0,
            'total': 0
        }
        
        # Get all files to process
        pattern = '**/*' if recursive else '*'
        files = [f for f in directory.glob(pattern) if f.is_file() and not f.name.startswith('.')]
        
        debugger.info('knowledge_ingestor', f'Processing {len(files)} files from {directory}')
        
        for file_path in files:
            status = self.ingest_file(file_path)
            stats[status] += 1
            stats['total'] += 1
            
        return stats

def main():
    """Main entry point for knowledge ingestion utility"""
    parser = argparse.ArgumentParser(description='Ingest knowledge files into Clever\'s database')
    parser.add_argument('--directory', '-d', type=Path, 
                       default=Path('Clever_Learn'),
                       help='Directory to ingest (default: Clever_Learn)')
    parser.add_argument('--recursive', '-r', action='store_true', 
                       help='Process subdirectories recursively')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    print("🧠 Clever Knowledge Ingestion Utility")
    print(f"📁 Processing directory: {args.directory.absolute()}")
    
    # Create ingestor
    ingestor = KnowledgeIngestor()
    
    # Process directory
    start_time = time.time()
    stats = ingestor.ingest_directory(args.directory, recursive=args.recursive)
    duration = time.time() - start_time
    
    # Report results
    if 'error' in stats:
        print(f"❌ Error: {stats['error']}")
        return 1
        
    print(f"\n📊 Ingestion Results (completed in {duration:.2f}s):")
    print(f"   ✅ Inserted: {stats['inserted']}")
    print(f"   🔄 Updated:  {stats['updated']}")
    print(f"   ⚡ Unchanged: {stats['unchanged']}")
    print(f"   ⏭️  Skipped:  {stats['skipped']}")
    print(f"   ❌ Failed:   {stats['failed']}")
    print(f"   📈 Total:    {stats['total']}")
    
    if stats['inserted'] + stats['updated'] > 0:
        print(f"\n🎉 Knowledge base updated! Clever now has access to {stats['inserted'] + stats['updated']} new/updated files.")
    else:
        print("\n✨ Knowledge base is up to date!")
        
    return 0

if __name__ == '__main__':
    exit(main())