#!/bin/bash
# Continuous PDF monitoring from Google Drive

echo "👁️  Starting Google Drive PDF watcher..."
echo "📁 Monitoring: /home/vscode/GoogleDrive/CLEVER_AI/clever_sync"
echo "🎯 Target: ./Clever_Learn"
echo ""
echo "Drop PDFs into your Google Drive CLEVER_AI/clever_sync folder"
echo "They will automatically be processed by Clever!"
echo ""

while true; do
    ./sync_pdfs.sh
    sleep 30  # Check every 30 seconds
done
