# Revenue Intelligence Inbox - Technical Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE LAYER                            │
│                         (Streamlit Frontend)                             │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐ │
│  │  Dashboard  │  │   Inbox     │  │  Routing    │  │Import/Export │ │
│  │    Page     │  │   Page      │  │   Page      │  │    Page      │ │
│  │             │  │             │  │             │  │              │ │
│  │ - KPIs      │  │ - Search    │  │ - Conflicts │  │ - Upload     │ │
│  │ - Charts    │  │ - Filters   │  │ - Override  │  │ - Preview    │ │
│  │ - Filters   │  │ - Details   │  │ - Audit Log │  │ - History    │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        APPLICATION SERVICES LAYER                        │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────┐  │
│  │ AnalyticsService │  │  RoutingEngine   │  │ ImportExportService│  │
│  │                  │  │                  │  │                    │  │
│  │ - calculate_kpis │  │ - assign_owner   │  │ - parse_csv       │  │
│  │ - get_timeseries │  │ - detect_conflict│  │ - parse_json      │  │
│  │ - apply_filters  │  │ - explain_routing│  │ - detect_duplicate│  │
│  │                  │  │ - log_assignment │  │ - protect_manual  │  │
│  │                  │  │                  │  │ - export_data     │  │
│  └──────────────────┘  └──────────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       DATA ACCESS LAYER (ORM)                            │
│                                                                          │
│  ┌───────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │  Account  │  │  SalesOwner  │  │ Conversation │  │ ImportLog   │  │
│  │  Model    │  │    Model     │  │    Model     │  │   Model     │  │
│  └───────────┘  └──────────────┘  └──────────────┘  └─────────────┘  │
│                                                                          │
│                        ┌──────────────┐                                 │
│                        │ RoutingLog   │                                 │
│                        │   Model      │                                 │
│                        └──────────────┘                                 │
│                                                                          │
│                      SQLAlchemy ORM + Alembic                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PERSISTENCE LAYER                                │
│                                                                          │
│  Development:                    Production:                             │
│  ┌─────────────────┐            ┌─────────────────────────────────┐   │
│  │ SQLite          │            │ PostgreSQL (Managed Service)    │   │
│  │ (revenue.db)    │            │ - AWS RDS                       │   │
│  │                 │            │ - Render PostgreSQL             │   │
│  └─────────────────┘            │ - Supabase                      │   │
│                                  └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. UI Layer Components

#### Dashboard Page (`pages/dashboard.py`)
**Responsibilities:**
- Display KPIs in metric cards
- Render interactive Plotly charts
- Handle date range filtering
- Refresh data on user interaction

**Key Functions:**
- `render_kpis(date_range)`: Display metrics
- `render_timeseries_chart(data)`: Conversations over time
- `render_distribution_charts(data)`: Type, owner, stage distributions

#### Inbox Page (`pages/inbox.py`)
**Responsibilities:**
- Display searchable conversation list
- Handle filtering and sorting
- Show conversation details
- Enable manual editing with tracking

**Key Functions:**
- `render_search_filters()`: Search bar + filter controls
- `render_conversation_list(conversations, page)`: Paginated list
- `render_conversation_detail(conv_id)`: Detail modal/expander
- `handle_manual_edit(conv_id, field, value)`: Update + track edit

#### Routing Page (`pages/routing.py`)
**Responsibilities:**
- Display routing conflicts
- Enable manual override
- Show routing audit log

**Key Functions:**
- `render_conflict_queue()`: Conversations needing review
- `handle_manual_assignment(conv_id, owner_id)`: Override routing
- `render_audit_log(filters)`: Historical routing decisions

#### Import/Export Page (`pages/import_export.py`)
**Responsibilities:**
- Handle file uploads
- Display import preview
- Manage import execution
- Generate and download exports

**Key Functions:**
- `handle_file_upload()`: Parse and validate CSV/JSON
- `render_import_preview(preview_data)`: Show counts before commit
- `execute_import(validated_data)`: Commit to database
- `generate_export(filters, format)`: Create export archive

### 2. Application Services

#### AnalyticsService (`services/analytics.py`)
**Purpose:** Calculate metrics and aggregate data for visualization

