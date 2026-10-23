"""
Revenue Intelligence Inbox - Main Application
"""

import streamlit as st
import sys
from pathlib import Path

# Fix imports for Streamlit Cloud
file_path = Path(__file__).resolve()
root_path = file_path.parent
if root_path not in sys.path:
    sys.path.insert(0, str(root_path))

st.set_page_config(
    page_title="Revenue Intelligence Inbox",
    page_icon="📊",
    layout="wide"
)

# Initialize database
@st.cache_resource
def init_db():
    try:
        from src.utils.database import Database
        from src.models.base import Base
        from data.synthetic_data import create_synthetic_data
        
        Database.create_all_tables(Base)
        
        session = Database.get_session()
        from src.models import Conversation
        count = session.query(Conversation).count()
        session.close()
        
        if count == 0:
            create_synthetic_data()
        return True
    except Exception as e:
        st.error(f"Database error: {e}")
        return False

init_db()

# Navigation
page = st.sidebar.radio("Navigation", ["Dashboard", "Inbox", "Routing", "Import/Export"])

# Load pages
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
    else:
        from src.pages import import_export
        import_export.render()
except Exception as e:
    st.error(f"Page error: {e}")
    import traceback
    st.code(traceback.format_exc())

st.sidebar.caption("⚠️ Synthetic data")
st.sidebar.caption("v1.0")
