# Revenue Intelligence Inbox

> A Revenue Intelligence platform for sales managers to monitor conversations, route opportunities intelligently, and maintain data quality.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- **📊 Dashboard Analytics**: KPIs and interactive charts for conversation trends
- **📥 Smart Inbox**: Searchable, filterable conversation list with detailed views
- **🎯 Explainable Routing**: Rule-based sales owner assignment with conflict detection
- **📤 Import/Export**: CSV/JSON data import with deduplication and manual edit protection
- **🔒 Data Quality**: Field-level edit tracking and audit trails
- **📜 Full Audit**: Complete history of imports and routing decisions
- **🎭 Sample Data**: Pre-populated synthetic data for demonstration

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher ✅
- pip (Python package manager) ✅
- Database already initialized with sample data ✅

### Running the Application

**The application is ready to run!**

```bash
# Navigate to project directory
cd d:\revenue-intelligence-inbox

# Start the application
streamlit run app.py
```

**The app opens automatically at `http://localhost:8501`**

### Running Tests

```bash
# Run all tests
python -m pytest tests/unit/ -v

# Run with coverage
python -m pytest tests/unit/ --cov=src --cov-report=html
```

**Expected:** 38 tests pass ✅

---

## 📁 Project Structure

```
revenue-intelligence-inbox/
├── .kiro/
│   ├── spec.md                    # Complete requirements specification
│   └── hooks/                     # Automation hooks
├── src/
│   ├── models/                    # SQLAlchemy database models
│   │   ├── account.py
│   │   ├── sales_owner.py
│   │   ├── conversation.py
│   │   ├── import_log.py
│   │   └── routing_log.py
│   ├── services/                  # Business logic
│   │   ├── analytics.py           # KPI and chart calculations
│   │   ├── routing.py             # Sales owner routing engine
│   │   └── import_export.py       # Data import/export handlers
│   ├── pages/                     # Streamlit UI pages
│   │   ├── dashboard.py
│   │   ├── inbox.py
│   │   ├── routing.py
│   │   └── import_export.py
│   └── utils/                     # Utilities
│       ├── config.py              # Configuration management
│       ├── database.py            # Database connection
│       └── validators.py          # Input validation
├── tests/
│   ├── unit/                      # Unit tests
│   └── integration/               # Integration tests
├── data/
│   ├── synthetic_data.py          # Sample data generator
│   └── revenue.db                 # SQLite database (created on init)
├── docs/
│   ├── ARCHITECTURE.md            # Technical architecture
│   ├── PROJECT_PLAN.md            # Implementation plan
│   └── presentation.pptx          # Five-slide presentation
├── app.py                         # Streamlit entry point
├── init_db.py                     # Database initialization
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🎯 Key Features Deep Dive

### Dashboard Analytics
Monitor team performance with:
- **KPIs**: Total conversations, active opportunities, follow-ups needed, avg response time, win rate
- **Charts**: Conversations over time, by type, by owner, opportunity stages
- **Filtering**: Date range selection affects all metrics

### Smart Inbox
- **Search**: Find conversations by customer name, sales owner, or keywords
- **Filter**: By type (call/meeting), date, owner, follow-up status, risk level
- **Sort**: By date, customer, or owner
- **Details**: View full conversation with summary, risks, follow-ups, and outcomes
- **Manual Editing**: Edit any field with automatic tracking

### Explainable Routing Engine
Assigns conversations to sales owners using transparent rules:
1. **Manual Override**: Protected from auto-reassignment
2. **Account Ownership**: Assign to owner with most conversations on account
3. **Territory Match**: Assign based on geographic/industry alignment
4. **Workload Balance**: Distribute fairly across team
5. **Round Robin**: Default rotation for new accounts

**Conflict Detection**: Flags when multiple rules suggest different owners

### Smart Import/Export
- **Import**: CSV or JSON with schema validation
- **Duplicate Detection**: Match on customer + date + type
- **Edit Protection**: Manual corrections never overwritten
- **Preview**: See new/update/skip counts before committing
- **Transaction Safety**: All-or-nothing import (rollback on error)
- **Export**: CSV or JSON with metadata manifest

---

## 🗄️ Database

### Development (SQLite)
- File: `data/revenue.db`
- Zero configuration
- Automatic creation on `init_db.py`
- Great for local development and testing

### Production (PostgreSQL)
Recommended for deployment:
- **Render**: Managed PostgreSQL (easiest setup)
- **AWS RDS**: Enterprise-grade
- **Supabase**: PostgreSQL with built-in APIs

**Why PostgreSQL for production?**
- ACID compliance for data integrity
- Better concurrent access than SQLite
- Automatic backups on managed services
- No file locking issues

### Migration
Switch database by changing `DATABASE_URL` environment variable:
```bash
# SQLite (default)
DATABASE_URL=sqlite:///data/revenue.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@host:5432/database
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=src --cov-report=html
```

### View Coverage Report
```bash
# Open htmlcov/index.html in browser
```

### Test Structure
- **Unit Tests**: Models, routing rules, import logic
- **Integration Tests**: Complete workflows (import, export, routing)
- **Target**: >80% coverage

---

## 📊 Sample Data

The application includes synthetic data for demonstration:
- **20-30 conversations** covering various scenarios
- **5-10 accounts** (e.g., Acme Corp, Globex Industries)
- **3-5 sales owners** with different workloads
- **Scenarios**: Won deals, lost deals, at-risk, routing conflicts

**⚠️ Important**: All sample data is clearly labeled as synthetic. Never fabricate findings and present them as real analytics.

### Generate New Sample Data
```bash
python data/synthetic_data.py
```

---

## 🚀 Deployment

### Local Deployment (SQLite)
Perfect for personal use:
```bash
streamlit run app.py
```

### Production Deployment (Render + PostgreSQL)

#### Prerequisites
- GitHub account
- Render account (free tier available)

#### Steps

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Create PostgreSQL Database on Render**
   - Log into [Render](https://render.com/)
   - Click "New +" → "PostgreSQL"
   - Name: `revenue-db`
   - Plan: Free (or paid for production)
   - Create database
   - Copy "Internal Database URL"

3. **Create Web Service on Render**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Name: `revenue-intelligence-inbox`
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

4. **Set Environment Variables**
   - Click "Environment" tab
   - Add variable:
     - Key: `DATABASE_URL`
     - Value: (paste Internal Database URL from step 2)
   - Add variable:
     - Key: `ENVIRONMENT`
     - Value: `production`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-5 minutes)
   - Access your app at the provided URL

6. **Initialize Database** (first deploy only)
   - Use Render Shell to run:
   ```bash
   python init_db.py
   ```

#### Alternative: Streamlit Cloud
- Push to GitHub
- Connect at [share.streamlit.io](https://share.streamlit.io/)
- Add PostgreSQL URL in secrets (not recommended: use external PostgreSQL)

---

## 🔧 Configuration

### Environment Variables

Create `.env` file for local development:
```bash
DATABASE_URL=sqlite:///data/revenue.db
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

