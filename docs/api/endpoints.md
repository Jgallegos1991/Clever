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