**Key Methods:**
```python
def calculate_kpis(date_range: tuple) -> dict:
    """Return: total_conversations, active_opportunities, 
       follow_ups_needed, avg_response_time, win_rate"""

def get_timeseries_data(date_range: tuple, group_by: str) -> pd.DataFrame:
    """Return conversations aggregated by day/week/month"""

def get_distribution_data(dimension: str, date_range: tuple) -> pd.DataFrame:
    """Return conversation counts by type, owner, or stage"""

def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply user-selected filters to dataset"""
```

#### RoutingEngine (`services/routing.py`)
**Purpose:** Assign conversations to sales owners using explainable rules

**Key Methods:**
```python
def assign_owner(conversation: Conversation) -> tuple[SalesOwner, str, bool]:
    """
    Returns: (assigned_owner, explanation, has_conflict)
    
    Rules (priority order):
    1. Skip if manually assigned
    2. Account ownership (historical)
    3. Territory match
    4. Workload balance
    5. Round robin
    """

def detect_conflicts(conversation: Conversation, rules_results: list) -> bool:
    """Check if multiple rules suggest different owners"""

def explain_routing(rule_applied: str, owner: SalesOwner, context: dict) -> str:
    """Generate human-readable routing explanation"""

def log_assignment(conversation: Conversation, previous_owner: SalesOwner, 
                   new_owner: SalesOwner, method: str, explanation: str):
    """Create audit trail entry"""
```

**Rule Implementation Details:**

```python
# Rule 1: Manual Override
if conversation.routing_method == 'manual':
    return (conversation.sales_owner, "Manually assigned", False)

# Rule 2: Account Ownership
previous_conversations = get_account_conversations(conversation.account_id)
if previous_conversations:
    owner = most_frequent_owner(previous_conversations)
    return (owner, f"Assigned to {owner.name} who owns this account 
            ({len(previous_conversations)} previous conversations)", False)

# Rule 3: Territory Match
territory_owners = get_owners_by_territory(conversation.account.territory)
if len(territory_owners) == 1:
    return (territory_owners[0], f"Assigned to {territory_owners[0].name} 
            based on territory: {conversation.account.territory}", False)
elif len(territory_owners) > 1:
    # Multiple matches - potential conflict, use workload balance
    owner = min(territory_owners, key=lambda o: get_workload(o))
    conflict = (max(get_workload(o) for o in territory_owners) - 
                min(get_workload(o) for o in territory_owners)) > 5
    return (owner, f"Assigned to {owner.name} (territory + workload balance)", conflict)

# Rule 4: Workload Balance
active_owners = get_active_owners()
owner = min(active_owners, key=lambda o: get_workload(o))
return (owner, f"Assigned to {owner.name} for workload balance 
        (currently {get_workload(owner)} active conversations)", False)

# Rule 5: Round Robin
owner = next_in_rotation()
return (owner, f"Assigned to {owner.name} via round-robin", False)
```

#### ImportExportService (`services/import_export.py`)
**Purpose:** Handle data import/export with validation and protection

**Key Methods:**
```python
def parse_csv(file_path: str) -> tuple[pd.DataFrame, list]:
    """Parse CSV and validate schema. Returns (data, errors)"""

def parse_json(file_path: str) -> tuple[pd.DataFrame, list]:
    """Parse JSON and validate schema. Returns (data, errors)"""

def detect_duplicates(import_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add columns: is_duplicate, existing_id, has_manual_edits
    Match on: customer_name, conversation_date, conversation_type
    """

def preview_import(import_df: pd.DataFrame) -> dict:
    """
    Return: {
        'new_count': int,
        'update_count': int,
        'skip_count': int,
        'protected_fields': list
    }
    """

def execute_import(import_df: pd.DataFrame) -> ImportLog:
    """
    Transaction:
    1. Begin transaction
    2. Insert/update records (respecting manual edits)
    3. Log import
    4. Commit or rollback on error
    """

def export_data(filters: dict, format: str) -> str:
    """
    Generate export file + manifest
    Return path to .zip archive
    """

def generate_manifest(filters: dict, record_count: int, format: str) -> dict:
    """Create export metadata"""
```

