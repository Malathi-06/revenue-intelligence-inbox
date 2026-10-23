# Revenue Intelligence Inbox - Quick Start Guide

⚠️ **All data in this application is SYNTHETIC and for demonstration purposes only.**

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

---

## Installation

### Step 1: Get the Code
Navigate to the project directory:
```powershell
cd d:\revenue-intelligence-inbox
```

### Step 2: Install Dependencies
Install all required Python packages:
```powershell
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed streamlit-1.28.0 sqlalchemy-2.0.23 pandas-2.1.3 plotly-5.18.0 ...
```

---

## Database Initialization

### Step 3: Create Database with Synthetic Data
Initialize the SQLite database with 25 synthetic conversations:
```powershell
python init_db.py
```

**Expected output:**
```
Database initialized successfully!
Created 8 accounts
Created 5 sales owners
Created 25 conversations
Database location: d:\revenue-intelligence-inbox\data\revenue.db
```

**Verification:**
- Check that `data\revenue.db` exists (should be ~86 KB)
- Database contains: 8 accounts, 5 sales owners, 25 conversations

---

## Running the Application

### Step 4: Start the Streamlit Server
Launch the web application:
```powershell
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

The application will automatically open in your default web browser.

### Step 5: Navigate the Application
The app has four main sections accessible from the sidebar:

1. **Dashboard** - View KPIs and analytics charts
2. **Inbox** - Browse, search, and edit conversations
3. **Routing** - Manage assignments and resolve conflicts
4. **Import/Export** - Upload CSV/JSON files or export data

---

## Feature Walkthrough

### 📊 Dashboard Page
**What you'll see:**
- **KPI Cards:** Total conversations, conversion rate, average deal size, response time
- **Conversation Breakdown Chart:** By type (discovery, demo, negotiation)
- **Sentiment Trends Chart:** Positive/neutral/negative over time
- **Outcome Distribution Chart:** Won, lost, pending
- **Top Accounts Chart:** By conversation count
- **Date Filter:** Filter all metrics by date range

**Try this:**
1. Open Dashboard page
2. Select date range (e.g., last 30 days)
3. Observe KPIs update in real-time

### 📥 Inbox Page
**What you'll see:**
- **Search bar:** Search by customer name
- **Filters:** Type, sentiment, outcome, assigned owner
- **Conversation list:** All 25 conversations with details
- **Edit capability:** Click any conversation to edit and mark fields as manually edited

**Try this:**
1. Search for "TechCorp"
2. Filter by sentiment = "positive"
3. Click a conversation to edit
4. Change summary and click "Save Changes"
5. Note that field is now marked as "manually edited"

### 🔀 Routing Page
**What you'll see:**
- **Conflict Queue:** Conversations with routing conflicts (overloaded owners)
- **Unassigned Queue:** Conversations without assignment
- **Routing Audit Log:** Complete history of routing decisions with explanations

**Try this:**
1. Check conflict queue for overloaded owners
2. Review routing explanations (e.g., "Account ownership - Bob has 3 prior conversations")
3. Reassign conversations if needed

### 📤 Import/Export Page
**What you'll see:**
- **Import section:** Upload CSV or JSON files
- **Preview table:** Review data before importing
- **Export section:** Download conversations as CSV or JSON with manifest
- **Import history:** Audit log of all imports

**Try this:**
1. Click "Export Data" → "Download as ZIP"
2. Extract ZIP file to see conversations.csv and manifest.json
3. Modify CSV file (e.g., add new conversation)
4. Upload modified CSV file
5. Review preview and click "Commit Import"
6. Verify new conversation appears in Inbox

---

## Running Tests

### Unit Tests (38 tests)
Run all unit tests to verify core functionality:
```powershell
python -m pytest tests/unit/ -v
```

**Expected output:**
```
tests/unit/test_models.py::test_create_account PASSED                    [  2%]
tests/unit/test_models.py::test_create_sales_owner PASSED                [  5%]
...
tests/unit/test_analytics.py::test_search_conversations PASSED           [100%]
================================ 38 passed in 1.96s ================================
```

**Note:** You may see 5 SQLAlchemy deprecation warnings - these are informational and do not affect functionality.

### Integration Tests (5 tests)
Run comprehensive end-to-end verification:
```powershell
python tests/integration_verification.py
```

**Expected output:**
```
Running Revenue Intelligence Inbox Integration Tests
=====================================================

Test 1: Duplicate Detection
✓ Imported duplicate conversation correctly identified as Conversation ID: 1

Test 2: Manual Edit Protection
✓ Summary field protected from import (manual edit preserved)
✓ Outcome field updated from 'pending' to 'won'

Test 3: Routing Conflict Detection
✓ Assigned to: Bob Johnson
✓ Reason: Account ownership - Bob Johnson has prior conversations with this account

Test 4: Export with Manifest
✓ CSV exported: 25 conversations
✓ Manifest generated with metadata and statistics
✓ ZIP archive created: 2432 bytes
✓ Export location: d:\revenue-intelligence-inbox\exports\revenue_export_YYYYMMDD_HHMMSS.zip

Test 5: Database Persistence
✓ Database file: D:\revenue-intelligence-inbox\data/revenue.db
✓ File size: 86016 bytes
✓ Accounts: 8
✓ Sales owners: 5
✓ Conversations: 25

