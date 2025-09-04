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