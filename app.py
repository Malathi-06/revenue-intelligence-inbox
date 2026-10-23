"""
Revenue Intelligence Inbox - Main Application

Complete sales conversation management platform with:
- Dashboard analytics
- Conversation inbox with search/filter
- Explainable routing with conflict detection
- CSV/JSON import with deduplication
- Manual edit protection
- Export with manifest
"""

import streamlit as st
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Revenue Intelligence Inbox",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database with synthetic data on first run (Streamlit Cloud)
@st.cache_resource(show_spinner="Initializing database...")
def initialize_database():
    """Initialize database with synthetic data on first load."""
    try:
        from src.utils.database import Database
        from src.models.base import Base
        from data.synthetic_data import create_synthetic_data
        
        # Create all tables
        Database.create_all_tables(Base)
        
        # Check if data exists
        session = Database.get_session()
        from src.models import Conversation
        
        try:
            count = session.query(Conversation).count()
        except:
            count = 0
        finally:
            session.close()
        
        # If no data, create synthetic data
        if count == 0:
            create_synthetic_data()
            return "✅ Database initialized (25 conversations)"
        else:
            return f"✅ Database ready ({count} conversations)"
    except Exception as e:
        import traceback
        error_msg = str(e)
        st.error(f"Database initialization error: {error_msg}")
        return f"⚠️ Using in-memory mode"

# Initialize on startup
try:
    init_status = initialize_database()
except Exception as e:
    init_status = f"⚠️ Startup error: {str(e)}"
    st.error(f"Failed to initialize: {e}")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Inbox", "Routing", "Import/Export"],
    index=0
)

# Import and render page modules
try:
    if page == "Dashboard":
        from src.pages import dashboard
        dashboard.render()
    elif page == "Inbox":
        from src.pages import inbox
        inbox.render()
    elif page == "Routing":
        from src.pages import routing
        routing.render()
    elif page == "Import/Export":
        from src.pages import import_export
        import_export.render()
except Exception as e:
    st.error(f"Error loading page: {e}")
    st.exception(e)

# Footer
st.sidebar.markdown("---")
st.sidebar.caption(init_status)
st.sidebar.caption("⚠️ Sample data is synthetic for demonstration only")
st.sidebar.caption("Revenue Intelligence Inbox v1.0")