For production (Render), set environment variables in dashboard:
```bash
DATABASE_URL=postgresql://...
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
```

### Configuration Options

Edit `src/utils/config.py`:
```python
# Import settings
MAX_IMPORT_SIZE_MB = 10          # Maximum file upload size
IMPORT_CHUNK_SIZE = 500          # Records per transaction

# Routing settings
WORKLOAD_IMBALANCE_THRESHOLD = 5 # Conflict threshold
WORKLOAD_WINDOW_DAYS = 30        # Lookback for workload calculation
```

---

## 🔒 Security & Privacy

### Current Security Measures
- ✅ Input validation on all imports
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ File upload size limits (10MB)
- ✅ File type validation (content-based)
- ✅ Parameterized database queries
- ✅ HTTPS recommended for production

### Data Privacy Considerations
- **Sensitive Data**: Customer names, conversation content may be sensitive
- **Recommendation**: Use encryption at rest (database-level)
- **Recommendation**: Enable HTTPS in production (automatic on Render)
- **Note**: No authentication in v1 (single-user deployment)

### Future Security (v2+)
- [ ] Multi-user authentication (OAuth, SSO)
- [ ] Role-based access control (admin, manager, viewer)
- [ ] Field-level encryption for sensitive data
- [ ] Audit log of all user actions
- [ ] API rate limiting

---

## 📖 API & Schema Documentation

### Import Schema

#### CSV Format
Required columns:
```csv
customer_name,account_name,conversation_type,conversation_date,duration_minutes,summary,outcome
John Doe,Acme Corp,call,2026-10-15,45,"Discussed Q4 requirements","Follow-up meeting scheduled"
```

