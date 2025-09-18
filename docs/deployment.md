# Clever AI - Deployment & Configuration Guide

## Changelog
- **2025-09-04**: Initial deployment documentation via static analysis
- **Author**: Documentation Audit Agent
- **Scope**: Production deployment, configuration management, and operational procedures

---

## System Requirements

### Minimum Hardware Requirements
- **CPU**: 2-core processor (ARM or x64)
- **Memory**: 2GB RAM (4GB recommended)
- **Storage**: 500MB available space
- **Graphics**: WebGL-capable GPU (integrated graphics acceptable)

### Software Dependencies
- **Python**: 3.8+ (tested with 3.12)
- **Node.js**: Not required (vanilla JavaScript)
- **Database**: SQLite (included with Python)
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+

### Platform Compatibility
- ✅ **Linux**: Primary development platform
- ✅ **macOS**: Full compatibility
- ✅ **Windows**: Compatible with WSL/native
- ✅ **Chromebook**: Target platform for UI performance

---

## Installation Procedures

### Quick Start (Development)
```bash
# Clone repository
git clone https://github.com/Jgallegos1991/projects.git
cd projects

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from database import db_manager; print('Database initialized')"

# Run development server
python app.py
```

### Production Installation
```bash
# System-level dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# Application setup
sudo useradd -m -s /bin/bash clever
sudo -u clever mkdir /home/clever/clever-ai
sudo -u clever git clone https://github.com/Jgallegos1991/projects.git /home/clever/clever-ai

# Virtual environment
sudo -u clever python3 -m venv /home/clever/clever-ai/venv
sudo -u clever /home/clever/clever-ai/venv/bin/pip install -r /home/clever/clever-ai/requirements.txt

# System service setup (see systemd section below)
```

---

## Configuration Management

### Environment Configuration

#### Development Environment
```python
# config.py - Development settings
OFFLINE_ONLY = True
SAFE_MODE = False  # Enable full NLP stack
DEBUG = True
DATABASE_NAME = "clever.db"
```

#### Production Environment  
```python
# config.py - Production overrides
OFFLINE_ONLY = True  # Always offline
SAFE_MODE = False
DEBUG = False
KEEP_LATEST_BACKUPS = 3  # More backups in production
```

### Environment Variables (Recommended)
```bash
# .env file support (future enhancement)
CLEVER_DB_PATH=/data/clever/clever.db
CLEVER_BACKUP_DIR=/data/clever/backups
CLEVER_UPLOAD_DIR=/data/clever/uploads
CLEVER_DEBUG=false
CLEVER_LOG_LEVEL=info
```

### Directory Structure
```
/home/clever/clever-ai/
├── app.py                 # Main application
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── clever.db      # SQLite database
├── backups/              # Automated backups
├── uploads/              # File ingestion
├── static/               # Frontend assets
│   ├── css/
│   ├── js/
│   └── vendor/
├── templates/            # Jinja2 templates
└── logs/                 # Application logs
```

---

## Database Configuration

### SQLite Setup
```python
# Automatic initialization on first run
class DatabaseManager:
    def __init__(self):
        self.db_path = config.DATABASE_NAME
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._ensure_tables()
```

### Database Schema Migration
```sql
-- Schema versioning table (future enhancement)
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Current schema version: 1.0
INSERT OR IGNORE INTO schema_version (version) VALUES (1);
```

### Backup Configuration
```python
# Automatic backup settings
KEEP_LATEST_BACKUPS = 3          # Production: more backups
BACKUP_ZIP_FORMAT = "backup_%Y-%m-%d_%H-%M-%S.zip"
BACKUP_DIR = os.path.join(PROJECT_PATH, "backups")
```

### Backup Automation
```bash
# Cron job for regular backups
0 6 * * * /home/clever/clever-ai/venv/bin/python /home/clever/clever-ai/backup_script.py
```

---

## Web Server Configuration

### Development Server
```python
# app.py - Built-in Flask development server
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
```

### Production Server (Gunicorn)
```bash
# Install Gunicorn
pip install gunicorn

# Production server configuration
gunicorn --bind 127.0.0.1:5000 --workers 2 --timeout 60 app:app
```

### Reverse Proxy (Nginx)
```nginx
# /etc/nginx/sites-available/clever-ai
server {
    listen 80;
    server_name localhost;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # Static file serving for performance
    location /static {
        alias /home/clever/clever-ai/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## System Service Configuration

### Systemd Service
```ini
# /etc/systemd/system/clever-ai.service
[Unit]
Description=Clever AI Assistant
After=network.target

