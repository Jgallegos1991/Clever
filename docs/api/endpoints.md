copilot/fix-645d4672-a183-4fe7-a0a8-c6ff0d030ac5
# API Endpoints

## Flask Route Documentation

### Core Application Routes

#### `GET /`
**Purpose:** Serve main application interface  
**Template:** `index.html`  
**Authentication:** None  
**Response:** HTML page with full Clever interface

#### `GET /capabilities`
**Purpose:** System information and feature discovery  
**Response Format:** JSON  
**Authentication:** None

```json
{
    "name": "Clever",
    "role": "AI co-pilot and strategic thinking partner", 
    "mission": "Blend high-level intelligence with authentic, human-like interaction",
    "operational_attributes": [
        "Witty Intelligence",
        "Intuitive Anticipation", 
        "Adaptive Genius",
        "Empathetic Collaboration",
        "Proactive Problem-Solving",
        "Comprehensive Contextual Memory"
    ],
    "features": [
        "Offline operation",
        "Animated starfield and 3D grid UI",
        "Particle cloud centerpiece",
        "File ingestion and contextual analysis"
    ],
    "ui_style": {
        "theme": "Dark, high-contrast space",
        "fonts": "Modern, crisp sans-serif",
        "structure": "Minimalist, clean, advanced but welcoming"
    }
}
```

### Chat & Interaction Routes

#### `POST /chat`
**Purpose:** Process user messages and generate AI responses  
**Content-Type:** `application/json`  
**Authentication:** None

**Request Body:**
```json
{
    "message": "User input text",
    "context": "Optional conversation context",
    "mode": "deep_dive|quick_hit|creative|support"
}
```

**Response:**
```json
{
    "response": "Clever's generated response",
    "analysis": {
        "intent": "detected_intent",
        "entities": ["extracted", "entities"],
        "sentiment": "positive|negative|neutral",
        "confidence": 0.95
    },
    "context_updated": true,
    "timestamp": "2025-09-04T08:41:52Z"
}
```

#### `GET /conversation-history`
**Purpose:** Retrieve conversation history  
**Parameters:** 
- `limit` (optional): Number of messages to return
- `offset` (optional): Pagination offset

**Response:**
```json
{
    "conversations": [
        {
            "id": 1,
            "user_message": "Hello Clever",
            "ai_response": "Hey there! Ready to collaborate?",
            "timestamp": "2025-09-04T08:30:00Z",
            "analysis_data": {}
        }
    ],
    "total_count": 150,
    "has_more": true
}
```

### File Processing Routes

#### `POST /upload`
**Purpose:** Handle file uploads for document processing  
**Content-Type:** `multipart/form-data`  
**Max File Size:** Configured in `config.py`

**Form Parameters:**
- `file`: File to upload
- `process_immediately`: Boolean flag for immediate processing

**Allowed Extensions:** `.txt`, `.md`, `.pdf`

**Response:**
```json
{
    "success": true,
    "filename": "document.pdf",
    "file_id": "uuid-string",
    "processing_status": "queued|processing|completed|error",
    "message": "File uploaded successfully"
}
```

#### `GET /file-status/<file_id>`
**Purpose:** Check file processing status  
**Response:**
```json
{
    "file_id": "uuid-string",
    "filename": "document.pdf",
    "status": "queued|processing|completed|error",
    "progress": 75,
    "extracted_content": "Text content when complete",
    "analysis": "NLP analysis results when complete",
    "error_message": "Error details if status is error"
}
```

### Analysis & Context Routes

#### `POST /analyze-text`
**Purpose:** Perform NLP analysis on provided text  
**Content-Type:** `application/json`

**Request Body:**
```json
{
    "text": "Text to analyze",
    "include_entities": true,
    "include_sentiment": true,
    "include_summary": false
}
```

**Response:**
```json
{
    "analysis": {
        "entities": [
            {
                "text": "Jordan",
                "label": "PERSON",
                "confidence": 0.99
            }
        ],
        "sentiment": {
            "polarity": 0.8,
            "subjectivity": 0.6,
            "label": "positive"
        },
        "key_phrases": ["strategic thinking", "collaboration"],
        "summary": "Optional text summary",
        "tokens": 25,
        "processing_time_ms": 150
    }
}
```

#### `GET /context`
**Purpose:** Retrieve current conversation context  
**Response:**
```json
{
    "active_topics": ["project planning", "AI development"],
    "user_preferences": {
        "communication_style": "casual",
        "preferred_mode": "quick_hit",
        "technical_level": "advanced"
    },
    "recent_files": ["document1.pdf", "notes.md"],
    "session_duration": 3600,
    "message_count": 45
}
```

### System Management Routes

