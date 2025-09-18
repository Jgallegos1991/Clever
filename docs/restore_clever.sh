#!/bin/bash
# Clever Restore Script  
# Restores Clever from backup files

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$PROJECT_DIR/backups"

echo "🔄 Clever Restore Script"
echo "📁 Project: $PROJECT_DIR"
echo "💾 Backup Dir: $BACKUP_DIR"

# Check if backups exist
if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A "$BACKUP_DIR" 2>/dev/null)" ]; then
    echo "❌ No backup directory or backups found"
    echo "💡 Run backup_clever.sh first to create backups"
    exit 1
fi

# List available backups
echo
echo "📋 Available backups:"
echo
echo "🗄️  Database backups:"
ls -lht "$BACKUP_DIR"/clever_memory_*.db 2>/dev/null | head -5 || echo "   No database backups found"

echo
echo "📦 Full application backups:"
ls -lht "$BACKUP_DIR"/clever_full_*.tar.gz 2>/dev/null | head -5 || echo "   No full backups found"

# Choose restore type
echo
echo "🔧 Restore Options:"
echo "1) Database only"
echo "2) Full application"
echo "3) List backup contents"
echo "4) Exit"
echo
read -p "Choose option (1-4): " -n 1 -r
echo

case $REPLY in
    1)
        echo "🗄️  Database restore selected"
        DB_BACKUPS=($(ls -t "$BACKUP_DIR"/clever_memory_*.db 2>/dev/null))
        
        if [ ${#DB_BACKUPS[@]} -eq 0 ]; then
            echo "❌ No database backups found"
            exit 1
        fi
        
        echo "Available database backups:"
        for i in "${!DB_BACKUPS[@]}"; do
            echo "$((i+1))) $(basename "${DB_BACKUPS[$i]}")"
        done
        
        read -p "Select backup number: " -r
        BACKUP_INDEX=$((REPLY-1))
        
        if [ $BACKUP_INDEX -ge 0 ] && [ $BACKUP_INDEX -lt ${#DB_BACKUPS[@]} ]; then
            SELECTED_BACKUP="${DB_BACKUPS[$BACKUP_INDEX]}"
            
            # Stop Clever
            echo "🛑 Stopping Clever..."
            pkill -f "python3 app.py" 2>/dev/null
            sleep 2
            
            # Backup current database
            if [ -f "$PROJECT_DIR/clever.db" ]; then
                mv "$PROJECT_DIR/clever.db" "$PROJECT_DIR/clever.db.bak"
                echo "📋 Current database backed up as clever.db.bak"
            fi
            
            # Restore
            cp "$SELECTED_BACKUP" "$PROJECT_DIR/clever.db"
            echo "✅ Database restored from: $(basename "$SELECTED_BACKUP")"
            
            # Verify
            if sqlite3 "$PROJECT_DIR/clever.db" ".tables" > /dev/null 2>&1; then
                echo "✅ Database verification successful"
            else
                echo "❌ Database verification failed"
                if [ -f "$PROJECT_DIR/clever.db.bak" ]; then
                    mv "$PROJECT_DIR/clever.db.bak" "$PROJECT_DIR/clever.db"
                    echo "🔄 Restored original database"
                fi
                exit 1
            fi
        else
            echo "❌ Invalid selection"
            exit 1
        fi
        ;;
        
    2)
        echo "📦 Full application restore selected"
        FULL_BACKUPS=($(ls -t "$BACKUP_DIR"/clever_full_*.tar.gz 2>/dev/null))
        
        if [ ${#FULL_BACKUPS[@]} -eq 0 ]; then
            echo "❌ No full backups found"
            exit 1
        fi
        
        echo "Available full backups:"
        for i in "${!FULL_BACKUPS[@]}"; do
            echo "$((i+1))) $(basename "${FULL_BACKUPS[$i]}")"
        done
        
        read -p "Select backup number: " -r
        BACKUP_INDEX=$((REPLY-1))
        
        if [ $BACKUP_INDEX -ge 0 ] && [ $BACKUP_INDEX -lt ${#FULL_BACKUPS[@]} ]; then
            SELECTED_BACKUP="${FULL_BACKUPS[$BACKUP_INDEX]}"
            
            echo "⚠️  WARNING: This will overwrite current application files!"
            read -p "Continue? (y/N): " -n 1 -r
            echo
            
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                # Stop Clever
                echo "🛑 Stopping Clever..."
                pkill -f "python3 app.py" 2>/dev/null
                sleep 2
                
                # Extract to temporary directory first
                TEMP_DIR=$(mktemp -d)
                echo "📦 Extracting backup to temporary location..."
                
                if tar -xzf "$SELECTED_BACKUP" -C "$TEMP_DIR"; then
                    echo "✅ Backup extracted successfully"
                    
                    # Move current files to backup (optional)
                    CURRENT_BACKUP="current_$(date +%Y%m%d_%H%M%S)"
                    mkdir -p "$BACKUP_DIR/$CURRENT_BACKUP"
                    
                    echo "💾 Backing up current files..."
                    cp -r "$PROJECT_DIR"/* "$BACKUP_DIR/$CURRENT_BACKUP/" 2>/dev/null
                    
                    # Restore files
                    echo "🔄 Restoring application files..."
                    cp -r "$TEMP_DIR"/* "$PROJECT_DIR/"
                    
                    # Cleanup
                    rm -rf "$TEMP_DIR"
                    
                    echo "✅ Full application restored from: $(basename "$SELECTED_BACKUP")"
                    echo "💾 Previous files backed up to: $BACKUP_DIR/$CURRENT_BACKUP"
                else
                    echo "❌ Failed to extract backup"
                    rm -rf "$TEMP_DIR"
                    exit 1
                fi
            else
                echo "❌ Restore cancelled"
            fi
        else
            echo "❌ Invalid selection"
            exit 1
        fi
        ;;
        
    3)
        echo "📋 Backup contents listing"
        FULL_BACKUPS=($(ls -t "$BACKUP_DIR"/clever_full_*.tar.gz 2>/dev/null))
        
        if [ ${#FULL_BACKUPS[@]} -eq 0 ]; then
            echo "❌ No full backups found"
            exit 1
        fi
        
        echo "Select backup to examine:"
        for i in "${!FULL_BACKUPS[@]}"; do
            echo "$((i+1))) $(basename "${FULL_BACKUPS[$i]}")"
        done
        
        read -p "Select backup number: " -r
        BACKUP_INDEX=$((REPLY-1))
        
        if [ $BACKUP_INDEX -ge 0 ] && [ $BACKUP_INDEX -lt ${#FULL_BACKUPS[@]} ]; then
            echo "📋 Contents of $(basename "${FULL_BACKUPS[$BACKUP_INDEX]}"):"
            tar -tzf "${FULL_BACKUPS[$BACKUP_INDEX]}" | head -20
            echo "..."
            echo "Total files: $(tar -tzf "${FULL_BACKUPS[$BACKUP_INDEX]}" | wc -l)"
        fi
        ;;
        
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
        
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo
echo "✅ Restore operation completed!"
echo "💡 You can now start Clever with: python3 app.py"