import streamlit as st
from components.ui_components import (
    render_hero,
    render_feature_card_html,
    render_workflow_step,
    render_value_card
)

st.container()

# ==============================================================================
# 1. HERO SECTION
# ==============================================================================
render_hero(
    title="Transform Your Retail Business with Intelligent Analytics",
    subtitle="AI-Powered Retail Decision Platform",
    description=(
        "RetailAI turns your sales data into actionable business growth. "
        "Explore interactive executive dashboards, predict future order revenue with precision, "
        "analyze customer sentiment, and consult your dedicated AI Business Copilot."
    )
)

# Quick Action / CTA Navigation Bar
st.markdown("<h4 style='text-align: center; color: var(--text-muted); font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;'>Quick Action — Explore Platform</h4>", unsafe_allow_html=True)
cta_col1, cta_col2, cta_col3, cta_col4 = st.columns(4)

with cta_col1:
    st.page_link("pages/2_PowerBI_Dashboard.py", label="Explore Analytics", icon="📊", use_container_width=True)

with cta_col2:
    st.page_link("pages/3_RevenuePrediction.py", label="Predict Revenue", icon="📈", use_container_width=True)

with cta_col3:
    st.page_link("pages/4_SentimentAnalysis.py", label="Analyze Sentiment", icon="💬", use_container_width=True)

with cta_col4:
    st.page_link("pages/5_AIAssistant.py", label="Ask AI Copilot", icon="🤖", use_container_width=True)

st.markdown("<br><hr style='border-color: var(--border-color); margin: 2rem 0 3rem 0;'>", unsafe_allow_html=True)

# ==============================================================================
# 2. CORE CAPABILITIES (FEATURE CARDS)
# ==============================================================================
st.markdown("<div style='text-align: center; margin-bottom: 2rem;' class='slide-up'><h2 style='font-size: 2.25rem; margin-bottom: 0.5rem;'>Core Capabilities</h2><p style='font-size: 1.05rem; color: var(--text-muted); max-width: 650px; margin: 0 auto;'>Everything you need to monitor, forecast, and optimize your retail operations in one place.</p></div>", unsafe_allow_html=True)

f_col1, f_col2, f_col3, f_col4 = st.columns(4)

with f_col1:
    st.markdown(
        render_feature_card_html(
            title="Analytics Dashboard",
            description="Explore retail sales and business performance with interactive visual reports.",
            icon="📊",
            badge="Interactive BI",
            delay_class="stagger-1"
        ),
        unsafe_allow_html=True
    )
    st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
    st.page_link("pages/2_PowerBI_Dashboard.py", label="Open Dashboard →", use_container_width=True)

with f_col2:
    st.markdown(
        render_feature_card_html(
            title="Revenue Prediction",
            description="Estimate expected order revenue using machine learning trained on historical sales.",
            icon="📈",
            badge="ML Forecasting",
            delay_class="stagger-2"
        ),
        unsafe_allow_html=True
    )
    st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
    st.page_link("pages/3_RevenuePrediction.py", label="Calculate Revenue →", use_container_width=True)

with f_col3:
    st.markdown(
        render_feature_card_html(
            title="Sentiment Analysis",
            description="Understand customer opinions and satisfaction directly from customer review text.",
            icon="💬",
            badge="Customer NLP",
            delay_class="stagger-3"
        ),
        unsafe_allow_html=True
    )
    st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
    st.page_link("pages/4_SentimentAnalysis.py", label="Analyze Reviews →", use_container_width=True)

with f_col4:
    st.markdown(
        render_feature_card_html(
            title="AI Business Copilot",
            description="Get practical retail insights, strategic advice, and immediate answers to key business questions.",
            icon="🤖",
            badge="NVIDIA Copilot",
            delay_class="stagger-4"
        ),
        unsafe_allow_html=True
    )
    st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
    st.page_link("pages/5_AIAssistant.py", label="Consult Copilot →", use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 3. HOW IT WORKS (VISUAL DATA WORKFLOW)
# ==============================================================================
workflow_steps_html = "".join([
    render_workflow_step(1, "Data Sources", "Raw sales, store orders, and customer activity.", "🗄️"),
    render_workflow_step(2, "ETL & Data Warehouse", "Data is cleaned, structured, and securely stored.", "⚙️"),
    render_workflow_step(3, "Analytics", "Interactive Power BI reports visualize KPIs.", "📊"),
    render_workflow_step(4, "Machine Learning", "Trained models forecast future revenue patterns.", "🧠"),
    render_workflow_step(5, "AI Insights", "Copilot provides clear, strategic recommendations.", "✨"),
])

workflow_html = (
    f'<div class="workflow-section fade-in">'
    f'<div class="workflow-header">'
    f'<h3 style="font-size: 2rem; margin-bottom: 0.5rem;">How Data Moves from Raw Sales to AI Insights</h3>'
    f'<p style="color: var(--text-muted); font-size: 1.05rem;">A seamless, enterprise-grade journey that powers smart business decisions.</p>'
    f'</div>'
    f'<div class="workflow-flow-grid">{workflow_steps_html}</div>'
    f'</div>'
)

st.markdown(workflow_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 4. BUSINESS VALUE HIGHLIGHTS
# ==============================================================================
st.markdown("<h3 style='text-align: center; margin-bottom: 1.5rem;' class='slide-up'>Why Business Leaders Choose RetailAI</h3>", unsafe_allow_html=True)

v_col1, v_col2, v_col3 = st.columns(3)

with v_col1:
    st.markdown(
        render_value_card(
            title="Full Sales Visibility",
            description="Track revenue across web, store, marketplace, and mobile channels in real time.",
            icon="🎯"
        ),
        unsafe_allow_html=True
    )

with v_col2:
    st.markdown(
        render_value_card(
            title="Data-Driven Decisions",
            description="Base your pricing, discounts, and inventory strategies on empirical machine learning models.",
            icon="⚡"
        ),
        unsafe_allow_html=True
    )

with v_col3:
    st.markdown(
        render_value_card(
            title="Instant Copilot Guidance",
            description="Ask questions in plain English and receive clear, actionable business recommendations.",
            icon="💡"
        ),
        unsafe_allow_html=True
    )

st.markdown("<br><br>", unsafe_allow_html=True)
