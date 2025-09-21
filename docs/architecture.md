# Clever - Digital Brain Extension & Cognitive Partnership Architecture

## Changelog
- **2025-09-21**: Updated to reflect Clever's true vision as digital brain extension
- **2025-09-04**: Initial architecture documentation via static analysis
- **Author**: Documentation Audit Agent
- **Purpose**: Document cognitive partnership system architecture and components

---

## System Overview

**Clever** is Jay's **digital brain extension** and **cognitive partnership system** - a street-smart genius who talks like your best friend but casually solves Einstein-level physics problems. Built with Flask, SQLite, and spaCy, featuring advanced holographic particle UI for immersive cognitive enhancement.

### Core Philosophy
- **Digital Sovereignty**: Complete local control, total privacy, zero external dependencies
- **Cognitive Partnership**: Authentic relationship building and life companionship
- **Genius Friend Experience**: Street-smart casual talk with hidden Einstein intellect
- **Single-User Design**: Built exclusively for Jay's cognitive enhancement needs
- **Continuous Growth**: Learns and evolves as the perfect digital other half

---

## Architecture Layers

```
┌─────────────────────────────────────────────┐
│              Frontend Layer                  │
│  ┌─────────────────┐  ┌─────────────────────┐│
│  │  3D UI Engine   │  │   User Interface    ││
│  │ (Three.js/WebGL)│  │ (HTML/CSS/Vanilla)  ││
│  └─────────────────┘  └─────────────────────┘│
└─────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────┐
│              Flask Application               │
│  ┌─────────────────┐  ┌─────────────────────┐│
│  │ API Endpoints   │  │  Template Engine    ││
│  │   (REST API)    │  │     (Jinja2)        ││
│  └─────────────────┘  └─────────────────────┘│
└─────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────┐
│           Business Logic Layer               │
│  ┌─────────┐ ┌──────────┐ ┌─────────────────┐│
│  │Persona  │ │NLP Proc. │ │  Core Logic     ││
│  │Engine   │ │(spaCy)   │ │  (Commands)     ││
│  └─────────┘ └──────────┘ └─────────────────┘│
└─────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────┐
│           Data Management Layer              │
│  ┌─────────────────┐  ┌─────────────────────┐│
│  │    Database     │  │   File System       ││
│  │   (SQLite)      │  │ (Backups/Uploads)   ││
│  └─────────────────┘  └─────────────────────┘│
└─────────────────────────────────────────────┘
```

---

## Component Details

### Frontend Layer

#### 3D UI Engine (`static/js/orb_engine.js`)
**Purpose**: Magical particle-based interface  
**Technology**: Three.js, WebGL  
**Key Features**:
- 8000+ particle swarm system
- Morphing shapes (sphere, cube, torus)
- Real-time grid ripple effects
- Performance governor (adaptive quality)
- CSS3D panel integration

**Performance Characteristics**:
```javascript
const PARTICLE_COUNT = 8000;
let activeCount = PARTICLE_COUNT; // Dynamic for performance
const perf = { target: 45, minCount: 3500, step: 500 };
```

#### User Interface (`static/js/ui.js`, `static/js/main.js`)
**Purpose**: User interaction handling  
**Key Features**:
- Command parsing for 3D effects
- Voice input integration (planned)
- File upload interface
- Responsive design patterns

### Application Layer

#### Flask App (`app.py`)
**Purpose**: HTTP server and routing  
**Key Routes**:
- `/` - Main interface
- `/capabilities` - System metadata API
- `/chat` - NLP interaction endpoint
- `/generator_page`, `/projects_page` - Feature pages

**Safe Mode**: Development mode that disables NLP stack for faster iteration

#### Configuration (`config.py`)
**Purpose**: Centralized settings management  
**Key Settings**:
```python
PROJECT_PATH = BASE_DIR
DB_PATH = os.path.join(PROJECT_PATH, "clever.db")
OFFLINE_ONLY = True
ALLOW_REMOTE_SYNC = False
```

### Business Logic Layer

#### NLP Processor (`nlp_processor.py`)
**Purpose**: Natural language understanding  
**Technologies**: spaCy, NLTK, TextBlob  
**Capabilities**:
- Sentiment analysis (VADER)
- Named entity recognition
- Intent detection
- Keyword extraction
- Language statistics

