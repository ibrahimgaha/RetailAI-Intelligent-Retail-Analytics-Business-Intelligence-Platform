"""
DEPRECATED — This module existed for the old Gemini integration.
All functions now live in services.ai_service (NVIDIA).
This file re-exports them so existing imports don't break.
"""
from services.ai_service import explain_revenue, explain_sentiment, generate_business_recommendations, chat
