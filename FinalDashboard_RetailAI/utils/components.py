import streamlit as st


def hero():

    st.markdown("""

<div class="hero">

<div class="hero-title">

RetailAI

</div>

<div class="hero-subtitle">

AI-Powered Retail Analytics Platform

</div>

<div class="hero-description">

Transforming Retail Data into Intelligent Business Decisions through
Business Intelligence, Machine Learning and Artificial Intelligence.

</div>

</div>

""",unsafe_allow_html=True)
    
def feature(icon,title,text):

    st.markdown(f"""

<div class="feature-card">

<div class="feature-icon">

{icon}

</div>

<div class="feature-title">

{title}

</div>

<div class="feature-text">

{text}

</div>

</div>

""",unsafe_allow_html=True)