**Import Flow Diagram:**
```
Upload File
    │
    ▼
Parse & Validate Schema
    │
    ├─ Errors? ──> Display errors, halt
    │
    ▼
Detect Duplicates
    │
    ▼
Check Manual Edits on Duplicates
    │
    ▼
Generate Preview
(New: X, Update: Y, Skip: Z)
    │
    ▼
User Confirms? ─No─> Cancel
    │
    Yes
    ▼
Begin Transaction
    │
    ├─> Insert New Records
    │
    ├─> Update Non-Protected Fields on Duplicates
    │
    ├─> Create Import Log
    │
    ▼
Commit Transaction
    │
    ▼
Display Success + Link to Import History
```

### 3. Data Models (SQLAlchemy)

#### File Structure
```
src/
  models/
    __init__.py
    base.py          # Base model with common fields
    account.py       # Account model
    sales_owner.py   # SalesOwner model
    conversation.py  # Conversation model
    import_log.py    # ImportLog model
    routing_log.py   # RoutingLog model
```

#### Base Model (`models/base.py`)
```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

Base = declarative_base()

class TimestampMixin:
    """Common timestamp fields for all models"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)
```

#### Relationships
```
Account (1) ──< (many) Conversation
SalesOwner (1) ──< (many) Conversation
Conversation (1) ──< (many) RoutingLog
SalesOwner (1) ──< (many) RoutingLog
```

### 4. Database Schema

#### Indexes for Performance
```sql
-- Conversation table
CREATE INDEX idx_conversation_date ON conversation(conversation_date);
CREATE INDEX idx_conversation_owner ON conversation(sales_owner_id);
CREATE INDEX idx_conversation_account ON conversation(account_id);
CREATE INDEX idx_conversation_duplicate ON conversation(customer_name, conversation_date, conversation_type);

-- RoutingLog table
CREATE INDEX idx_routing_conversation ON routing_log(conversation_id);
CREATE INDEX idx_routing_timestamp ON routing_log(created_at);

-- ImportLog table
CREATE INDEX idx_import_timestamp ON import_log(import_timestamp);
```

## Data Flow Scenarios

### Scenario 1: New Import with Duplicates

```
1. User uploads customers_oct2026.csv (50 records)
2. ImportExportService.parse_csv() validates schema
3. ImportExportService.detect_duplicates() finds:
   - 30 new records
   - 15 existing (no manual edits) -> will update
   - 5 existing (with manual edits) -> will skip protected fields
4. Preview shown to user:
   "30 new, 15 to update, 5 partially protected"
5. User clicks "Import"
6. execute_import() begins transaction:
   - INSERT 30 new conversations
   - For 15 existing: UPDATE all fields
   - For 5 protected: UPDATE only non-manually-edited fields
   - RoutingEngine.assign_owner() runs for all new conversations
   - ImportLog created
7. Transaction commits
8. Success message: "Imported 45 records (30 new, 15 updated, 5 partial)"
```

### Scenario 2: Routing Conflict Resolution

```
1. New conversation imported: Acme Corp, no prior history
2. RoutingEngine.assign_owner() evaluates:
   - Rule 2 (Account): No history, skip
   - Rule 3 (Territory): 2 owners match "West" territory -> CONFLICT
     Candidates: Jane (10 conversations), Bob (12 conversations)
   - Workload balance suggests Jane
3. Conflict flagged: routing_method = NULL, requires_manual = True
4. Manager views Routing page conflict queue
5. Manager sees:
   "Suggested: Jane Smith (West territory, lower workload)
    Alternative: Bob Johnson (West territory)
    Reason: Multiple territory matches"
6. Manager clicks "Assign to Jane"
7. RoutingLog created:
   - routing_method = 'conflict_resolved'
   - explanation = "Manually resolved conflict: assigned to Jane Smith"
8. Conversation.routing_method = 'manual' (protected from auto-reassignment)
```

### Scenario 3: Export with Filters

```
1. User navigates to Import/Export page
2. User sets filters:
   - Date: Oct 1-15, 2026
   - Sales Owner: Jane Smith
   - Risk Level: Medium or High
3. User selects format: JSON
4. User clicks "Export"
5. ImportExportService.export_data():
   - Query conversations with filters applied (12 records)
   - Generate conversations.json with full nested structure
   - Generate manifest.json with metadata
   - Create revenue_export_20261023_103045.zip
6. Browser downloads .zip file
7. User can unzip and find:
   - conversations.json (12 records)
   - manifest.json (filter details, timestamp, schema version)
```

