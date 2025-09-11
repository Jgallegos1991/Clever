#!/bin/bash
# Enhanced rclone Google Drive Setup for Clever AI
# Integrates with existing rclone config or sets up new one

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Setting up rclone Google Drive integration for Clever AI...${NC}"

# Check if rclone is available
if ! command -v rclone >/dev/null 2>&1; then
    echo -e "${RED}❌ rclone not found. Installing...${NC}"
    curl https://rclone.org/install.sh | sudo bash
fi

echo -e "${GREEN}✅ rclone found: $(rclone version | head -1)${NC}"

# Check existing remotes
EXISTING_REMOTES=$(rclone listremotes 2>/dev/null)
GDRIVE_REMOTE=""

if [ -n "$EXISTING_REMOTES" ]; then
    echo -e "${BLUE}📡 Existing rclone remotes found:${NC}"
    echo "$EXISTING_REMOTES"
    
    # Look for Google Drive remotes
    for remote in $EXISTING_REMOTES; do
        remote_clean=$(echo "$remote" | tr -d ':')
        remote_type=$(rclone config show "$remote_clean" 2>/dev/null | grep -E "^type =" | cut -d'=' -f2 | tr -d ' ')
        if [ "$remote_type" = "drive" ]; then
            GDRIVE_REMOTE="$remote_clean"
            echo -e "${GREEN}✅ Found Google Drive remote: $GDRIVE_REMOTE${NC}"
            break
        fi
    done
fi

# If no Google Drive remote found, help set one up
if [ -z "$GDRIVE_REMOTE" ]; then
    echo -e "${YELLOW}⚠️  No Google Drive remote found${NC}"
    echo -e "${BLUE}🔧 Setting up Google Drive remote...${NC}"
    echo ""
    echo -e "${BLUE}Please follow these steps:${NC}"
    echo -e "1. Run: ${YELLOW}rclone config${NC}"
    echo -e "2. Choose: ${YELLOW}n) New remote${NC}"
    echo -e "3. Name it: ${YELLOW}gdrive${NC}"
    echo -e "4. Choose: ${YELLOW}drive (Google Drive)${NC}"
    echo -e "5. Leave client_id and client_secret empty (press Enter)"
    echo -e "6. Choose: ${YELLOW}1 (Full access)${NC}"
    echo -e "7. Leave root_folder_id empty (press Enter)"
    echo -e "8. Leave service_account_file empty (press Enter)"
    echo -e "9. Choose: ${YELLOW}N (No advanced config)${NC}"
    echo -e "10. Choose: ${YELLOW}Y (Yes auto config)${NC}"
    echo -e "11. This will open a browser - sign in with: ${YELLOW}lapirfta@gmail.com${NC}"
    echo -e "12. Choose: ${YELLOW}Y (Yes this is OK)${NC}"
    echo -e "13. Choose: ${YELLOW}q (Quit config)${NC}"
    echo ""
    echo -e "${GREEN}Then run this script again to complete setup!${NC}"
    
    # Offer to run config now
    echo -e "${BLUE}Would you like to run rclone config now? (y/N)${NC}"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        rclone config
        echo -e "${GREEN}✅ Please run this script again to complete setup${NC}"
    fi
    exit 0
fi

# Configure Clever AI to use the Google Drive remote
echo -e "${BLUE}🔧 Configuring Clever AI to use rclone remote: $GDRIVE_REMOTE${NC}"

# Update config.py with rclone settings
if [ -f config.py ]; then
    # Backup original config
    cp config.py config.py.backup.$(date +%s)
    echo -e "${GREEN}✅ Backed up original config.py${NC}"
fi

# Create enhanced rclone config
cat > rclone_config.py << EOF
# rclone Google Drive Configuration for Clever AI
# Auto-generated on $(date)

# Your Google Drive remote
RCLONE_REMOTE = "$GDRIVE_REMOTE"
RCLONE_ENABLED = True

# Google Drive paths
GDRIVE_CLEVER_FOLDER = "CLEVER_AI"
GDRIVE_SYNC_FOLDER = "CLEVER_AI/clever_sync"
GDRIVE_BACKUP_FOLDER = "CLEVER_AI/backup"

# Sync settings
RCLONE_SYNC_INTERVAL = 30  # seconds
RCLONE_AUTO_SYNC = True

# Performance settings
RCLONE_EXTRA = "--fast-list --checkers 8 --transfers 4 --copy-links --drive-chunk-size 64M"
EOF

# Update the main config to include rclone settings
if grep -q "RCLONE_REMOTE" config.py; then
    # Update existing rclone config
    sed -i "s/RCLONE_REMOTE = .*/RCLONE_REMOTE = \"$GDRIVE_REMOTE\"/" config.py
    sed -i "s/ENABLE_RCLONE = .*/ENABLE_RCLONE = True/" config.py
else
    # Add rclone config
    echo "" >> config.py
    echo "# rclone Configuration (auto-added)" >> config.py
    echo "RCLONE_REMOTE = \"$GDRIVE_REMOTE\"" >> config.py
    echo "ENABLE_RCLONE = True" >> config.py
fi

# Create enhanced sync script using rclone
cat > rclone_sync_clever.sh << 'EOF'
#!/bin/bash
# Enhanced rclone sync for Clever AI

set -e

REMOTE="REMOTE_PLACEHOLDER"
GDRIVE_SYNC_PATH="CLEVER_AI/clever_sync"
LOCAL_LEARN_PATH="./Clever_Learn"

echo "🔄 Syncing from Google Drive via rclone..."
echo "📡 Remote: $REMOTE"
echo "📂 GDrive path: $GDRIVE_SYNC_PATH"
echo "📁 Local path: $LOCAL_LEARN_PATH"