Optional columns:
```csv
risks,follow_ups,sales_owner_email,requires_follow_up,risk_level
```

#### JSON Format
```json
{
  "conversations": [
    {
      "customer_name": "John Doe",
      "account_name": "Acme Corp",
      "conversation_type": "call",
      "conversation_date": "2026-10-15T14:30:00Z",
      "duration_minutes": 45,
      "summary": "Discussed Q4 requirements",
      "risks": [
        {"type": "budget", "description": "Budget constraints mentioned"}
      ],
      "follow_ups": [
        {"action": "Send proposal", "due_date": "2026-10-20"}
      ],
      "outcome": "Follow-up meeting scheduled",
      "requires_follow_up": true,
      "risk_level": "medium"
    }
  ]
}
```

### Export Schema

Exports include:
1. **Data file** (`conversations.csv` or `conversations.json`)
2. **Manifest** (`manifest.json`)

Manifest structure:
```json
{
  "export_timestamp": "2026-10-23T10:30:00Z",
  "schema_version": "1.0",
  "record_count": 25,
  "filters_applied": {
    "date_range": ["2026-10-01", "2026-10-23"],
    "sales_owner": "Jane Smith",
    "conversation_type": null
  },
  "export_format": "csv"
}
```

---

## 🎤 Presentation & Demo

### Five-Slide Presentation
Location: `docs/presentation.pptx`

**Slides**:
1. Problem & Solution
2. Key Features & Benefits
3. Architecture & Tech Stack
4. Demo Flow
5. Deployment & Next Steps

### Three-Minute Demo Script

**0:00-0:30** - Dashboard
- Show KPIs and charts
- Demonstrate date range filtering

**0:30-1:00** - Inbox
- Search for customer
- Apply filters
- View conversation details

**1:00-1:30** - Routing
- Show routing explanation
- Demonstrate conflict resolution
- Manual override

**1:30-2:15** - Import
- Upload CSV file
- View preview (new/update/skip)
- Commit import
- Show import history

**2:15-2:45** - Export
- Apply filters
- Select JSON format
- Download export archive
- Show manifest

**2:45-3:00** - Summary
- Recap key value propositions
- Q&A

---

## 🤝 Contributing

(To be added in v2)

---

## 📄 License

MIT License - see LICENSE file for details

---

## 📚 Additional Documentation

- **[.kiro/spec.md](.kiro/spec.md)**: Complete requirements specification
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Technical architecture and design
- **[PROJECT_PLAN.md](PROJECT_PLAN.md)**: Implementation roadmap

---

## 🆘 Troubleshooting

### Database Issues

**Problem**: `sqlalchemy.exc.OperationalError: no such table`
**Solution**: Run `python init_db.py` to initialize database

**Problem**: SQLite database locked
**Solution**: Close other connections or switch to PostgreSQL

### Import Issues

**Problem**: "Invalid schema" error on import
**Solution**: Check CSV has required columns: `customer_name`, `account_name`, `conversation_type`, `conversation_date`

**Problem**: Import preview shows 0 new records
**Solution**: Check duplicate detection rules - records may already exist

### Deployment Issues

**Problem**: Render app crashes on startup
**Solution**: Check environment variables are set correctly (especially `DATABASE_URL`)

**Problem**: Streamlit Cloud app loses data on restart
**Solution**: Use external PostgreSQL database (not local SQLite)

---

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- See [.kiro/spec.md](.kiro/spec.md) for complete specifications

---

## 🗺️ Roadmap

### v1.0 (Current)
- ✅ Dashboard analytics
- ✅ Smart inbox
- ✅ Explainable routing
- ✅ Import/export with deduplication
- ✅ Manual edit protection
- ✅ Audit trails

### v1.1 (Future)
- [ ] Dashboard auto-refresh
- [ ] Email notifications for conflicts
- [ ] Advanced filtering (saved filters)
- [ ] Bulk conversation actions

### v2.0 (Future)
- [ ] Multi-user authentication
- [ ] Role-based access control
- [ ] AI-powered summarization (OpenAI/Anthropic)
- [ ] Calendar integration
- [ ] CRM integration (Salesforce, HubSpot)
- [ ] Mobile app

---

**Built with ❤️ using Python, Streamlit, and Pandas**

*Last updated: October 23, 2026*
