"""
RetailAI Copilot — AI Service (NVIDIA API)

Provides AI-powered explanations for revenue predictions,
sentiment analysis, business recommendations, and an
intelligent retail business assistant.

Model:    mistralai/mistral-medium-3.5-128b
Endpoint: https://integrate.api.nvidia.com/v1/chat/completions
"""

import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ─── Configuration ──────────────────────────────────────────────────────────
_NVIDIA_ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions"
_NVIDIA_MODEL = "mistralai/mistral-medium-3.5-128b"
_REQUEST_TIMEOUT = 120  # seconds (increased for stability)


# ─── Internal helpers ───────────────────────────────────────────────────────
def _get_api_key() -> str | None:
    """Returns the NVIDIA API key from the environment, or None."""
    key = os.getenv("NVIDIA_API_KEY", "").strip()
    if not key or key == "YOUR_NVIDIA_API_KEY":
        return None
    return key


def _friendly_error(status_code: int | None = None, detail: str = "") -> str:
    """Maps HTTP status codes / exception messages to user-friendly text."""
    if status_code == 401 or status_code == 403:
        return "The NVIDIA API key was rejected. Please check NVIDIA_API_KEY in your .env file."
    if status_code == 404:
        return "The NVIDIA AI model or endpoint could not be found."
    if status_code == 429:
        return "The NVIDIA AI service is temporarily rate-limited."
    if status_code and status_code >= 500:
        return "The NVIDIA AI service is temporarily unavailable."
    if "timeout" in detail.lower() or "timed out" in detail.lower():
        return "The NVIDIA AI request timed out."
    if "connection" in detail.lower():
        return "Could not connect to the NVIDIA AI service."
    return f"NVIDIA AI error: {detail}" if detail else "An unexpected AI error occurred."


def _call_nvidia(messages: list[dict], max_tokens: int = 600, temperature: float = 0.3) -> str | None:
    """
    Makes a single request to the NVIDIA Chat Completions endpoint.
    Returns the assistant reply string, or None if the request failed/timed out.
    """
    api_key = _get_api_key()
    if api_key is None:
        print("[NVIDIA API Log] Missing or unconfigured API key.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": _NVIDIA_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }

    try:
        resp = requests.post(
            _NVIDIA_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=_REQUEST_TIMEOUT,
        )
        print(f"[NVIDIA API Log] HTTP Response Code: {resp.status_code}")
    except requests.exceptions.Timeout:
        print("[NVIDIA API Log] Error: Request timed out after 120s.")
        return None
    except requests.exceptions.ConnectionError:
        print("[NVIDIA API Log] Error: Connection error.")
        return None
    except Exception as exc:
        print(f"[NVIDIA API Log] Exception encountered: {type(exc).__name__}")
        return None

    if resp.status_code != 200:
        try:
            body = resp.json()
            err_detail = body.get("detail", body.get("error", {}).get("message", resp.text[:200]))
            print(f"[NVIDIA API Log] HTTP Error {resp.status_code}: {err_detail}")
        except Exception:
            print(f"[NVIDIA API Log] HTTP Error {resp.status_code}")
        return None

    try:
        data = resp.json()
        choices = data.get("choices", [])
        if not choices:
            print("[NVIDIA API Log] Error: Empty choices in response JSON.")
            return None
        content = choices[0].get("message", {}).get("content", "").strip()
        if not content:
            print("[NVIDIA API Log] Error: Empty message content in response JSON.")
            return None
        return content
    except Exception as parse_exc:
        print(f"[NVIDIA API Log] Error parsing JSON response: {parse_exc}")
        return None


def _generate_fallback_revenue_insight(prediction: float, inputs: dict) -> str:
    """Generates a structured, deterministic business insight in TND from input metrics when API is offline/timing out."""
    qty = inputs.get("TotalQuantity", 1)
    discount_pct = inputs.get("AverageDiscountPercentage", inputs.get("AverageDiscount", 0.0))
    channel = inputs.get("Channel", "Web")
    payment = inputs.get("PaymentMethod", "Card")
    products = inputs.get("NumProducts", 1)

    discount_desc = "heavy" if discount_pct >= 20.0 else "moderate" if discount_pct >= 8.0 else "light"

    return (
        f"### 1. Prediction Summary\n"
        f"The local Linear Regression model calculated a predicted total revenue of **{prediction:,.2f} TND** for this order.\n\n"
        f"### 2. Key Revenue Drivers\n"
        f"- **Order Quantity:** {qty} items across {products} products, representing the main order scale.\n"
        f"- **Discount Level:** A {discount_pct}% discount ({discount_desc}) applied to item pricing.\n"
        f"- **Channel & Payment:** Order placed via **{channel}** and settled using **{payment}**.\n\n"
        f"### 3. Two Business Recommendations\n"
        f"1. **Optimize Discount Thresholds:** Ensure discounts around {discount_pct}% require minimum order quantities to protect profitability.\n"
        f"2. **Cart Value Bundling:** Offer complementary product recommendations on {channel} to increase average basket size.\n\n"
        f"### 4. Model Note\n"
        f"*This prediction is calculated by the local Linear Regression model (R²=0.735) trained on 2,500 retail orders. NVIDIA AI only interprets and contextualizes the result.*"
    )