# Create local directory if it doesn't exist
mkdir -p "$LOCAL_LEARN_PATH"

# Sync from Google Drive to local
if rclone copy "$REMOTE:$GDRIVE_SYNC_PATH" "$LOCAL_LEARN_PATH" --verbose; then
    echo "✅ rclone sync successful"
    
    # Update timestamp
    touch "$LOCAL_LEARN_PATH/.last_rclone_sync"
    
    # Count files synced
    FILE_COUNT=$(find "$LOCAL_LEARN_PATH" -type f \( -name "*.pdf" -o -name "*.txt" -o -name "*.md" \) | wc -l)
    echo "📄 Files available for processing: $FILE_COUNT"
    
else
    echo "❌ rclone sync failed"
    exit 1
fi
EOF

# Replace placeholder with actual remote name
sed -i "s/REMOTE_PLACEHOLDER/$GDRIVE_REMOTE/g" rclone_sync_clever.sh
chmod +x rclone_sync_clever.sh

# Create continuous monitoring script
cat > watch_rclone_sync.sh << 'EOF'
#!/bin/bash
# Continuous rclone monitoring for Clever AI

echo "👁️  Starting rclone Google Drive monitoring..."
echo "📡 Using remote: REMOTE_PLACEHOLDER"
echo "🔄 Sync interval: 30 seconds"
echo ""
echo "Drop files into Google Drive CLEVER_AI/clever_sync/ folder"
echo "They will automatically sync and be processed by Clever!"
echo ""

while true; do
    ./rclone_sync_clever.sh
    if [ $? -eq 0 ]; then
        # Auto-process if new files found
        if [ -f "./Clever_Learn/.last_rclone_sync" ]; then
            NEW_FILES=$(find "./Clever_Learn" -type f \( -name "*.pdf" -o -name "*.txt" -o -name "*.md" \) -newer "./Clever_Learn/.last_rclone_sync" 2>/dev/null | wc -l)
            if [ "$NEW_FILES" -gt 0 ]; then
                echo "🧠 Processing $NEW_FILES new files..."
                make ingest-pdfs 2>/dev/null || echo "⚠️  Auto-processing failed - run 'make ingest-pdfs' manually"
            fi
        fi
    fi
    sleep 30
done
EOF

sed -i "s/REMOTE_PLACEHOLDER/$GDRIVE_REMOTE/g" watch_rclone_sync.sh
chmod +x watch_rclone_sync.sh

# Test the rclone connection
echo -e "${BLUE}🧪 Testing rclone connection...${NC}"
if rclone lsd "$GDRIVE_REMOTE:" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ rclone connection successful!${NC}"
    
    # Check if CLEVER_AI folder exists
    if rclone lsd "$GDRIVE_REMOTE:CLEVER_AI" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ CLEVER_AI folder found in Google Drive${NC}"
    else
        echo -e "${YELLOW}📁 Creating CLEVER_AI folder structure in Google Drive...${NC}"
        rclone mkdir "$GDRIVE_REMOTE:CLEVER_AI"
        rclone mkdir "$GDRIVE_REMOTE:CLEVER_AI/clever_sync"
        rclone mkdir "$GDRIVE_REMOTE:CLEVER_AI/backup"
        echo -e "${GREEN}✅ Created folder structure in Google Drive${NC}"
    fi
    
    # Do initial sync
    echo -e "${BLUE}🔄 Running initial sync...${NC}"
    ./rclone_sync_clever.sh
    
else
    echo -e "${RED}❌ rclone connection failed${NC}"
    echo -e "${BLUE}💡 Try running: rclone config reconnect $GDRIVE_REMOTE${NC}"
    exit 1
fi

# Update Makefile
if [ -f Makefile ]; then
    # Add rclone targets if they don't exist
    if ! grep -q "rclone-sync" Makefile; then
        echo "" >> Makefile
        echo "# rclone Google Drive integration" >> Makefile
        echo "rclone-sync:" >> Makefile
        echo "	@echo \"🔄 Syncing from Google Drive via rclone...\"" >> Makefile
        echo "	./rclone_sync_clever.sh" >> Makefile
        echo "" >> Makefile
        echo "rclone-watch:" >> Makefile
        echo "	@echo \"👁️  Starting rclone Google Drive monitoring...\"" >> Makefile
        echo "	./watch_rclone_sync.sh" >> Makefile
        echo "" >> Makefile
        echo "rclone-test:" >> Makefile
        echo "	@echo \"🧪 Testing rclone connection...\"" >> Makefile
        echo "	rclone lsd $GDRIVE_REMOTE: && echo \"✅ Connection OK\"" >> Makefile
    fi
fi

echo -e "${GREEN}🎉 rclone Google Drive integration setup complete!${NC}"
echo ""
echo -e "${BLUE}📁 Your Google Drive folder structure:${NC}"
echo -e "   📂 CLEVER_AI/"
echo -e "      ├── 📂 clever_sync/     ← Drop PDFs here!"
echo -e "      └── 📂 backup/          ← Automatic backups"
echo ""
echo -e "${BLUE}🚀 Available commands:${NC}"
echo -e "   ${YELLOW}make rclone-sync${NC}    - Sync once from Google Drive"
echo -e "   ${YELLOW}make rclone-watch${NC}   - Monitor Google Drive continuously"
echo -e "   ${YELLOW}make rclone-test${NC}    - Test Google Drive connection"
echo -e "   ${YELLOW}./rclone_sync_clever.sh${NC} - Direct sync script"
echo ""
echo -e "${GREEN}✨ Drop PDFs into Google Drive CLEVER_AI/clever_sync/ and Clever learns automatically!${NC}"
