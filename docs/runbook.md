# Clever AI - Operations Runbook

**Version:** 1.0  
**Created:** 2025-09-04  
**Purpose:** Comprehensive operational guide for the Clever Flask application

## Changelog
- 2025-09-04: Initial runbook creation with startup procedures, troubleshooting, and testing guidance

---

## Overview

Clever is an offline-first Flask application serving as Jordan's AI co-pilot and strategic thinking partner. The application uses:
- **Backend:** Flask 3.1.1 with SQLite database
- **NLP:** spaCy (en_core_web_sm), NLTK, TextBlob for natural language processing  
- **Storage:** SQLite (`clever_memory.db`) for persistent data
- **UI:** Dark theme with particle effects, responsive design
- **Dependencies:** 50+ Python packages (see `requirements.txt`)

---

## Clean Start Procedures

### Prerequisites
- Python 3.8+ with pip
- 4GB+ RAM (for spaCy model loading)
- 1GB+ disk space

### Initial Setup

1. **Clone and navigate to repository:**
   ```bash
   git clone https://github.com/Jgallegos1991/projects.git
   cd projects
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This downloads ~30MB+ including spaCy model data*

3. **Verify installation:**
   ```bash
   python3 -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✅ spaCy model loaded')"
   ```

### Environment Configuration

Clever uses hardcoded configuration in `config.py`. No `.env` file is required, but you can create one for customization:

**Optional `.env` file:**
```bash
# Create .env file (optional)
cat > .env << EOF
FLASK_DEBUG=true
FLASK_PORT=5000
SAFE_MODE=false
BACKUP_DIR=./backups
EOF
```

**Configuration locations:**
- Database: `./clever_memory.db` (auto-created)
- Uploads: `./uploads/` (auto-created)
- Backups: `./backups/` (auto-created)
- Static files: `./static/`
- Templates: `./templates/`

### Port Selection & Flask Startup

**Default startup (port 5000):**
```bash
python3 app.py
```

**Custom port startup:**
```bash
# Edit app.py line 224 to change port, or use environment variable
FLASK_RUN_PORT=8080 python3 app.py
```

**Alternative Flask commands:**
```bash
# Using flask run (requires FLASK_APP env var)
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5001 --debug

# Background execution
nohup python3 app.py > clever.log 2>&1 &
```

---

## First-Run Database Initialization

### Automatic Initialization
The database initializes automatically on first startup via `database.py`:

```python
# Tables created automatically:
# - sources: File upload tracking
# - knowledge: Fact storage
# - conversations: Chat history
# - system_state: Application state
```

### Manual Database Verification
```bash
# Check if database exists and is accessible
sqlite3 clever_memory.db ".tables"
# Expected output: conversations  knowledge  sources  system_state

# Verify table schemas
sqlite3 clever_memory.db ".schema sources"
```

### Database Reset (if needed)
```bash
# ⚠️  WARNING: This destroys all data
rm clever_memory.db
python3 app.py  # Will recreate database
```

---

## Common Failures & Fixes

### 1. Port 5000 Already in Use

**Error:** `OSError: [Errno 98] Address already in use`

**Solutions:**
```bash
# Find process using port 5000
lsof -i :5000
netstat -tuln | grep 5000

# Kill process (replace PID)
kill -9 <PID>

# Or use different port
sed -i 's/port=5000/port=5001/g' app.py
```

### 2. spaCy Model Missing

**Error:** `OSError: [E050] Can't find model 'en_core_web_sm'`

**Fix:**
```bash
python3 -m spacy download en_core_web_sm
# Or reinstall
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

### 3. NLTK Data Missing

**Error:** `LookupError: Resource vader_lexicon not found`

**Fix:** Data downloads automatically, but if issues persist:
```bash
python3 -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
```

### 4. SQLite Permission Issues

**Error:** `sqlite3.OperationalError: unable to open database file`

**Fix:**
```bash
# Check directory permissions
ls -la clever_memory.db
chmod 664 clever_memory.db
chmod 755 .
```

### 5. Memory Issues (spaCy Loading)

**Error:** Process killed or out of memory during startup

**Solutions:**
```bash
# Enable safe mode (no NLP processing)
# Edit app.py line 9: SAFE_MODE = True

# Or increase swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 6. Template/Static Files Missing

**Error:** `jinja2.exceptions.TemplateNotFound`

**Fix:**
```bash
# Verify directory structure
ls -la templates/ static/
# Should contain index.html and static assets

# If missing, check git status
git status
git checkout HEAD -- templates/ static/
```

---

## Smoke Tests for Endpoints