[Service]
Type=simple
User=clever
Group=clever
WorkingDirectory=/home/clever/clever-ai
Environment=PATH=/home/clever/clever-ai/venv/bin
ExecStart=/home/clever/clever-ai/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 2 app:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Service Management
```bash
# Enable and start service
sudo systemctl enable clever-ai
sudo systemctl start clever-ai

# Check status
sudo systemctl status clever-ai

# View logs
sudo journalctl -u clever-ai -f
```

---

## Security Configuration

### File System Permissions
```bash
# Set appropriate ownership
sudo chown -R clever:clever /home/clever/clever-ai

# Secure permissions
chmod 750 /home/clever/clever-ai
chmod 644 /home/clever/clever-ai/*.py
chmod 600 /home/clever/clever-ai/clever.db
chmod 755 /home/clever/clever-ai/static
```

### Application Security
```python
# File upload restrictions
ALLOWED_EXTENSIONS = {'txt', 'md', 'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

# Secure filename handling
from werkzeug.utils import secure_filename
filename = secure_filename(file.filename)
```

### Network Security
- **Localhost Binding**: Default configuration binds to 127.0.0.1 only
- **No External APIs**: Offline-only operation prevents data leakage
- **HTTPS**: Recommended for production with SSL certificates

---

## Performance Configuration

### Python Optimization
```python
# Production optimizations
import sys
if not sys.flags.debug:
    # Disable debug features
    import logging
    logging.getLogger().setLevel(logging.WARNING)
```

### Database Optimization
```sql
-- SQLite performance tuning
PRAGMA journal_mode=WAL;        -- Write-ahead logging
PRAGMA synchronous=NORMAL;      -- Performance vs safety balance
PRAGMA cache_size=10000;        -- 10MB cache
PRAGMA temp_store=memory;       -- Use RAM for temp tables
```

### Static Asset Optimization
```nginx
# Nginx compression and caching
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
}
```

---

## Monitoring & Logging

### Application Logging
```python
# Structured logging configuration
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/clever/clever-ai/logs/app.log'),
        logging.StreamHandler()  # Also output to console
    ]
)
```

### Performance Monitoring
```javascript
// Frontend performance tracking
const performanceMonitor = {
    fps: 0,
    memory: performance.memory ? performance.memory.usedJSHeapSize : 0,
    particles: activeCount
};

// Log performance metrics
console.log('Performance:', JSON.stringify(performanceMonitor));
```

### Health Check Endpoints
```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'database': 'connected' if db_manager.conn else 'disconnected',
        'timestamp': datetime.utcnow().isoformat()
    }
```

---

## Backup & Recovery

### Automated Backup Strategy
```python
# Enhanced backup manager
class ProductionBackupManager(BackupManager):
    def __init__(self):
        super().__init__(keep_latest=7)  # Week of backups
        self.remote_backup_enabled = False  # Local only
    
    def create_incremental_backup(self):
        # Future: Implement incremental backups
        pass
```

### Recovery Procedures
```bash
# Database recovery from backup
cd /home/clever/clever-ai/backups
unzip backup_2025-09-04_06-00-00.zip
cp clever.db ../clever.db.restore

# Service restart after recovery
sudo systemctl restart clever-ai
```

### Data Integrity Checks
```sql
-- SQLite integrity verification
PRAGMA integrity_check;
PRAGMA foreign_key_check;
```

---

## Troubleshooting Guide

### Common Issues

#### 1. Database Connection Errors
```bash
# Check database file permissions
ls -la clever.db

# Test database connectivity
sqlite3 clever.db ".tables"
```

#### 2. NLP Model Loading Failures
```bash
# Re-download spaCy model
python -m spacy download en_core_web_sm

# Verify NLTK data
python -c "import nltk; nltk.download('vader_lexicon')"
```

#### 3. WebGL/3D Rendering Issues
```javascript
// Check WebGL support
console.log('WebGL supported:', !!window.WebGLRenderingContext);

// Fallback to 2D mode
document.body.classList.add('no-3d');
```

### Log Analysis
```bash
# Application logs
tail -f /home/clever/clever-ai/logs/app.log

# System service logs
sudo journalctl -u clever-ai --since "1 hour ago"

# Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

---

## Development vs Production Checklist

### Development Setup ✅
- [x] Requirements installed
- [x] Database initialized  
- [x] Safe mode disabled
- [x] Debug logging enabled

### Production Readiness 🔄
- [ ] System user created
- [ ] Service configuration installed
- [ ] Nginx proxy configured
- [ ] SSL certificates installed
- [ ] Automated backups scheduled
- [ ] Log rotation configured
- [ ] Performance monitoring enabled
- [ ] Health checks implemented

### Security Hardening 🔄
- [ ] File permissions secured
- [ ] Database access restricted
- [ ] Upload validation enhanced
- [ ] Error messages sanitized
- [ ] Security headers added

---

This deployment guide provides the foundation for running Clever AI in both development and production environments, with emphasis on the offline-first nature and security requirements of the system.