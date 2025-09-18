#!/bin/bash
# Clever Backup Script
# Creates full backup of Clever application and database

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$PROJECT_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🔄 Clever Backup Script"
echo "📁 Project: $PROJECT_DIR"
echo "💾 Backup Dir: $BACKUP_DIR"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Stop Clever if running (optional)
echo
read -p "❓ Stop Clever before backup? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🛑 Stopping Clever..."
    pkill -f "python3 app.py" 2>/dev/null || echo "No Clever process found"
    sleep 2
fi

# Database backup
echo
echo "💾 Backing up SQLite database..."
if [ -f "$PROJECT_DIR/clever.db" ]; then
    cp "$PROJECT_DIR/clever.db" "$BACKUP_DIR/clever_${TIMESTAMP}.db"
    echo "✅ Database backed up: clever_${TIMESTAMP}.db"
    
    # Verify backup
    if sqlite3 "$BACKUP_DIR/clever_${TIMESTAMP}.db" ".tables" > /dev/null 2>&1; then
        echo "✅ Database backup verified"
    else
        echo "❌ Database backup verification failed"
    fi
else
    echo "⚠️  Database file not found: clever.db"
fi

# Full application backup
echo
echo "📦 Creating full application backup..."
BACKUP_NAME="clever_full_${TIMESTAMP}.tar.gz"

cd "$PROJECT_DIR" || exit 1

tar -czf "$BACKUP_DIR/$BACKUP_NAME" \
  --exclude='backups' \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='*.log' \
  --exclude='node_modules' \
  --exclude='.pytest_cache' \
  --exclude='.coverage' \
  . 2>/dev/null

if [ -f "$BACKUP_DIR/$BACKUP_NAME" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_NAME" | cut -f1)
    echo "✅ Full backup created: $BACKUP_NAME ($BACKUP_SIZE)"
else
    echo "❌ Full backup failed"
    exit 1
fi

# List recent backups
echo
echo "📋 Recent backups:"
ls -lht "$BACKUP_DIR" | head -6

# Cleanup old backups (keep last 5)
echo
OLD_BACKUPS=$(ls -t "$BACKUP_DIR"/clever_full_*.tar.gz 2>/dev/null | tail -n +6)
if [ -n "$OLD_BACKUPS" ]; then
    echo "🗑️  Cleaning up old backups..."
    echo "$OLD_BACKUPS" | xargs rm -f
    echo "✅ Old backups cleaned up"
fi

echo
echo "✅ Backup completed successfully!"
echo "💾 Database: $BACKUP_DIR/clever_${TIMESTAMP}.db"
echo "📦 Full backup: $BACKUP_DIR/$BACKUP_NAME"
echo
echo "💡 To restore:"
echo "   Database: cp backups/clever_${TIMESTAMP}.db clever.db"
echo "   Full restore: tar -xzf backups/$BACKUP_NAME"