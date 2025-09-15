# Sample Knowledge Document

## Introduction
This is a sample document to demonstrate Clever's learning capabilities. When you place real PDFs in this directory, Clever will automatically extract and learn from their content.

## Key Features

### Intelligent Processing
- **PDF Text Extraction**: Extracts readable text from PDF documents
- **Smart Chunking**: Breaks large documents into digestible sections
- **Metadata Preservation**: Maintains document titles, authors, and structure
- **Deduplication**: Prevents processing the same content multiple times

### Content Types Supported
1. **Research Papers**: Academic and technical documents
2. **Books**: Technical manuals and guides  
3. **Reports**: Business and technical reports
4. **Documentation**: API docs, user manuals, specifications
5. **Articles**: Blog posts, tutorials, white papers

## How It Works

When you drop a PDF into this folder:

1. **Detection**: File watcher notices the new document
2. **Extraction**: Text content is extracted using PyPDF2
3. **Analysis**: Content is analyzed for keywords and structure
4. **Chunking**: Large documents are split into manageable sections
5. **Storage**: Content is indexed in Clever's knowledge base
6. **Integration**: Information becomes part of Clever's responses

## Example Usage

```bash
# Drop PDFs in Clever_Learn/
cp ~/Downloads/research_paper.pdf ./Clever_Learn/

# Process manually
make ingest-pdfs

# Or start auto-watching
make watch-pdfs
```

## Benefits

- **Instant Knowledge**: PDFs become part of Clever's understanding immediately
- **Contextual Responses**: Clever can reference and quote from your documents
- **Smart Search**: Find information across all your documents
- **Offline Operation**: Everything happens locally, no cloud dependencies

This system turns Clever into your personal research assistant that actually knows your documents!
