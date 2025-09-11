#!/bin/bash
# Google Drive PDF Sync for Clever AI
# Monitors Google Drive folder and syncs PDFs to Clever for learning

set -e

# Configuration
GOOGLE_DRIVE_CLEVER_FOLDER="$HOME/GoogleDrive/CLEVER_AI"
GOOGLE_DRIVE_PDF_FOLDER="$GOOGLE_DRIVE_CLEVER_FOLDER/clever_sync"
LOCAL_CLEVER_SYNC="$PWD/Clever_Sync"
LOCAL_LEARN_FOLDER="$PWD/Clever_Learn"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Setting up Google Drive PDF sync for Clever AI...${NC}"

# Create directories if they don't exist
mkdir -p "$LOCAL_CLEVER_SYNC"
mkdir -p "$LOCAL_LEARN_FOLDER"

# Check for Google Drive mount points
GDRIVE_PATHS=(
    "$HOME/GoogleDrive/MyDrive/CLEVER_AI/clever_sync"
    "$HOME/Google Drive/CLEVER_AI/clever_sync"
    "/mnt/chromeos/GoogleDrive/MyDrive/CLEVER_AI/clever_sync"
    "/mnt/chromeos/removable/GoogleDrive/CLEVER_AI/clever_sync"
    "$HOME/gdrive/CLEVER_AI/clever_sync"
)

FOUND_GDRIVE=""
for path in "${GDRIVE_PATHS[@]}"; do
    if [ -d "$path" ]; then
        FOUND_GDRIVE="$path"
        echo -e "${GREEN}✅ Found Google Drive at: $path${NC}"
        break
    fi
done

if [ -z "$FOUND_GDRIVE" ]; then
    echo -e "${YELLOW}⚠️  Google Drive not found at standard locations${NC}"
    echo -e "${BLUE}📁 Creating local simulation of Google Drive structure...${NC}"
    
    # Create local Google Drive simulation
    mkdir -p "$GOOGLE_DRIVE_PDF_FOLDER"
    FOUND_GDRIVE="$GOOGLE_DRIVE_PDF_FOLDER"
    
    echo -e "${GREEN}✅ Created: $GOOGLE_DRIVE_PDF_FOLDER${NC}"
    echo -e "${BLUE}💡 You can now drop PDFs into this folder:${NC}"
    echo -e "   📂 $GOOGLE_DRIVE_PDF_FOLDER"
fi

# Create sync script
cat > sync_pdfs.sh << 'EOF'
#!/bin/bash
# PDF Sync Script - monitors and syncs PDFs from Google Drive with Evolution Integration

GDRIVE_PDF_FOLDER="GDRIVE_FOLDER_PLACEHOLDER"
LOCAL_SYNC="./Clever_Sync"
LOCAL_LEARN="./Clever_Learn" 

echo "🔄 Syncing PDFs from Google Drive..."
echo "📂 Source: $GDRIVE_PDF_FOLDER"
echo "📂 Target: $LOCAL_LEARN"

# Sync PDFs, text files, and markdown files to Clever_Learn folder for processing
if [ -d "$GDRIVE_PDF_FOLDER" ]; then
    # Find and copy new files (PDFs, text, markdown)
    find "$GDRIVE_PDF_FOLDER" \( -name "*.pdf" -o -name "*.txt" -o -name "*.md" \) -newer "$LOCAL_LEARN/.last_sync" 2>/dev/null | while read file; do
        if [ -f "$file" ]; then
            echo "📄 Syncing: $(basename "$file")"
            cp "$file" "$LOCAL_LEARN/"
            
            # Trigger evolution learning for PDFs
            if [[ "$file" == *.pdf ]]; then
                echo "🧠 Triggering Clever evolution for: $(basename "$file")"
                python3 -c "
from evolution_engine import get_evolution_engine
import sys, os
sys.path.append('$PWD')

try:
    engine = get_evolution_engine()
    # PDF will be processed by file_ingestor which will call evolution engine
    print('✨ Evolution engine ready for PDF learning')
except Exception as e:
    print(f'⚠️ Evolution engine error: {e}')
"
            fi
        fi
    done
    
    # Update timestamp
    touch "$LOCAL_LEARN/.last_sync"
    echo "✅ PDF sync complete"
else
    echo "❌ Google Drive folder not found: $GDRIVE_PDF_FOLDER"
    exit 1
fi
EOF

# Replace placeholder with actual path
sed -i "s|GDRIVE_FOLDER_PLACEHOLDER|$FOUND_GDRIVE|g" sync_pdfs.sh
chmod +x sync_pdfs.sh

# Create watcher script for continuous monitoring
cat > watch_gdrive_pdfs.sh << 'EOF'
#!/bin/bash
# Continuous PDF monitoring from Google Drive

echo "👁️  Starting Google Drive PDF watcher..."
echo "📁 Monitoring: GDRIVE_FOLDER_PLACEHOLDER"
echo "🎯 Target: ./Clever_Learn"
echo ""
echo "Drop PDFs into your Google Drive CLEVER_AI/clever_sync folder"
echo "They will automatically be processed by Clever!"
echo ""

while true; do
    ./sync_pdfs.sh
    sleep 30  # Check every 30 seconds
done
EOF

sed -i "s|GDRIVE_FOLDER_PLACEHOLDER|$FOUND_GDRIVE|g" watch_gdrive_pdfs.sh
chmod +x watch_gdrive_pdfs.sh

# Create sample instructions file
cat > "$FOUND_GDRIVE/README_CLEVER_PDF_SYNC.md" << 'EOF'
# 📚 Clever AI PDF Learning

## How to Add PDFs for Clever to Learn:

1. **Drop PDFs here** - Just drag and drop PDF files into this folder
2. **Automatic Processing** - Clever will automatically detect and process them
3. **Smart Learning** - PDFs are chunked intelligently and added to Clever's knowledge

## Supported Files:
- ✅ PDF documents
- ✅ Text files (.txt)
- ✅ Markdown files (.md)

## Examples of what to add:
- Research papers
- Documentation
- Books
- Articles
- Technical manuals
- Personal notes

## Processing:
- Files are automatically synced every 30 seconds
- Clever will extract text and create smart chunks
- Knowledge is immediately available in conversations

**Just drop files here and Clever gets smarter! 🧠✨**
EOF

echo -e "${GREEN}✅ PDF sync setup complete!${NC}"
echo ""
echo -e "${BLUE}📁 Your Google Drive PDF folder:${NC}"
echo -e "   $FOUND_GDRIVE"
echo ""
echo -e "${BLUE}🔄 To start automatic PDF monitoring:${NC}"
echo -e "   ${YELLOW}./watch_gdrive_pdfs.sh${NC}"
echo ""
echo -e "${BLUE}🔄 To sync PDFs once:${NC}"
echo -e "   ${YELLOW}./sync_pdfs.sh${NC}"
echo ""
echo -e "${GREEN}💡 Just drop PDFs into the Google Drive folder and Clever will learn them automatically!${NC}"
