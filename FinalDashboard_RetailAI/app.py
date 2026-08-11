import streamlit as st
import os

# Must be the first Streamlit command
st.set_page_config(
    page_title="RetailAI | AI-Powered Retail Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found: {file_name}")

load_css("assets/css/style.css")

# --- NAVIGATION SETUP ---
pages = {
    "Analytics": [
        st.Page("pages/1_Home.py", title="Home", icon="🏠"),
        st.Page("pages/2_PowerBI_Dashboard.py", title="BI Dashboard", icon="📊"),
        st.Page("pages/3_RevenuePrediction.py", title="Revenue Prediction", icon="📈"),
    ],
    "Intelligence": [
        st.Page("pages/4_SentimentAnalysis.py", title="Sentiment Analysis", icon="💬"),
        st.Page("pages/5_AIAssistant.py", title="AI Assistant", icon="🤖"),
    ]
}

pg = st.navigation(pages)

# Custom Sidebar Branding (placed after navigation)
with st.sidebar:
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #CBD5E1; font-size: 0.8rem; padding: 1rem 0;">
            <p style="margin-bottom: 0; font-weight: 600; color: white;">RetailAI Enterprise Platform</p>
            <p>Version 1.0.0</p>
        </div>
    """, unsafe_allow_html=True)

# Run the selected page
pg.run()