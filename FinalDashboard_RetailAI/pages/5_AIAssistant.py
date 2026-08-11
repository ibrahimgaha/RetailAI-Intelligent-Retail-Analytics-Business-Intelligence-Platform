import streamlit as st
from services.ai_service import chat

st.container()

html_header = f"""<div class="slide-up" style="padding-bottom: 1.5rem;"><h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.05em;">RetailAI Copilot</h1><p style="font-size: 1.15rem; color: var(--text-muted); max-width: 800px;">Your intelligent business consultant. Ask questions about the data warehouse, prediction models, or general retail strategies.</p></div>"""
st.markdown(html_header, unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I am your RetailAI Business Copilot. I can help you analyze your data, explain revenue predictions, and improve your retail strategy. How can I assist you today?"
    })

# Suggested Prompts (only show if history is just the welcome message)
if len(st.session_state.messages) == 1:
    st.markdown("### Suggested Prompts")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("What factors can increase order revenue?", use_container_width=True):
            st.session_state.preset_prompt = "What factors can increase order revenue based on our retail data model?"
        if st.button("Explain the revenue prediction model.", use_container_width=True):
            st.session_state.preset_prompt = "Explain how the Linear Regression revenue prediction model works and what R²=0.735 means."

    with col2:
        if st.button("How should we optimize discounts?", use_container_width=True):
            st.session_state.preset_prompt = "How should the business optimize discount levels to maximize revenue without eroding margins?"
        if st.button("How can sentiment improve performance?", use_container_width=True):
            st.session_state.preset_prompt = "How can customer sentiment analysis improve retail performance and customer retention?"

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle preset prompt injection
user_input = st.chat_input("Ask RetailAI a question...")
if "preset_prompt" in st.session_state and st.session_state.preset_prompt:
    user_input = st.session_state.preset_prompt
    st.session_state.preset_prompt = None

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("RetailAI Copilot is thinking..."):
            history_context = st.session_state.messages[:-1]
            response_text = chat(history_context, user_input)
        message_placeholder.markdown(response_text)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