#### `GET /health`
**Purpose:** System health check  
**Response:**
```json
{
    "status": "healthy|degraded|unhealthy",
    "database": {
        "connected": true,
        "response_time_ms": 5
    },
    "nlp": {
        "model_loaded": true,
        "model_version": "en_core_web_sm-3.8.0"
    },
    "storage": {
        "disk_space_mb": 1024,
        "backup_status": "current"
    },
    "uptime_seconds": 86400
}
```

#### `POST /backup`
**Purpose:** Trigger manual database backup  
**Authentication:** Admin (if implemented)  
**Response:**
```json
{
    "backup_created": true,
    "backup_filename": "backup_2025-09-04_08-41-52.zip",
    "backup_size_mb": 2.5,
    "timestamp": "2025-09-04T08:41:52Z"
}
```

### Error Handling

#### Standard Error Response Format
```json
{
    "error": true,
    "error_code": "INVALID_INPUT|SERVER_ERROR|NOT_FOUND",
    "message": "Human-readable error description",
    "details": "Technical error details for debugging",
    "timestamp": "2025-09-04T08:41:52Z"
}
```

#### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found
- `413`: Payload Too Large (file upload)
- `429`: Too Many Requests (rate limiting)
- `500`: Internal Server Error

## TODO Items

### API Documentation
- [ ] Generate OpenAPI/Swagger documentation
- [ ] Create API client libraries for common languages
- [ ] Document rate limiting and throttling policies
- [ ] Create API versioning strategy and documentation
- [ ] Document webhook support for real-time updates

### Security & Authentication
- [ ] Implement API key authentication for sensitive endpoints
- [ ] Document CORS policies and configuration
- [ ] Create request validation and sanitization documentation
- [ ] Implement request logging and audit trails
- [ ] Document API security best practices

### Performance & Monitoring
- [ ] Document response time benchmarks for each endpoint
- [ ] Create API performance monitoring and alerting
- [ ] Document caching strategies for expensive operations
- [ ] Implement request/response compression
- [ ] Create load testing procedures for API endpoints

### Integration & Testing
- [ ] Create comprehensive API test suite
- [ ] Document integration testing procedures
- [ ] Create API mocking utilities for development
- [ ] Document error scenario testing
- [ ] Create automated API documentation validation

### Advanced Features
- [ ] Implement Server-Sent Events for real-time updates
- [ ] Create batch processing endpoints for bulk operations
- [ ] Document file streaming for large uploads
- [ ] Implement GraphQL endpoint for flexible queries
- [ ] Create webhook system for external integrations

---

**Last Updated:** September 4, 2025  
**Changelog:** Initial API documentation - comprehensive endpoint specification
=======
# Clever AI - API Endpoints Documentation

**Generated:** 2025-09-04  
**Source:** app.py  
**Framework:** Flask 3.1.1  
**Database:** SQLite (offline_ai_data.db)  

## Changelog
- 2025-09-04: Initial API audit - extracted all Flask routes from app.py

## Overview

Clever is an offline-first Flask application serving as Jordan's AI co-pilot. The API provides endpoints for conversational AI, file ingestion, health monitoring, and UI components. All endpoints maintain offline operation with no cloud dependencies.

## Summary Table

| Path | Methods | Authentication | Purpose | Side Effects |
|------|---------|---------------|---------|--------------|
| `/` | GET | None | Main UI/Homepage | None |
| `/capabilities` | GET | None | System capabilities info | None |
| `/health` | GET | None | System health check | None |
| `/favicon.ico` | GET | None | Favicon serving | None |
| `/sw.js` | GET | None | Service worker serving | None |
| `/chat` | POST | None | AI conversation endpoint | DB write (conversations) |
| `/ingest` | POST | None | File upload/processing | File write, DB write (knowledge) |
| `/generator_page` | GET | None | Output generator UI | None |
| `/projects_page` | GET | None | Projects management UI | None |

## Detailed Endpoints

### GET `/`
**Purpose:** Serve the main Synaptic Hub interface  
**Blueprint:** None (main app)  
**Authentication:** None  
**Parameters:** None  
**Response Schema:**
```
Content-Type: text/html
Status: 200
Body: Rendered index.html template
```
**Status Codes:** 200  
**Side Effects:** None  
**Templates:** `templates/index.html`  
**Static Files:** Referenced via template (CSS, JS, manifests)  

### GET `/capabilities`
**Purpose:** Return system capabilities and configuration  
**Blueprint:** None (main app)  
**Authentication:** None  
**Parameters:** None  
**Response Schema:**
```json
{
  "name": "string",
  "role": "string", 
  "mission": "string",
  "operational_attributes": ["string"],
  "features": ["string"],
  "ui_style": {
    "theme": "string",
    "fonts": "string", 
    "structure": "string"
  }
}
```
**Status Codes:** 200  
**Side Effects:** None  
**Templates:** None  
**Static Files:** None  