### Automated Test Script
```bash
#!/bin/bash
# Create test script: test_endpoints.sh

BASE_URL="http://127.0.0.1:5000"
echo "🧪 Starting Clever endpoint smoke tests..."

# Test 1: Health check
echo "1. Testing health endpoint..."
curl -f -s "$BASE_URL/health" | jq . || echo "❌ Health check failed"

# Test 2: Capabilities
echo "2. Testing capabilities endpoint..."
curl -f -s "$BASE_URL/capabilities" | jq .name || echo "❌ Capabilities failed"

# Test 3: Main page
echo "3. Testing main page..."
curl -f -s "$BASE_URL/" | grep -q "Synaptic Hub" && echo "✅ Main page OK" || echo "❌ Main page failed"

# Test 4: Chat endpoint (POST)
echo "4. Testing chat endpoint..."
curl -f -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Clever"}' | jq .reply || echo "❌ Chat failed"

# Test 5: Static files
echo "5. Testing static file serving..."
curl -f -s "$BASE_URL/favicon.ico" > /dev/null && echo "✅ Static files OK" || echo "❌ Static files failed"

echo "🏁 Smoke tests completed"
```

### Manual Testing Steps

1. **Start application:**
   ```bash
   python3 app.py
   ```

2. **Test endpoints:**
   ```bash
   # Health check - should return {"status": "ok"}
   curl http://127.0.0.1:5000/health

   # Capabilities - should return Clever's info
   curl http://127.0.0.1:5000/capabilities

   # Main UI - should return HTML
   curl http://127.0.0.1:5000/

   # Chat test - should return AI response
   curl -X POST http://127.0.0.1:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "test message"}'
   ```

3. **UI functionality:**
   - Open browser to `http://127.0.0.1:5000`
   - Verify dark theme with particle effects loads
   - Test chat interface input/response
   - Check for JavaScript console errors (F12)

---

## Backup & Restore Procedures

### SQLite Database Backup

**Manual backup:**
```bash
# Create timestamped backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp clever_memory.db "backups/clever_memory_${TIMESTAMP}.db"

# Verify backup
sqlite3 "backups/clever_memory_${TIMESTAMP}.db" ".tables"
```

**Automated backup using BackupManager:**
```bash
python3 -c "
from backup_manager import BackupManager
bm = BackupManager('.', keep_latest=5)
bm.create_backup()
"
```

### Memory Store Backup

**Full application backup:**
```bash
#!/bin/bash
# backup_clever.sh
BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="clever_full_${TIMESTAMP}"

mkdir -p "$BACKUP_DIR"

# Create compressed backup
tar -czf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" \
  --exclude='backups' \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='node_modules' \
  .

echo "✅ Full backup created: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
```

### Restore Procedures

**Database restore:**
```bash
# Stop application first
pkill -f "python3 app.py"

# Restore from backup
cp backups/clever_memory_20250904_143000.db clever_memory.db

# Restart application
python3 app.py
```

**Full application restore:**
```bash
# Extract backup to new directory
mkdir clever_restored
tar -xzf backups/clever_full_20250904_143000.tar.gz -C clever_restored/

# Move files (careful not to overwrite current)
cd clever_restored && cp -r * ../
```

**Automated restore script:**
```bash
#!/bin/bash
# restore_clever.sh
if [ -z "$1" ]; then
  echo "Usage: $0 <backup_filename>"
  echo "Available backups:"
  ls backups/
  exit 1
fi

echo "🔄 Stopping Clever..."
pkill -f "python3 app.py"

echo "📦 Restoring from $1..."
cp "backups/$1" clever_memory.db

echo "🚀 Restarting Clever..."
python3 app.py &

echo "✅ Restore completed"
```

---

## Production Deployment Notes

### Security Considerations
- Disable debug mode: Set `debug=False` in `app.run()`
- Use production WSGI server (Gunicorn, uWSGI)
- Implement proper logging configuration
- Set up log rotation for `clever.log`

### Performance Tuning
- Consider SQLite WAL mode for concurrent access
- Implement caching for NLP results
- Monitor memory usage during spaCy processing
- Use process monitoring (systemd, supervisor)

### Monitoring Commands
```bash
# Monitor memory usage
ps aux | grep python3 | grep app.py

# Check log files
tail -f clever.log

# Database size monitoring
ls -lh clever_memory.db
sqlite3 clever_memory.db "SELECT COUNT(*) as conversations FROM conversations;"
```

---

## Support & Troubleshooting

### Debug Mode Information
When running with `debug=True` (default):
- Automatic reload on code changes
- Detailed error pages in browser
- Debug PIN displayed in console for debugger access

### Common Debug Steps
1. Check console output for error messages
2. Verify all required files exist (`ls -la`)
3. Test with `SAFE_MODE = True` to isolate NLP issues
4. Check browser developer console for frontend errors
5. Examine SQLite database integrity: `sqlite3 clever_memory.db "PRAGMA integrity_check;"`

