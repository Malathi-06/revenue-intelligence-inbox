import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Revenue Intelligence Inbox", page_icon="📊", layout="wide")

st.title("📊 Revenue Intelligence Inbox")
st.caption("⚠️ Demo with synthetic data")

# Sample data
data = {
    'Customer': ['TechCorp', 'DataFlow', 'CloudSync', 'FinanceHub', 'RetailMax'],
    'Type': ['Discovery', 'Negotiation', 'Demo', 'Discovery', 'Negotiation'],
    'Outcome': ['Won', 'Pending', 'Won', 'Lost', 'Won'],
    'Value': [50000, 75000, 45000, 30000, 60000]
}
df = pd.DataFrame(data)

# Navigation
page = st.sidebar.radio("Navigation", ["Dashboard", "Inbox"])

if page == "Dashboard":
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Conversations", "5")
    col2.metric("Conversion Rate", "60%")
    col3.metric("Total Value", "$260K")
    
    st.subheader("Conversations by Type")
    fig = px.bar(df, x='Type', y='Value', color='Outcome')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.subheader("Conversation Inbox")
    st.dataframe(df, use_container_width=True)

st.sidebar.success("✅ App deployed successfully!")
