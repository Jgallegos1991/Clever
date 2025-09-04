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