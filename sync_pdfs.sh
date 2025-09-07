#!/bin/bash
# PDF Sync Script - monitors and syncs PDFs from Google Drive

GDRIVE_PDF_FOLDER="/home/vscode/GoogleDrive/CLEVER_AI/clever_sync"
LOCAL_SYNC="./Clever_Sync"
LOCAL_LEARN="./Clever_Learn" 

echo "🔄 Syncing PDFs from Google Drive..."
echo "📂 Source: $GDRIVE_PDF_FOLDER"
echo "📂 Target: $LOCAL_LEARN"

# Sync PDFs to Clever_Learn folder for processing
if [ -d "$GDRIVE_PDF_FOLDER" ]; then
    # Find and copy new PDFs and other documents
    echo "📄 Looking for new files..."
    find "$GDRIVE_PDF_FOLDER" -type f \( -name "*.pdf" -o -name "*.txt" -o -name "*.md" \) -newer "$LOCAL_LEARN/.last_sync" 2>/dev/null | while read file; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            echo "📄 Syncing: $filename"
            cp "$file" "$LOCAL_LEARN/"
        fi
    done
    
    # Update timestamp
    touch "$LOCAL_LEARN/.last_sync"
    echo "✅ Document sync complete"
else
    echo "❌ Google Drive folder not found: $GDRIVE_PDF_FOLDER"
    exit 1
fi