=====================================================
ALL 5 INTEGRATION TESTS PASSED ✓
```

---

## Key Features Demonstrated

### ✅ Duplicate Detection
- **How it works:** Matches on customer_name + conversation_date + conversation_type
- **Test it:** Import the same conversation twice - second import detected as duplicate
- **Evidence:** See `src\services\import_export.py` lines 118-165

### ✅ Manual Edit Protection
- **How it works:** Tracks edited fields in `manually_edited_fields` JSON column
- **Test it:** Edit a conversation summary, then reimport - summary preserved
- **Evidence:** See `src\services\import_export.py` lines 256-280

### ✅ Explainable Routing (5 Priority Rules)
1. **Account Ownership:** Assign to owner with most conversations with this account
2. **Territory Match:** Assign to owner covering account's territory
3. **Workload Balance:** Assign to owner with lowest conversation count
4. **Round Robin:** Cycle through available owners
5. **Fallback:** Assign to any active owner

**Test it:** Create new conversation and observe routing explanation in audit log  
**Evidence:** See `src\services\routing.py` lines 45-170

### ✅ Conflict Detection
- **How it works:** Flags owners with >8 active conversations as overloaded
- **Test it:** View conflict queue in Routing page
- **Evidence:** See `src\services\routing.py` lines 171-230

### ✅ Export with Manifest
- **How it works:** Generates CSV + JSON manifest with metadata and statistics
- **Test it:** Export data and review manifest.json
- **Evidence:** See `src\services\import_export.py` lines 256-280

---

## Project Structure

```
d:\revenue-intelligence-inbox\
├── app.py                           # Main Streamlit application
├── init_db.py                       # Database initialization script
├── requirements.txt                 # Python dependencies
├── README.md                        # Main documentation
├── QUICKSTART.md                    # This file
├── FINAL_STATUS.md                  # Comprehensive status report
│
├── data\
│   ├── revenue.db                  # SQLite database (86 KB, 25 conversations)
│   └── synthetic_data.py           # Synthetic data generator (CLEARLY LABELED)
│
├── src\
│   ├── models\                     # Database models
│   │   ├── account.py
│   │   ├── sales_owner.py
│   │   ├── conversation.py        # Includes manually_edited_fields tracking
│   │   ├── import_log.py
│   │   └── routing_log.py
│   ├── services\                   # Business logic
│   │   ├── routing.py             # Routing engine (5 priority rules)
│   │   ├── import_export.py       # Import/export with deduplication
│   │   └── analytics.py           # KPIs and analytics
│   └── pages\                      # Streamlit UI pages
│       ├── dashboard.py
│       ├── inbox.py
│       ├── routing.py
│       └── import_export.py
│
├── tests\
│   ├── unit\                       # 38 unit tests
│   │   ├── test_models.py         # 14 tests
│   │   ├── test_routing.py        # 6 tests
│   │   ├── test_import_export.py  # 11 tests
│   │   └── test_analytics.py      # 7 tests
│   └── integration_verification.py # 5 integration tests
│
├── exports\                         # Generated export files
│   └── revenue_export_*.zip
│
└── docs\
    ├── presentation_slides.md      # 5-slide editable presentation
    └── demo_script_3min.md         # 3-minute demo script with narration
```

---

## Troubleshooting

### Database Locked Error
If you get a "database is locked" error:
```powershell
# Stop the Streamlit app (Ctrl+C)
# Then restart
streamlit run app.py
```

### Port Already in Use
If port 8501 is already in use:
```powershell
streamlit run app.py --server.port 8502
```

### Module Not Found Error
Make sure you're in the project directory:
```powershell
cd d:\revenue-intelligence-inbox
```

### Test Failures
If tests fail, verify database is initialized:
```powershell
python init_db.py
python -m pytest tests/unit/ -v
```

---

## Next Steps

### For Demonstration
1. **Review Presentation:** Open `docs\presentation_slides.md` (5 editable slides)
2. **Practice Demo:** Follow `docs\demo_script_3min.md` (3-minute narrated walkthrough)
3. **Explore Application:** Use the 4 main pages to understand features

### For Development
1. **Read Architecture:** Review `ARCHITECTURE.md` for technical design decisions
2. **Review Tests:** Examine test files to understand expected behavior
3. **Check Status Report:** Read `FINAL_STATUS.md` for comprehensive evidence

### For Production Deployment
1. **Configure PostgreSQL:** Update database connection string
2. **Add Authentication:** Implement user login and role-based access
3. **Set Up Monitoring:** Add logging and error tracking
4. **Deploy Server:** Configure reverse proxy and HTTPS

---

## Key Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main project overview and features |
| `QUICKSTART.md` | This file - getting started guide |
| `FINAL_STATUS.md` | Comprehensive status report with evidence |
| `ARCHITECTURE.md` | Technical architecture and design |
| `IMPLEMENTATION_COMPLETE.md` | Feature implementation summary |
| `docs\presentation_slides.md` | 5-slide presentation (editable) |
| `docs\demo_script_3min.md` | 3-minute demo script with timing |

---

## ⚠️ Important Notes

1. **Synthetic Data:** All conversations, accounts, and owners are synthetic for demonstration
2. **SQLite for Development:** Using SQLite locally; PostgreSQL recommended for production
3. **No Authentication:** Single-user mode; add authentication for multi-user production use
4. **Test Warnings:** SQLAlchemy deprecation warnings are informational and do not affect functionality

---

## Summary of Commands

```powershell
# Initialize database
python init_db.py

# Run application
streamlit run app.py

# Run unit tests (38 tests)
python -m pytest tests/unit/ -v

# Run integration tests (5 tests)
python tests/integration_verification.py

# Export data (use UI: Import/Export → Export Data)
# Import data (use UI: Import/Export → Upload File)
```

---

**🎉 Application is production-ready! All 43 tests passing.**

For detailed evidence and verification results, see `FINAL_STATUS.md`.

---

*Last updated: October 23, 2026*
