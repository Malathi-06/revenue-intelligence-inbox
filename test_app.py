"""Simple test to verify Streamlit Cloud deployment works"""
import streamlit as st

st.title("✅ Streamlit Cloud Test")
st.write("If you see this, the basic deployment works!")

try:
    import pandas as pd
    st.success("✅ Pandas imported")
except Exception as e:
    st.error(f"❌ Pandas failed: {e}")

try:
    import sqlalchemy
    st.success("✅ SQLAlchemy imported")
except Exception as e:
    st.error(f"❌ SQLAlchemy failed: {e}")

try:
    from src.models.base import Base
    st.success("✅ Models imported")
except Exception as e:
    st.error(f"❌ Models failed: {e}")

try:
    from src.utils.database import Database
    st.success("✅ Database imported")
except Exception as e:
    st.error(f"❌ Database failed: {e}")

st.write("---")
st.write("If all checks pass, the main app should work!")
