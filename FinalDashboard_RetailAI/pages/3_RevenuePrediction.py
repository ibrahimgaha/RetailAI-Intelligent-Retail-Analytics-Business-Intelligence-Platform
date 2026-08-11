import streamlit as st
from services.prediction_service import predict_revenue
from services.ai_service import explain_revenue

st.container()

html_header = "<div class='slide-up' style='padding-bottom: 2rem;'><h1 style='font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.05em;'>Revenue Prediction</h1><p style='font-size: 1.15rem; color: var(--text-muted); max-width: 800px;'>Forecast total revenue using our Linear Regression model trained on 2,500 retail orders, then receive deep AI-driven business insights from the RetailAI Copilot.</p></div>"
st.markdown(html_header, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Input Form ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("#### 👤 Customer & Channel")
    gender = st.selectbox(
        "Gender",
        ["Female", "Male", "Unknown"]
    )
    channel = st.selectbox(
        "Channel",
        ["Web", "Store", "Marketplace", "Mobile App"]
    )
    payment = st.selectbox(
        "Payment Method",
        ["COD", "Card", "Cash", "Wallet"]
    )
    col_y, col_m = st.columns(2)
    with col_y:
        year = st.number_input("Year", min_value=2020, max_value=2030, value=2024)
    with col_m:
        month = st.number_input("Month (1–12)", min_value=1, max_value=12, value=6)

with col2:
    st.markdown("#### 🛒 Order Metrics")
    qty = st.number_input("Total Quantity", min_value=1, value=5)
    discount = st.number_input("Average Discount (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.5, help="Enter the discount percentage (e.g., 5 for 5%).")
    products = st.number_input("Number of Products", min_value=1, value=3)
    categories = st.number_input("Number of Categories", min_value=1, value=2)

st.markdown("<br>", unsafe_allow_html=True)

# --- How the model works info box ---
with st.expander("ℹ️  How does the prediction work?"):
    st.markdown("""
**Model:** Linear Regression — trained on 2,500 retail orders.

**Accuracy:** R² ≈ 0.735 (explains ~73.5% of variance in order revenue).

**Features evaluated:**
- Numerical: `YearNumber`, `MonthNumber`, `TotalQuantity`, `AvgDiscount`, `NumberOfProducts`, `NumberOfCategories`
- Categorical One-Hot Encoded: `Gender`, `ChannelName`, `PaymentMethod`
""")

predict_btn = st.button("⚡  Generate Prediction & AI Insights", type="primary", use_container_width=True)

# Compute explicit discount representation
discount_pct = float(discount)
discount_dec = discount_pct / 100.0

# Package input dictionary with explicit Percentage and Decimal values
input_data = {
    "Gender": gender,
    "Channel": channel,
    "PaymentMethod": payment,
    "Year": year,
    "Month": month,
    "TotalQuantity": qty,
    "AverageDiscount": discount_pct,
    "AverageDiscountPercentage": discount_pct,  # e.g., 6.5 for 6.5%
    "AverageDiscountDecimal": discount_dec,     # e.g., 0.065
    "NumProducts": products,
    "NumCategories": categories,
}

# Execute prediction & AI call ONLY when button is clicked
if predict_btn:
    with st.spinner("Running local Linear Regression model..."):
        predicted_revenue = predict_revenue(input_data)

    with st.spinner("RetailAI Copilot is analyzing the prediction..."):
        explanation = explain_revenue(predicted_revenue, input_data)

    # Store in session state to prevent duplicate requests on Streamlit reruns
    st.session_state["revenue_prediction_result"] = {
        "predicted_revenue": predicted_revenue,
        "input_data": input_data,
        "explanation": explanation
    }

# Render results from session_state if available
if "revenue_prediction_result" in st.session_state:
    res = st.session_state["revenue_prediction_result"]
    pred_val = res["predicted_revenue"]
    exp_text = res["explanation"]

    st.markdown("<hr style='border-color: var(--border-color); margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("### 📊 Prediction Results")

    result_html = (
        f'<div class="fade-in premium-card" style="display: flex; justify-content: space-between; align-items: center; padding: 2rem 3rem; margin-bottom: 2rem; border-left: 4px solid var(--accent-primary);">'
        f'<div>'
        f'<p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.5rem; text-transform: uppercase; font-weight: 600; letter-spacing: 1px;">Predicted Total Revenue</p>'
        f'<h2 style="font-size: 3.5rem; color: #60A5FA; margin: 0; font-weight: 700;">{pred_val:,.2f} TND</h2>'
        f'</div>'
        f'<div style="text-align: right;">'
        f'<div style="display: inline-block; background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.3); border-radius: 8px; padding: 0.5rem 1rem; margin-bottom: 0.75rem;"><span style="color: #93C5FD; font-weight: 600;">Linear Regression</span></div><br>'
        f'<span style="color: var(--text-muted); font-size: 0.9rem;">Model Accuracy (R²): </span><strong style="color: white;">0.735</strong>'
        f'</div>'
        f'</div>'
    )
    st.markdown(result_html, unsafe_allow_html=True)

    # Render AI Explanation
    st.markdown("### ✨ RetailAI Copilot Insights")
    st.info(exp_text, icon="🤖")
