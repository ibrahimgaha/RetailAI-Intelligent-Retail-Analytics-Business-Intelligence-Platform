import streamlit as st
from services.sentiment_service import preprocess_review, get_sentiment_confidence
from services.ai_service import explain_sentiment

st.container()

html_header = "<div class='slide-up' style='padding-bottom: 2rem;'><h1 style='font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.05em;'>Sentiment Analysis</h1><p style='font-size: 1.15rem; color: var(--text-muted); max-width: 800px;'>Analyze customer reviews using Natural Language Processing and receive actionable recommendations from the RetailAI Copilot.</p></div>"
st.markdown(html_header, unsafe_allow_html=True)

review_text = st.text_area("Customer Review", height=150, placeholder="Paste a customer review here to analyze its sentiment and extract business insights...")

analyze_btn = st.button("Analyze Sentiment", type="primary")

if analyze_btn and review_text:
    # 1. Local NLP classification
    sentiment = preprocess_review(review_text)
    confidence = get_sentiment_confidence(sentiment)

    # Determine badge color & icon
    color = "#22C55E" if sentiment == "Positive" else "#EF4444" if sentiment == "Negative" else "#F59E0B"
    icon = "😊" if sentiment == "Positive" else "😞" if sentiment == "Negative" else "😐"

    st.markdown("<hr style='border-color: var(--border-color); margin: 3rem 0;'>", unsafe_allow_html=True)

    result_html = (
        f'<div class="fade-in premium-card" style="display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2.5rem; margin-bottom: 2rem; border-left: 4px solid {color};">'
        f'<div style="display: flex; align-items: center; gap: 1rem;">'
        f'<div style="font-size: 3rem;">{icon}</div>'
        f'<div>'
        f'<p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.25rem; text-transform: uppercase; font-weight: 600; letter-spacing: 1px;">Detected Sentiment</p>'
        f'<h2 style="font-size: 2rem; color: {color}; margin: 0;">{sentiment}</h2>'
        f'</div></div>'
        f'<div style="text-align: right;">'
        f'<p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.25rem;">Confidence Score</p>'
        f'<h3 style="margin: 0; color: white;">{confidence * 100:.1f}%</h3>'
        f'</div></div>'
    )
    st.markdown(result_html, unsafe_allow_html=True)

    # 2. AI Analysis
    st.markdown("### RetailAI Copilot Analysis")
    with st.spinner("RetailAI Copilot is analyzing the review..."):
        explanation = explain_sentiment(review_text, sentiment)

    st.info(explanation, icon="✨")

elif analyze_btn:
    st.warning("Please enter a customer review to analyze.")