## Configuration Management

### Environment Variables

```bash
# Development (.env.local)
DATABASE_URL=sqlite:///revenue.db
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Production (.env.production)
DATABASE_URL=postgresql://user:pass@host:5432/revenue_db
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
SECRET_KEY=<generated>
```

### Configuration File (`src/config.py`)

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///revenue.db')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Import settings
    MAX_IMPORT_SIZE_MB = 10
    IMPORT_CHUNK_SIZE = 500
    
    # Routing settings
    WORKLOAD_IMBALANCE_THRESHOLD = 5
    WORKLOAD_WINDOW_DAYS = 30
    
    # Export settings
    EXPORT_TEMP_DIR = 'exports'
    
    @staticmethod
    def get_db_engine():
        from sqlalchemy import create_engine
        return create_engine(
            Config.DATABASE_URL,
            echo=Config.DEBUG
        )
```

## Security Implementation

### Input Validation

```python
# services/validators.py

from typing import List, Dict, Any
import pandas as pd

class ImportValidator:
    REQUIRED_FIELDS = [
        'customer_name', 'account_name', 'conversation_type', 
        'conversation_date'
    ]
    
    VALID_CONVERSATION_TYPES = ['call', 'meeting']
    VALID_RISK_LEVELS = ['none', 'low', 'medium', 'high']
    
    @staticmethod
    def validate_schema(df: pd.DataFrame) -> List[str]:
        errors = []
        
        # Check required fields
        missing = set(ImportValidator.REQUIRED_FIELDS) - set(df.columns)
        if missing:
            errors.append(f"Missing required fields: {', '.join(missing)}")
        
        # Validate data types
        if 'conversation_date' in df.columns:
            try:
                pd.to_datetime(df['conversation_date'])
            except:
                errors.append("Invalid date format in conversation_date")
        
        # Validate enums
        if 'conversation_type' in df.columns:
            invalid_types = set(df['conversation_type']) - set(ImportValidator.VALID_CONVERSATION_TYPES)
            if invalid_types:
                errors.append(f"Invalid conversation_type values: {invalid_types}")
        
        return errors
    
    @staticmethod
    def sanitize_input(value: str) -> str:
        """Remove potentially dangerous characters"""
        return value.strip().replace('\x00', '')
```

### SQL Injection Prevention

```python
# All queries use SQLAlchemy ORM - parameterized by default

# ✅ SAFE (ORM)
conversations = session.query(Conversation).filter(
    Conversation.customer_name == user_input
).all()

# ❌ DANGEROUS (Never do this)
# conversations = session.execute(
#     f"SELECT * FROM conversation WHERE customer_name = '{user_input}'"
# )
```

### File Upload Security

```python
# pages/import_export.py

import streamlit as st
from werkzeug.utils import secure_filename

def handle_file_upload():
    uploaded_file = st.file_uploader(
        "Upload CSV or JSON",
        type=['csv', 'json'],
        help="Maximum file size: 10MB"
    )
    
    if uploaded_file:
        # Check file size
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
            st.error("File size exceeds 10MB limit")
            return None
        
        # Sanitize filename
        safe_filename = secure_filename(uploaded_file.name)
        
        # Validate file type by content (not just extension)
        if uploaded_file.type not in ['text/csv', 'application/json']:
            st.error("Invalid file type")
            return None
        
        return uploaded_file
```

## Testing Strategy

### Test Structure
```
tests/
  unit/
    test_models.py
    test_routing_engine.py
    test_import_export.py
    test_analytics.py
  integration/
    test_import_workflow.py
    test_export_workflow.py
    test_routing_workflow.py
  fixtures/
    sample_data.py
    test_database.py
```

### Key Test Cases

#### Routing Engine Tests (`tests/unit/test_routing_engine.py`)
```python
def test_account_ownership_rule():
    """Assign to owner with most conversations on account"""
    
def test_territory_match_single():
    """Assign to sole owner in territory"""
    
def test_territory_match_multiple_with_conflict():
    """Detect conflict when multiple owners in territory"""
    