### Getting Help
- Check application logs: `tail -50 clever.log`
- Review database status: `sqlite3 clever_memory.db ".tables"`
- Test with minimal config: Enable `SAFE_MODE` in `app.py`
- Verify Python environment: `pip list | grep -E "(flask|spacy|nltk)"`

---

*End of Runbook - Last updated: 2025-09-04*
# Operations Runbook

## System Startup & Shutdown

### Starting Clever
```bash
# Activate virtual environment (if using)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

### Shutdown Procedures
```bash
# Graceful shutdown: Ctrl+C in terminal
# Force shutdown: kill -TERM <flask_pid>
```

### Health Checks
- **Database Connection**: Verify `clever_memory.db` accessibility
- **spaCy Model**: Confirm `en_core_web_sm` is loaded
- **Static Assets**: Check Three.js and frontend resources
- **Port Availability**: Default Flask port (typically 5000)

## Database Operations

### Backup Procedures
```bash
# Manual backup using backup_manager.py
python backup_manager.py --create-backup

# Automated backup (configured in system)
# Backups stored in /backups/ directory
```

### Database Maintenance
```bash
# Check database integrity
sqlite3 clever_memory.db "PRAGMA integrity_check;"

# Vacuum database to reclaim space
sqlite3 clever_memory.db "VACUUM;"

# View database schema
sqlite3 clever_memory.db ".schema"
```

### Data Recovery
```bash
# Restore from backup
python backup_manager.py --restore-backup <backup_file>

# Emergency recovery from conversations.json
python database.py --import-conversations conversations.json
```

## Development Workflows

### Development Server
```bash
# Development mode with auto-reload
export FLASK_ENV=development
python app.py

# Safe mode (minimal dependencies)
# Modify SAFE_MODE = True in app.py
```

### Testing Procedures
```bash
# Run NLP processing tests
python nlp_processor.py --test

# Test database connectivity
python database.py --test-connection

# Frontend functionality test
# Open browser to localhost:5000
```

### File Ingestion
```bash
# Upload files via web interface
# Or directly process files:
python file_ingestor.py --process <file_path>
```

## Maintenance Procedures

### Regular Maintenance (Weekly)
1. **Database Backup**: Automatic via `backup_manager.py`
2. **Log Rotation**: Check application logs for errors
3. **Storage Cleanup**: Remove old temporary files
4. **Dependency Updates**: Review `requirements.txt` for security updates

### Monthly Maintenance
1. **Database Optimization**: Run VACUUM on SQLite database
2. **Conversation Archive**: Export old conversations if needed
3. **Asset Cleanup**: Remove unused static files
4. **Performance Review**: Check response times and memory usage

### Emergency Procedures
1. **System Recovery**: Restore from latest backup
2. **Data Corruption**: Use conversation JSON as fallback
3. **Performance Issues**: Check database locks and restart
4. **Memory Leaks**: Monitor Python process memory usage

## Configuration Management

### Environment Variables
- `FLASK_ENV`: development/production
- `DATABASE_PATH`: SQLite database location
- `BACKUP_DIR`: Backup storage directory
- `UPLOAD_FOLDER`: File upload location

### Configuration Files
- **`config.py`**: Primary configuration settings
- **`requirements.txt`**: Python dependencies
- **`Makefile`**: Build and development commands

## Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check database file permissions
ls -la clever_memory.db
# Verify SQLite installation
sqlite3 --version
```

#### spaCy Model Issues
```bash
# Reinstall spaCy model
python -m spacy download en_core_web_sm
# Verify model installation
python -c "import spacy; spacy.load('en_core_web_sm')"
```

#### Frontend Not Loading
```bash
# Check static file permissions
ls -la static/
# Verify Three.js files
ls -la static/vendor/three*
```

#### Performance Issues
```bash
# Monitor system resources
htop
# Check database size
du -h clever_memory.db
# Monitor Flask process
ps aux | grep python
```

## TODO Items

### Operational Procedures
- [ ] Document production deployment procedures
- [ ] Create monitoring and alerting setup
- [ ] Document log aggregation and analysis
- [ ] Create performance benchmarking procedures
- [ ] Document capacity planning guidelines

### Maintenance Automation
- [ ] Create automated health check scripts
- [ ] Set up automated backup verification
- [ ] Document dependency update procedures
- [ ] Create system cleanup automation
- [ ] Document configuration drift detection

### Emergency Response
- [ ] Create incident response procedures
- [ ] Document data recovery scenarios
- [ ] Create system rollback procedures
- [ ] Document emergency contact information
- [ ] Create disaster recovery testing procedures

### Security Operations
- [ ] Document security audit procedures
- [ ] Create access control management
- [ ] Document data privacy compliance
- [ ] Create security incident response
- [ ] Document vulnerability management

---

**Last Updated:** September 4, 2025  
**Changelog:** Initial runbook - comprehensive operational procedures established