### GET `/health`
**Purpose:** System health and status monitoring  
**Blueprint:** None (main app)  
**Authentication:** None  
**Parameters:** None  
**Response Schema:**
```json
{
  "status": "ok",
  "db": "up|down",    // Only if not SAFE_MODE
  "nlp": "loaded|missing"  // Only if not SAFE_MODE
}
```
**Status Codes:** 200  
**Side Effects:** None  
**Templates:** None  
**Static Files:** None  

### GET `/favicon.ico`
**Purpose:** Serve application favicon  
**Blueprint:** None (main app)  
**Authentication:** None  
**Parameters:** None  
**Response Schema:**
```
Content-Type: image/svg+xml
Status: 200
Body: SVG favicon file
```
**Status Codes:** 200, 404  
**Side Effects:** None  
**Templates:** None  
**Static Files:** `static/img/favicon.svg`  

### GET `/sw.js`
**Purpose:** Serve Progressive Web App service worker  
**Blueprint:** None (main app)  
**Authentication:** None  
**Parameters:** None  
**Response Schema:**
```
Content-Type: application/javascript
Status: 200
Body: Service worker JavaScript
```
**Status Codes:** 200, 404  
**Side Effects:** None  
**Templates:** None  
**Static Files:** `static/js/sw.js`  

### POST `/chat`
**Purpose:** Process conversational AI requests  
**Blueprint:** None (main app)  
**Authentication:** None  
**Request Parameters:**
- **Body (JSON):**
  ```json
  {
    "message": "string" // Required: User input message
  }
  ```
**Response Schema:**
```json
{
  "reply": "string",
  "analysis": {
    "user_input": "string",
    "active_mode": "safe|full",
    "detected_intent": "string",
    "user_mood": "string|null",
    "key_topics": ["string"],
    "entities": [{}],
    "full_nlp_analysis": {},
    "activePersona": "string",
    "responseTime": "number"
  }
}
```
**Error Response:**
```json
{
  "ok": false,
  "error": "string"
}
```
**Status Codes:** 200, 400, 500  
**Side Effects:** 
- Database write: `db_manager.add_conversation(msg, reply)` (if not SAFE_MODE)
- File append: `conversations.json` (if SAFE_MODE)  
**Templates:** None  
**Static Files:** None  

### POST `/ingest`
**Purpose:** Upload and process files for knowledge ingestion  
**Blueprint:** None (main app)  
**Authentication:** None  
**Request Parameters:**
- **Body (multipart/form-data):**
  - `file`: File upload (required)
**Response Schema:**
```json
{
  "message": "File uploaded and ingested successfully.",
  "filename": "string"
}
```
**Error Response:**
```json
{
  "ok": false,
  "error": "string"
}
```
**Status Codes:** 200, 400, 500  
**Side Effects:**
- File write: Saves uploaded file to upload directory
- Database write: `db_manager.add_source(filename, path, content)` (if not SAFE_MODE)  
**Templates:** None  
**Static Files:** None  

### GET `/generator_page`
**Purpose:** Output generator interface page  
**Blueprint:** None (main app)  
**Authentication:** None  
**Parameters:** None  
**Response Schema:**
```
Content-Type: text/html
Status: 200
Body: Rendered template or fallback HTML
```
**Status Codes:** 200  
**Side Effects:** None  
**Templates:** `templates/generate_output.html` (optional), fallback to template string  
**Static Files:** Referenced via template  

### GET `/projects_page`
**Purpose:** Active projects management interface  
**Blueprint:** None (main app)  
**Authentication:** None  
**Parameters:** None  
**Response Schema:**
```
Content-Type: text/html
Status: 200
Body: Rendered template or fallback HTML  
```
**Status Codes:** 200  
**Side Effects:** None  
**Templates:** `templates/projects.html` (optional), fallback to template string  
**Static Files:** Referenced via template  

## Global Request/Response Handling

### After Request Hook
The application includes a global `@app.after_request` decorator that adds security headers:
- `X-Content-Type-Options: nosniff`

### Configuration
- **Upload Folder:** Configurable via `config.UPLOAD_FOLDER` or defaults to `uploads/`  
- **Safe Mode:** Controlled by `SAFE_MODE` boolean flag
  - `True`: Limited functionality for development/testing
  - `False`: Full NLP and database integration

### Dependencies
- **Database:** SQLite via `database.py` (DatabaseManager)
- **NLP Processing:** spaCy, NLTK, TextBlob via `nlp_processor.py`
- **AI Persona:** Custom personality system via `persona.py`
- **File Security:** Uses `werkzeug.utils.secure_filename()` for uploads

### Error Handling
All endpoints include comprehensive exception handling with graceful fallbacks to maintain system stability and offline operation requirements.
jay-import