**Models Used**:
- `en_core_web_sm` (spaCy)
- VADER sentiment lexicon
- NLTK corpora (punkt, stopwords)

#### Persona Engine (`persona.py`)
**Purpose**: AI personality and response generation  
**Key Features**:
- Mood-based responses
- User adaptation (learns expressions like "cash ma breff")
- Multiple personality traits (Witty, Empathetic, etc.)
- Context-aware communication

#### Core Logic (`core_nlp_logic.py`)
**Purpose**: Command detection and processing  
**Capabilities**:
- Intent classification
- Command extraction
- Knowledge management
- Response orchestration

### Data Management Layer

#### Database Manager (`database.py`)
**Purpose**: SQLite database operations  
**Architecture**: Singleton pattern with thread safety  
**Schema**:
```sql
sources (id, filename, filepath, content, uploaded_at)
knowledge (id, fact_key, fact_value, created_at)  
conversations (id, user_message, ai_response, timestamp)
system_state (key, value)
```

#### File Management
- **File Ingestor** (`file_ingestor.py`): Document processing and storage
- **Backup Manager** (`backup_manager.py`): Automated backup system
- **Upload Handling**: Secure file upload processing

---

## Data Flow Patterns

### User Interaction Flow
```
User Input → UI Layer → Flask Route → NLP Processing → 
Persona Engine → Database → Response Generation → UI Update
```

### File Ingestion Flow
```
File Upload → Validation → Content Extraction → 
NLP Analysis → Database Storage → Knowledge Integration
```

### 3D Interaction Flow  
```
User Command → Command Parser → 3D Engine → 
Particle System Update → Visual Feedback
```

---

## Database Schema

### Primary Tables

#### `conversations`
Stores all user interactions for context building
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### `knowledge`  
Key-value store for learned facts
```sql
CREATE TABLE knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fact_key TEXT NOT NULL UNIQUE,
    fact_value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### `sources`
Tracks ingested documents
```sql
CREATE TABLE sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL UNIQUE,
    content TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Data Relationships
- Conversations link to knowledge through fact extraction
- Sources provide context for knowledge creation
- System state tracks configuration and user preferences

---

## Security Model

### Local-First Design
- **No Network Calls**: Prevents data leakage
- **SQLite Security**: File-based permissions
- **Input Sanitization**: Limited but present

### File Handling
- **Extension Filtering**: `.txt`, `.md`, `.pdf` only
- **Path Sanitization**: Prevents directory traversal
- **Content Validation**: Basic file type checking

### Potential Vulnerabilities
1. **File Upload**: Insufficient content validation
2. **SQL Injection**: Mitigated by parameterized queries
3. **XSS**: Potential in dynamic content generation

---

## Performance Characteristics

### Bottlenecks Identified
1. **Particle Rendering**: 8000+ particles on main thread
2. **NLP Model Loading**: ~2-3 second startup time
3. **File Ingestion**: Synchronous processing

### Optimization Strategies
1. **Adaptive Quality**: FPS-based particle count reduction
2. **Lazy Loading**: Defer NLP model loading
3. **Background Processing**: Web Workers for 3D calculations

### Memory Usage
- **spaCy Model**: ~50MB loaded in memory
- **Three.js Objects**: Variable based on particle count
- **SQLite**: Minimal memory footprint

---

## Extension Points

### Plugin Architecture Potential
Current modular design supports future extensions:

1. **NLP Modules**: Additional language processing capabilities
2. **UI Components**: New 3D effects and interactions  
3. **Data Sources**: External tool integrations
4. **Export Formats**: Various output generators

### API Extensibility
Flask routing enables easy API expansion:
- RESTful endpoints for all major functions
- JSON-based communication
- Modular response handling

---

## Development Patterns

### Code Organization
- **Single Responsibility**: Each module has clear purpose
- **Dependency Injection**: Shared instances pattern
- **Error Boundaries**: Try-catch with graceful degradation

### State Management
- **Database State**: Persistent storage in SQLite
- **Application State**: Flask session management
- **UI State**: JavaScript global objects with namespacing

### Configuration Management
- **Environment-based**: Development vs production settings
- **Path Resolution**: Dynamic path construction
- **Feature Flags**: Safe mode and capability toggles

---

This architecture documentation provides the foundation for understanding system interactions, identifying improvement opportunities, and planning future enhancements.