# ─── System Prompts ─────────────────────────────────────────────────────────
_SYSTEM_BASE = (
    "You are the RetailAI Business Copilot — a professional retail analytics consultant. "
    "Rules you MUST follow:\n"
    "- Always state currency in TND (Tunisian Dinar), NEVER in $.\n"
    "- The local Linear Regression model calculates the prediction; you ONLY interpret the result.\n"
    "- Distinguish discount percentages clearly: if AverageDiscountPercentage is 0.5, treat it strictly as 0.5% (NOT 50%).\n"
    "- Do NOT call a discount 'deep' or 'heavy' unless the percentage clearly exceeds 20%.\n"
    "- Do NOT make unsupported claims or invent historical market statistics, averages, or channel performance percentages.\n"
    "- Keep responses concise, professional, and structured into the 4 requested sections."
)


# ─── Public API ─────────────────────────────────────────────────────────────

def explain_revenue(prediction: float, inputs: dict) -> str:
    """
    Explains a revenue prediction in TND to a business stakeholder.
    Explicitly receives AverageDiscountPercentage (e.g. 6.5) and AverageDiscountDecimal (e.g. 0.065).
    """
    qty = inputs.get("TotalQuantity", 1)
    discount_pct = inputs.get("AverageDiscountPercentage", inputs.get("AverageDiscount", 0.0))
    channel = inputs.get("Channel", "Web")
    payment = inputs.get("PaymentMethod", "Card")
    gender = inputs.get("Gender", "Female")
    products = inputs.get("NumProducts", 1)
    categories = inputs.get("NumCategories", 1)
    year = inputs.get("Year", 2024)
    month = inputs.get("Month", 6)

    user_prompt = (
        f"The local Linear Regression model calculated a predicted total revenue of {prediction:,.2f} TND.\n\n"
        f"Order Input Metrics:\n"
        f"- Total Quantity: {qty}\n"
        f"- Average Discount Percentage: {discount_pct}% (this is a {discount_pct}% discount rate)\n"
        f"- Sales Channel: {channel}\n"
        f"- Payment Method: {payment}\n"
        f"- Gender: {gender}\n"
        f"- Number of Products: {products}\n"
        f"- Number of Categories: {categories}\n"
        f"- Order Date: Year {year}, Month {month}\n\n"
        "Provide a concise business explanation formatted into EXACTLY these 4 sections:\n"
        "1. **Prediction Summary** — State predicted revenue in TND and clarify that the local Linear Regression model calculated it.\n"
        "2. **Key Revenue Drivers** — Factual evaluation of the provided inputs (Quantity, Discount rate of {discount_pct}%, Channel, Payment).\n"
        "3. **Two Business Recommendations** — Exactly 2 practical, actionable recommendations.\n"
        "4. **Model Note** — Clarify that this is a statistical estimate from a local model (R²=0.735)."
    )

    messages = [
        {"role": "system", "content": _SYSTEM_BASE},
        {"role": "user", "content": user_prompt},
    ]

    response = _call_nvidia(messages, max_tokens=600, temperature=0.3)
    if response:
        return response
    
    # Return structured fallback if API fails/times out
    return _generate_fallback_revenue_insight(prediction, inputs)


def explain_sentiment(review_text: str, sentiment: str) -> str:
    """Provides a qualitative analysis of a customer review."""
    messages = [
        {"role": "system", "content": _SYSTEM_BASE},
        {
            "role": "user",
            "content": (
                f'Customer review: "{review_text}"\n'
                f"NLP Sentiment classification: {sentiment}.\n\n"
                "Provide a short analysis:\n"
                "1. **Sentiment Summary**\n"
                "2. **Key Topics**\n"
                "3. **Recommended Action**"
            ),
        },
    ]
    response = _call_nvidia(messages, max_tokens=500, temperature=0.3)
    if response:
        return response

    return (
        f"### 1. Sentiment Summary\n"
        f"The review was classified as **{sentiment}** based on NLP sentiment keyword analysis.\n\n"
        f"### 2. Key Topics\n"
        f"- Customer feedback regarding product experience and overall satisfaction.\n\n"
        f"### 3. Recommended Action\n"
        f"- Log feedback into customer relationship management system and monitor service trends."
    )


def generate_business_recommendations(context_data: str) -> str:
    """Generates strategic recommendations from contextual retail data."""
    messages = [
        {"role": "system", "content": _SYSTEM_BASE},
        {
            "role": "user",
            "content": (
                f"Context:\n{context_data}\n\n"
                "Provide 3 strategic retail recommendations in TND with Markdown headers."
            ),
        },
    ]
    response = _call_nvidia(messages, max_tokens=700, temperature=0.4)
    if response:
        return response

    return (
        "### 1. Enhance Channel Cross-Selling\nPromote top-performing product categories across digital and store channels.\n\n"
        "### 2. Strategic Discount Management\nEstablish dynamic discount ceilings to protect profit margins.\n\n"
        "### 3. Customer Retention Focus\nImplement loyalty rewards for frequent purchasers."
    )


def chat(history: list, user_prompt: str) -> str:
    """Handles a chat turn with full project context."""
    messages = [{"role": "system", "content": _SYSTEM_BASE}]

    # Keep chat history concise — last 4 turns max to avoid latency
    for msg in history[-4:]:
        role = msg.get("role", "user")
        if role not in ("user", "assistant"):
            role = "user"
        messages.append({"role": role, "content": msg["content"]})

    messages.append({"role": "user", "content": user_prompt})
    response = _call_nvidia(messages, max_tokens=800, temperature=0.5)
    if response:
        return response

    return (
        "I am currently operating in offline mode. The RetailAI local machine learning models "
        "and analytics dashboards remain fully available in your navigation menu!"
    )
