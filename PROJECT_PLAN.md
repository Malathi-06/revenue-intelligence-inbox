# Revenue Intelligence Inbox - Project Plan

## Executive Summary

**Project**: Revenue Intelligence Inbox Web Application  
**Target User**: Sales Managers  
**Technology**: Python, Streamlit, Pandas, SQLAlchemy, SQLite/PostgreSQL  
**Timeline**: 12 phases, estimated 60-80 hours  
**Status**: Requirements & Design Complete, Ready for Implementation

## Quick Links
- [Full Requirements Specification](.kiro/spec.md)
- [Technical Architecture](ARCHITECTURE.md)
- [Implementation Tasks](#implementation-roadmap)

---

## Key Design Decisions

### 1. Database Strategy: Dual-Mode Persistence
**Decision**: Support both SQLite (local dev) and PostgreSQL (production)

**Rationale**:
- SQLite enables zero-config local development
- PostgreSQL provides production-grade reliability and concurrent access
- SQLAlchemy abstraction makes switching seamless

**Recommendation**: Deploy to **Render with PostgreSQL** for production (automatic backups, managed service)

**Trade-offs**:
- Slight complexity in maintaining compatibility
- Must avoid database-specific features
- Worth it for flexibility and proper production deployment

---

### 2. Routing Engine: Explainable AI Alternative
**Decision**: Rule-based routing with priority ordering, not black-box AI

**Rationale**:
- Transparent decision-making (sales managers can see WHY each assignment happened)
- Auditable and explainable for compliance
- No AI training data or API costs required
- Deterministic behavior (same inputs = same outputs)

**Rules Priority**:
1. Manual override (never auto-reassign)
2. Account ownership (historical relationship)
3. Territory match (geographic/industry alignment)
4. Workload balance (fair distribution)
5. Round-robin (default fallback)

**Conflict Detection**: When multiple rules suggest different owners with similar priority

---

### 3. Duplicate Detection: Conservative Matching
**Decision**: Match on `customer_name + conversation_date + conversation_type`

**Rationale**:
- Conservative approach prevents false matches
- Same customer can have multiple conversations per day if different types (call vs meeting)
- Avoids complex fuzzy matching that could merge distinct conversations

**Edge Cases Handled**:
- Case-insensitive name matching
- Whitespace trimming
- Same-day time variance (ignores hours/minutes)

---

### 4. Manual Edit Protection: Field-Level Tracking
**Decision**: Track which fields were manually edited, protect only those fields from reimport

**Rationale**:
- User corrections should never be overwritten silently
- Allows partial updates (non-edited fields can still be updated from source)
- Full audit trail of manual interventions

**Implementation**: `manually_edited_fields` JSON column stores list of field names

**Example**:
```json
{
  "id": 123,
  "summary": "Manually corrected summary",
  "sales_owner_id": 5,
  "manually_edited_fields": ["summary", "sales_owner_id"]
}
```
Next import: Update `risks`, `follow_ups`, `outcome` but skip `summary` and `sales_owner_id`

---

### 5. Import Workflow: Preview-Then-Commit
**Decision**: Two-step import process with validation preview before commit

**Rationale**:
- Prevents accidental data corruption
- Gives user chance to review what will change
- Enables informed decision-making

**Steps**:
1. Parse & validate file → show errors immediately
2. Detect duplicates → show counts (new/update/skip)
3. User reviews preview
4. User clicks "Commit Import"
5. Transaction executes (all-or-nothing)

**Rollback**: Any error during commit rolls back entire transaction (no partial imports)

---

### 6. Export Format: CSV + JSON with Manifest
**Decision**: Support both formats, always include metadata manifest

**Rationale**:
- CSV: Excel-compatible, widely used for data analysis
- JSON: Structured format, preserves nested data (risks, follow-ups)
- Manifest: Reproducibility (know what filters were applied, when exported)

**Manifest Contents**:
- Export timestamp
- Record count
- Filter criteria (date range, owner, type, etc.)
- Schema version (for future compatibility)

**Packaging**: .zip file containing `data.csv` (or `data.json`) + `manifest.json`

---

### 7. Synthetic Data: Clearly Labeled Examples
**Decision**: Pre-populate with 20-30 synthetic conversations, labeled as example data

**Rationale**:
- Enables immediate demo without user-provided data
- Showcases all features (routing conflicts, risks, follow-ups)
- Clearly marked as synthetic to prevent confusion

**Data Characteristics**:
- Realistic but obviously fictional customer names (Acme Corp, Globex Industries)
- Variety of scenarios (won deals, lost deals, at-risk, follow-up needed)
- Multiple sales owners with different workloads
- Routing conflicts for demonstration purposes

**Ethical Note**: Never fabricate findings and present them as real analytics

---

### 8. Testing Strategy: >80% Coverage Requirement
**Decision**: Automated tests for routing, import, export with coverage reporting

**Rationale**:
- Complex business logic (routing rules, duplicate detection) requires verification
- Prevent regressions during future changes
- Build confidence in data integrity

**Key Test Areas**:
1. **Routing Engine**: All 5 rules, conflict detection, explanation generation
2. **Import Service**: Duplicate detection, manual edit protection, transaction rollback
3. **Export Service**: Filter application, manifest generation, archive creation
4. **Analytics**: KPI calculations, chart data aggregation

**Tools**: pytest, pytest-cov, pandas.testing

---

### 9. Security: Defense-in-Depth
**Decision**: Multiple layers of security despite single-user v1

**Rationale**:
- Input validation prevents injection attacks
- File upload restrictions prevent malicious files
- SQLAlchemy ORM prevents SQL injection
- Future-proofed for multi-user v2

**Security Measures**:
1. Schema validation before import
2. File size limits (10MB)
3. File type validation (content-based, not just extension)
4. Parameterized queries (ORM)
5. Input sanitization (strip dangerous characters)
6. HTTPS in production (deployment config)

**Privacy Considerations**:
- Document data sensitivity in README
- Recommend encryption at rest (database-level)
- No authentication in v1 (noted in docs as future requirement)

---

### 10. Deployment: Platform Recommendation
**Decision**: Recommend **Render** for production deployment

**Rationale**:

| Platform | Pros | Cons |
|----------|------|------|
| **Render** (✅ Recommended) | Free PostgreSQL, easy GitHub deploy, automatic HTTPS | Free tier has some limitations |
| Streamlit Cloud | Easiest Streamlit deploy, free tier | Ephemeral filesystem (SQLite risky), external DB needed |
| AWS ECS + RDS | Enterprise-grade, full control | Complex setup, higher cost |
| Heroku | Easy deploy, PostgreSQL add-on | More expensive than Render |

**Render Deployment Steps**:
1. Push to GitHub
2. Create PostgreSQL database (free tier available)
3. Create Web Service from repo
4. Set environment variable: `DATABASE_URL`
5. Deploy (automatic on git push)

**Alternative**: Local deployment with persistent SQLite for personal use

---

## Implementation Roadmap

### Phase 1: Foundation (8-10 hours)
- **T1.1-T1.6**: Project structure, dependencies, database models, migrations, tests

**Deliverables**:
- `requirements.txt` with all dependencies
- SQLAlchemy models for all entities
- Alembic migration scripts
- pytest configuration
- Database initialization script
- Synthetic data seeding script

**Success Criteria**:
- `python init_db.py` creates database with sample data
- All model tests pass

---

### Phase 2: Data Layer (6-8 hours)
- **T2.1-T2.7**: Implement CRUD operations, relationships, tests

**Deliverables**:
- Repository pattern for data access
- CRUD functions for all models
- Relationship navigation (account → conversations)
- Unit tests for all data operations

**Success Criteria**:
- Can create, read, update, delete all entities
- Tests achieve >90% coverage for models

---

### Phase 3: Routing Engine (8-10 hours)
- **T3.1-T3.8**: Implement all routing rules, conflict detection, logging

**Deliverables**:
- `services/routing.py` with all 5 rules
- Conflict detection logic
- Routing explanation generator
- Routing log creation
- Comprehensive test suite

**Success Criteria**:
- All rules assign correctly in isolation
- Priority ordering works correctly
- Conflicts detected when rules disagree
- Explanations are clear and accurate
- Tests cover all rules + edge cases

---

### Phase 4: Import/Export Service (10-12 hours)
- **T4.1-T4.11**: CSV/JSON parsing, duplicate detection, manual edit protection, export

**Deliverables**:
- CSV and JSON parsers with validation
- Duplicate detection algorithm
- Manual edit protection logic
- Import preview functionality
- Transaction-based import commit
- CSV and JSON export generators
- Manifest generation
- Zip archive creation

**Success Criteria**:
- Invalid files rejected with clear errors
- Duplicates detected correctly
- Manual edits protected on reimport
- Import rolls back on error
- Exports include all filtered data + manifest
- Tests cover all import/export scenarios

---

### Phase 5: Analytics Service (4-6 hours)
- **T5.1-T5.4**: KPI calculations, chart data aggregation, filtering

**Deliverables**:
- `services/analytics.py` with KPI functions
- Time-series aggregation for charts
- Filter application logic
- Unit tests

**Success Criteria**:
- All 5 KPIs calculate correctly
- Chart data formatted for Plotly
- Filters apply to all queries
- Tests verify calculations

---

### Phase 6: Dashboard UI (6-8 hours)
- **T6.1-T6.8**: Streamlit dashboard page with KPIs and charts

**Deliverables**:
- Main app with navigation
- Dashboard page with KPI cards
- 4 interactive Plotly charts
- Date range filter

**Success Criteria**:
- Dashboard loads without errors
- All KPIs display with correct values
- Charts render and update with date filter
- Loads in <2 seconds with 1000 conversations

---

### Phase 7: Inbox UI (8-10 hours)
- **T7.1-T7.8**: Searchable conversation list, detail view, manual editing

**Deliverables**:
- Inbox page with search bar
- Filter controls (type, date, owner, follow-up, risk)
- Sorting (date, customer, owner)
- Paginated conversation list
- Conversation detail modal/expander
- Manual edit form with field tracking
- Visual indicators for risks/follow-ups

**Success Criteria**:
- Search finds conversations by name, owner, keywords
- Filters work correctly (individually and combined)
- Pagination handles 100+ records
- Manual edits tracked and persist
- Detail view shows all conversation fields

---

### Phase 8: Routing UI (4-6 hours)
- **T8.1-T8.6**: Conflict queue, manual override, audit log

**Deliverables**:
- Routing page
- Conflict queue with suggested assignments
- Manual override form
- Routing audit log with filters

**Success Criteria**:
- Conflicts appear in queue
- Manual override creates routing log
- Audit log shows all assignments
- Explanations are visible

---

### Phase 9: Import/Export UI (6-8 hours)
- **T9.1-T9.9**: File upload, preview, import execution, export download

**Deliverables**:
- Import/Export page
- File upload widget
- Import preview (new/update/skip counts)
- Validation error display
- Import commit button
- Import history table
- Export filter configuration
- Export format selection
- Download button

**Success Criteria**:
- File uploads work for CSV and JSON
- Preview shows accurate counts
- Validation errors clear and actionable
- Import commits successfully
- Import history displays all operations
- Export downloads .zip with data + manifest

---

### Phase 10: Testing (6-8 hours)
- **T10.1-T10.5**: Integration tests, coverage reporting

**Deliverables**:
- Integration tests for full workflows
- Test coverage report (>80%)
- CI configuration (optional: GitHub Actions)

**Success Criteria**:
- All tests pass
- Coverage >80%
- No flaky tests

---

### Phase 11: Documentation (6-8 hours)
- **T11.1-T11.8**: README, presentation, demo script, deployment guide

**Deliverables**:
- Comprehensive README.md
- Five-slide presentation (PowerPoint/Google Slides)
- Three-minute demo script with timestamps
- Deployment guide (local + Render)
- Schema documentation
- Security notes

**Success Criteria**:
- README enables anyone to set up locally
- Presentation covers all key features
- Demo script fits in 3 minutes
- Deployment guide tested on Render

---

### Phase 12: Polish & Deployment (4-6 hours)
- **T12.1-T12.8**: Error handling, responsive layout, performance testing, deployment

**Deliverables**:
- User-friendly error messages throughout
- Mobile-responsive layout
- Loading indicators for long operations
- Environment configuration (dev/prod)
- Successful local deployment
- Successful Render deployment
- Performance test results

**Success Criteria**:
- No user-facing error stack traces
- App usable on mobile/tablet
- Dashboard loads in <2 seconds with 1000 records
- Import processes 500 records in <5 seconds
- Deployed to Render with PostgreSQL
- All features work in production

---

## Total Estimated Effort

| Phase | Hours |
|-------|-------|
| 1. Foundation | 8-10 |
| 2. Data Layer | 6-8 |
| 3. Routing Engine | 8-10 |
| 4. Import/Export Service | 10-12 |
| 5. Analytics Service | 4-6 |
| 6. Dashboard UI | 6-8 |
| 7. Inbox UI | 8-10 |
| 8. Routing UI | 4-6 |
| 9. Import/Export UI | 6-8 |
| 10. Testing | 6-8 |
| 11. Documentation | 6-8 |
| 12. Polish & Deployment | 4-6 |
| **Total** | **76-100 hours** |

**Timeline**: 2-3 weeks for one developer working full-time

---

## Risk Mitigation

### Technical Risks
1. **SQLite → PostgreSQL migration issues**
   - Mitigation: Use SQLAlchemy, test on both databases early
   
2. **Import performance with large files**
   - Mitigation: Chunked processing, progress indicators, set 10MB limit
   
3. **Streamlit state management complexity**
   - Mitigation: Keep UI simple, document session state usage

### Deployment Risks
1. **Render free tier limitations**
   - Mitigation: Document upgrade path, provide AWS alternative
   
2. **Database persistence on Streamlit Cloud**
   - Mitigation: Clearly document PostgreSQL requirement, not just SQLite

---

## Success Metrics

### Functional Completeness
- [ ] All 13 core features implemented (F1-F11 from spec)
- [ ] All acceptance criteria met
- [ ] Automated tests >80% coverage
- [ ] Documentation complete

### Performance
- [ ] Dashboard loads in <2 seconds (1000 conversations)
- [ ] Search/filter results in <500ms
- [ ] Import processes 500 records in <5 seconds

### Usability
- [ ] Sales manager can navigate without training
- [ ] Error messages are clear and actionable
- [ ] Mobile-responsive layout works

### Deployment
- [ ] One-command local setup
- [ ] Successfully deployed to Render with PostgreSQL
- [ ] Demo runs in 3 minutes

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Ask essential questions** if any requirements are unclear
3. **Begin Phase 1** (Project Setup) once approved
4. **Implement incrementally**, testing each phase before moving forward
5. **Demo after Phase 12** for final review

---

## Essential Questions Before Starting

1. **AI Summarization**: Should the app generate conversation summaries using AI (e.g., OpenAI API), or import pre-generated summaries?
   - **Recommendation**: Import pre-generated summaries to reduce complexity and avoid API costs
   
2. **Authentication**: Is single-user deployment acceptable for v1, or is multi-user authentication required?
   - **Recommendation**: Single-user v1 (faster to build), add auth in v2
   
3. **Real-time Updates**: Should dashboard auto-refresh, or is manual refresh acceptable?
   - **Recommendation**: Manual refresh v1, add auto-refresh later if needed

4. **Data Source**: Will you provide real conversation data, or should we use only synthetic data?
   - **Recommendation**: Start with synthetic data for demo, add real data import later

5. **Deployment Target**: Do you have a preference for hosting platform?
   - **Recommendation**: Render (easiest with PostgreSQL), but can adapt to AWS/Heroku if preferred

---

*Ready to begin implementation? All requirements, architecture, and tasks are documented. Let's build this!*
