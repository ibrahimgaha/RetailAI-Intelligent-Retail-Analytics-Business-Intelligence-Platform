import streamlit as st
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
from components.ui_components import render_interactive_launch_card

load_dotenv()

st.container()

st.markdown("""
    <div class="slide-up" style="padding-bottom: 2rem;">
        <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.05em;">Business Intelligence</h1>
        <p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px;">Interactive insights powered by the Retail Data Warehouse and Power BI. Explore revenue metrics, customer behavior, and sales trends.</p>
    </div>
""", unsafe_allow_html=True)

# Retrieve the embed URL from environment variables
powerbi_url = os.getenv("POWERBI_EMBED_URL", "")

if powerbi_url:
    # 1. Interactive Launch Card (for full screen or external viewing)
    st.markdown(render_interactive_launch_card(
        title="Open Interactive Report",
        description="Launch the full Power BI dashboard in a new interactive window for deep-dive analysis.",
        icon="📊",
        link=powerbi_url
    ), unsafe_allow_html=True)
    
    st.markdown("<br><br><h3 class='fade-in stagger-2'>Embedded View</h3>", unsafe_allow_html=True)
    
    # 2. Embedded View
    st.markdown("""
        <div class="fade-in stagger-3" style="background-color: var(--bg-secondary); border-radius: var(--radius-xl); padding: 0.75rem; border: 1px solid var(--border-color); box-shadow: var(--shadow-lg);">
    """, unsafe_allow_html=True)
    
    components.iframe(powerbi_url, width=None, height=750, scrolling=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Empty State for missing Power BI URL
    st.markdown("""
        <div class="fade-in premium-card" style="text-align: center; padding: 4rem 2rem; border-style: dashed; border-color: rgba(255, 255, 255, 0.2);">
            <div style="font-size: 3.5rem; margin-bottom: 1.5rem;">📊</div>
            <h3 style="margin-top: 0; font-size: 1.75rem; font-weight: 600; margin-bottom: 1rem;">Power BI Integration Not Configured</h3>
            <p style="color: var(--text-muted); max-width: 550px; margin: 0 auto 2rem auto; font-size: 1.1rem;">
                The Business Intelligence dashboard is ready to be embedded. Please link your official Power BI Embed URL in the environment configuration.
            </p>
            <div style="background-color: var(--bg-primary); padding: 1.25rem; border-radius: var(--radius-md); font-family: monospace; display: inline-block; border: 1px solid var(--border-color); color: #60A5FA; font-size: 1rem; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
                POWERBI_EMBED_URL="https://app.powerbi.com/reportEmbed?..."
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
