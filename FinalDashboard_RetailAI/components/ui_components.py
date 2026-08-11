import streamlit as st

def render_hero(title, subtitle, description):
    """Renders a business-centric SaaS hero banner."""
    html = f'<div class="hero-wrapper slide-up"><div class="hero-pill"><span>✨</span> Enterprise Retail Intelligence</div><h1 class="hero-title">{title}</h1><p class="hero-subtitle">{description}</p></div>'
    st.markdown(html, unsafe_allow_html=True)


def render_feature_card_html(title, description, icon, badge="Capability", delay_class="stagger-1"):
    """Returns HTML for a modern business feature card."""
    return f'<div class="feature-card-wrapper fade-in {delay_class}"><div><div class="feature-icon-box">{icon}</div><span class="feature-badge">{badge}</span><div class="feature-title">{title}</div><div class="feature-desc">{description}</div></div></div>'


# Alias for backward compatibility
def render_feature_card(title, description, icon, delay_class=""):
    """Backward compatible alias for render_feature_card_html."""
    return render_feature_card_html(title, description, icon, badge="Capability", delay_class=delay_class)


def render_workflow_step(step_num, title, description, icon):
    """Renders a single step in the business visual data workflow."""
    return f'<div class="flow-step-card"><div class="flow-step-number">{step_num}</div><div class="flow-step-icon">{icon}</div><div class="flow-step-title">{title}</div><div class="flow-step-desc">{description}</div></div>'


def render_value_card(title, description, icon):
    """Renders a key business benefit card."""
    return f'<div class="value-card"><div class="value-icon">{icon}</div><div class="value-title">{title}</div><div class="value-desc">{description}</div></div>'


def render_workflow_node(title, icon, is_last=False, is_highlight=False, delay_class=""):
    """Legacy workflow node helper maintained for backward compatibility."""
    highlight_cls = "highlight" if is_highlight else ""
    node_html = f'<div class="slide-right {delay_class} workflow-node {highlight_cls}"><div class="workflow-icon">{icon}</div><div class="workflow-text">{title}</div></div>'
    if not is_last:
        node_html += f'<div class="workflow-connector slide-right {delay_class}"></div>'
    return node_html


def render_tech_grid(tech_list, delay_class=""):
    """Legacy tech grid helper maintained for backward compatibility."""
    badges = "".join([f'<div class="tech-badge">{tech}</div>' for tech in tech_list])
    return f'<div class="fade-in {delay_class} tech-grid">{badges}</div>'


def render_interactive_launch_card(title, description, icon, link):
    """Renders an interactive launcher card for embedded Power BI reports."""
    return f'<a href="{link}" target="_blank" rel="noopener noreferrer" class="slide-up interactive-launch-card" aria-label="{title}"><div style="font-size: 3.5rem; margin-bottom: 1rem;">{icon}</div><h3 style="margin-top: 0; font-size: 1.75rem; font-weight: 700; color: white; margin-bottom: 0.5rem;">{title}</h3><p style="color: #93C5FD; font-size: 1.1rem; margin-bottom: 1.5rem;">{description}</p><div style="display: inline-block; background-color: var(--accent-primary); color: white; padding: 0.75rem 2rem; border-radius: 9999px; font-weight: 600; font-size: 1rem;">Launch Dashboard <span aria-hidden="true">→</span></div></a>'