def test_workload_balance():
    """Assign to owner with fewest active conversations"""
    
def test_round_robin():
    """Rotate through owners alphabetically"""
    
def test_manual_override_protection():
    """Never auto-reassign manually assigned conversations"""
```

#### Import/Export Tests (`tests/unit/test_import_export.py`)
```python
def test_duplicate_detection():
    """Match on customer_name + date + type"""
    
def test_manual_edit_protection():
    """Skip updating manually edited fields on reimport"""
    
def test_import_rollback_on_error():
    """No partial data on validation failure"""
    
def test_export_manifest_generation():
    """Manifest includes all required metadata"""
```

## Performance Considerations

### Database Optimization
1. **Indexes** on frequently queried columns (conversation_date, sales_owner_id)
2. **Pagination** for large result sets (limit/offset)
3. **Eager loading** for relationships (joinedload to avoid N+1 queries)
4. **Connection pooling** for production PostgreSQL

### Streamlit Optimization
1. **Session state caching** for expensive queries
2. **@st.cache_data** decorator for analytics calculations
3. **Lazy loading** conversation details (load on demand)
4. **Chunked processing** for large imports (process 500 records at a time)

### Example Caching
```python
import streamlit as st

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_kpis(date_start, date_end):
    """Cached KPI calculation"""
    return analytics_service.calculate_kpis((date_start, date_end))
```

## Deployment Architecture

### Local Development
```
Developer Machine
  ├─ Python 3.10+
  ├─ SQLite (revenue.db)
  ├─ Streamlit Dev Server (port 8501)
  └─ Git repository
```

### Production (Render + PostgreSQL)
```
┌─────────────────────────────────────┐
│  Render Web Service                 │
│  ├─ Docker Container                │
│  │  ├─ Python 3.10                  │
│  │  ├─ Streamlit Server             │
│  │  └─ App Code                     │
│  └─ Environment Variables           │
│     └─ DATABASE_URL (PostgreSQL)    │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Render PostgreSQL                  │
│  ├─ Database: revenue_db            │
│  ├─ Automatic Backups               │
│  └─ Connection Pooling              │
└─────────────────────────────────────┘
```

### Deployment Steps (Render)
1. Push code to GitHub
2. Create Render PostgreSQL instance
3. Create Render Web Service from GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port=$PORT`
6. Set environment variable: `DATABASE_URL=<postgresql_url>`
7. Run initial migration: `alembic upgrade head`
8. Deploy

## Monitoring & Maintenance

### Logging Strategy
```python
# src/utils/logger.py

import logging
from config import Config

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Usage
logger = get_logger(__name__)
logger.info("Import started: %s", filename)
logger.error("Import failed: %s", str(e))
```

### Health Checks
- Database connectivity test on app startup
- Import history monitoring (failed imports alert)
- Disk space monitoring (SQLite file size)

### Backup Strategy
- **SQLite**: Daily file backup to cloud storage (S3, Google Drive)
- **PostgreSQL**: Automatic daily backups (Render managed)
- **Export**: Recommend users regularly export data as backup

---

## Appendix: Technology Choices Rationale

### Why Streamlit?
- Rapid prototyping for data apps
- Built-in components (file upload, charts, forms)
- Python-native (no JavaScript required)
- Easy deployment options
- Trade-off: Less flexible than React, but faster to build

### Why SQLAlchemy?
- Database abstraction (SQLite ↔ PostgreSQL portability)
- ORM prevents SQL injection
- Migration support via Alembic
- Well-documented and mature

### Why Pandas?
- Excellent CSV/JSON handling
- Data validation and transformation
- Integration with SQLAlchemy
- Familiar to data analysts

### Why PostgreSQL for Production?
- ACID compliance (critical for import transactions)
- Better concurrent access than SQLite
- Managed services available (RDS, Render, Supabase)
- Industry standard for production web apps

### Why NOT SQLite in Production?
- File locking issues with concurrent writes
- Ephemeral filesystems on many hosting platforms
- Not designed for high-concurrency web apps
- Risk of data loss on container restart (Streamlit Cloud, Heroku)

---

*This architecture document should be read alongside the main specification (.kiro/spec.md) for complete project understanding.*
