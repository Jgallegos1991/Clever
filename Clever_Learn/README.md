# Clever Learn Directory

**Purpose:** Drop PDFs here for Clever to automatically learn from.

## How it Works

1. **Drop PDFs:** Place any PDF documents in this folder
2. **Auto-Detection:** The sync watcher monitors this directory
3. **Smart Processing:** PDFs are extracted and chunked intelligently
4. **Knowledge Integration:** Content becomes part of Clever's knowledge base

## Supported Formats

- ✅ **PDF Documents** - Primary target, full text extraction
- ✅ **Text Files** - Direct ingestion
- ✅ **Markdown Files** - Structured content processing
- 🔄 **Future:** Word docs, presentations, code files

## Processing Features

- **Smart Chunking:** Large documents split into digestible sections
- **Metadata Extraction:** Title, author, creation date preserved
- **Content Deduplication:** Prevents duplicate ingestion
- **Progress Tracking:** Monitor processing status in logs

## Usage

Simply drop your PDFs here and run:

```bash
# Manual trigger
make ingest

# Or use the auto-watcher
make watch
```

**Note:** Processing happens automatically when sync_watcher is running. Check logs for ingestion status.
