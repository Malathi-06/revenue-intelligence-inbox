import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Revenue Intelligence Inbox", page_icon="📊", layout="wide")

st.title("📊 Revenue Intelligence Inbox")
st.caption("⚠️ Demo with synthetic data")

# Sample data
data = {
    'Customer': ['TechCorp', 'DataFlow', 'CloudSync', 'FinanceHub', 'RetailMax', 'HealthTech', 'EduSoft', 'ManufactureX'],
    'Type': ['Discovery', 'Negotiation', 'Demo', 'Discovery', 'Negotiation', 'Demo', 'Discovery', 'Negotiation'],
    'Outcome': ['Won', 'Pending', 'Won', 'Lost', 'Won', 'Pending', 'Won', 'Lost'],
    'Value': [50000, 75000, 45000, 30000, 60000, 40000, 55000, 35000],
    'Owner': ['Alice', 'Bob', 'Carol', 'Alice', 'Bob', 'Carol', 'Alice', 'Bob'],
    'Sentiment': ['Positive', 'Neutral', 'Positive', 'Negative', 'Positive', 'Neutral', 'Positive', 'Negative'],
    'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(8)]
}
df = pd.DataFrame(data)

# Navigation
page = st.sidebar.radio("Navigation", ["📊 Dashboard", "📥 Inbox", "🔀 Routing", "📤 Analytics", "⚙️ Settings"])

if page == "📊 Dashboard":
    st.header("Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Conversations", len(df), "+2")
    col2.metric("Conversion Rate", "62.5%", "+5%")
    col3.metric("Total Value", f"${df['Value'].sum():,.0f}", "+$50K")
    col4.metric("Avg Deal Size", f"${df['Value'].mean():,.0f}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Conversations by Type")
        fig1 = px.bar(df, x='Type', y='Value', color='Outcome', 
                     title="Deal Value by Type & Outcome")
        st.plotly_chart(fig1, use_container_width=True)
        
        st.subheader("Sentiment Analysis")
        sentiment_counts = df['Sentiment'].value_counts()
        fig3 = px.pie(values=sentiment_counts.values, names=sentiment_counts.index,
                     title="Conversation Sentiment Distribution")
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.subheader("Conversion Funnel")
        funnel_data = df['Type'].value_counts()
        fig2 = go.Figure(go.Funnel(
            y=funnel_data.index,
            x=funnel_data.values,
            textposition="inside",
            textinfo="value+percent initial"
        ))
        fig2.update_layout(title="Sales Funnel by Stage")
        st.plotly_chart(fig2, use_container_width=True)
        
        st.subheader("Sales by Owner")
        owner_sales = df.groupby('Owner')['Value'].sum().sort_values(ascending=True)
        fig4 = px.bar(x=owner_sales.values, y=owner_sales.index, orientation='h',
                     title="Total Sales by Owner")
        st.plotly_chart(fig4, use_container_width=True)

elif page == "📥 Inbox":
    st.header("Conversation Inbox")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("🔍 Search customer", "")
    with col2:
        filter_type = st.selectbox("Filter by Type", ["All"] + df['Type'].unique().tolist())
    with col3:
        filter_outcome = st.selectbox("Filter by Outcome", ["All"] + df['Outcome'].unique().tolist())
    
    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['Customer'].str.contains(search, case=False)]
    if filter_type != "All":
        filtered_df = filtered_df[filtered_df['Type'] == filter_type]
    if filter_outcome != "All":
        filtered_df = filtered_df[filtered_df['Outcome'] == filter_outcome]
    
    st.dataframe(filtered_df, use_container_width=True, height=400)
    
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    col1.button("📧 Send Follow-up", use_container_width=True)
    col2.button("📅 Schedule Meeting", use_container_width=True)
    col3.button("📝 Add Notes", use_container_width=True)

elif page == "🔀 Routing":
    st.header("Intelligent Routing & Assignment")
    
    st.subheader("Owner Workload")
    workload = df.groupby('Owner').size().reset_index(name='Conversations')
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(workload, x='Owner', y='Conversations', 
                    title="Current Workload Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Routing Rules:**")
        st.info("✅ Account Ownership - Assign to owner with history")
        st.info("✅ Territory Match - Based on geography")
        st.info("✅ Workload Balance - Distribute evenly")
        st.success("✅ Round Robin - Cycle through team")
        
        st.write("**Recent Assignments:**")
        for _, row in df.head(3).iterrows():
            st.text(f"• {row['Customer']} → {row['Owner']} ({row['Type']})")
    
    st.subheader("Conflict Queue")
    conflicts = df[df['Outcome'] == 'Pending']
    if len(conflicts) > 0:
        st.warning(f"⚠️ {len(conflicts)} conversations need attention")
        st.dataframe(conflicts[['Customer', 'Owner', 'Type', 'Value']], use_container_width=True)
    else:
        st.success("✅ No routing conflicts!")

elif page == "📤 Analytics":
    st.header("Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Deal Value Over Time")
        time_series = df.groupby('Date')['Value'].sum().reset_index()
        fig = px.line(time_series, x='Date', y='Value', markers=True,
                     title="Revenue Trend (Last 8 Days)")
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Win Rate by Type")
        win_rate = df[df['Outcome'] == 'Won'].groupby('Type').size() / df.groupby('Type').size() * 100
        fig = px.bar(x=win_rate.values, y=win_rate.index, orientation='h',
                    title="Win Rate % by Conversation Type")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Performers")
        owner_wins = df[df['Outcome'] == 'Won'].groupby('Owner')['Value'].sum().sort_values(ascending=False)
        st.dataframe(owner_wins.reset_index().rename(columns={'Value': 'Won Value'}), 
                    use_container_width=True)
        
        st.subheader("Sentiment vs Outcome")
        sentiment_outcome = pd.crosstab(df['Sentiment'], df['Outcome'])
        fig = px.imshow(sentiment_outcome, text_auto=True, aspect="auto",
                       title="Sentiment-Outcome Correlation")
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Export Data")
    col1, col2, col3 = st.columns(3)
    col1.download_button("📥 Download CSV", df.to_csv(index=False), "data.csv", "text/csv")
    col2.download_button("📥 Download JSON", df.to_json(), "data.json", "application/json")
    col3.button("📧 Email Report", use_container_width=True)

else:  # Settings
    st.header("⚙️ Settings")
    
    st.subheader("Team Configuration")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Add Sales Owner", placeholder="Enter name...")
        st.selectbox("Default Territory", ["West", "East", "Central", "International"])
    with col2:
        st.number_input("Max Conversations per Owner", value=10, min_value=1, max_value=50)
        st.number_input("Auto-assign Threshold", value=3, min_value=1, max_value=10)
    
    st.subheader("Notification Preferences")
    st.checkbox("Email on new conversation", value=True)
    st.checkbox("Slack notifications", value=False)
    st.checkbox("Daily summary report", value=True)
    
    st.subheader("Integration")
    st.text_input("Salesforce API Key", type="password")
    st.text_input("HubSpot API Key", type="password")
    
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        st.success("✅ Settings saved successfully!")

st.sidebar.markdown("---")
st.sidebar.success("✅ App running")
st.sidebar.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
st.sidebar.caption("Revenue Intelligence Inbox v1.0")
