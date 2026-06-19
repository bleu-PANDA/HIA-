import streamlit as st
from auth.session_manager import SessionManager
from components.footer import show_footer
from config.app_config import ANALYSIS_DAILY_LIMIT

def show_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='margin-top:0; font-size:1.4rem; color: var(--primary-blue); font-family: var(--font-heading);'>🩺 HIA settings</h2>", unsafe_allow_html=True)
        
        # User details card inside sidebar
        if st.session_state.user:
            display_name = st.session_state.user.get("name") or st.session_state.user.get("email", "")
            display_email = st.session_state.user.get("email", "")
            st.markdown(
                f"""
                <div style="background: var(--bg-base); border: 1px solid var(--border-light); padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
                    <p style="margin: 0; font-weight: 600; color: var(--text-main); font-size: 0.9rem;">{display_name}</p>
                    <p style="margin: 0.2rem 0 0 0; color: var(--text-muted); font-size: 0.78rem; font-family: var(--font-body);">{display_email}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Daily quota indicator
        if 'analysis_count' not in st.session_state:
            st.session_state.analysis_count = 0
        
        remaining = ANALYSIS_DAILY_LIMIT - st.session_state.analysis_count
        st.markdown(
            f"""
            <div style='
                padding: 0.75rem 1rem;
                border-radius: 12px;
                background: rgba(37, 99, 235, 0.04);
                border: 1px solid rgba(37, 99, 235, 0.12);
                margin: 0.75rem 0;
                text-align: center;
            '>
                <p style='margin: 0; color: var(--text-muted); font-size: 0.72rem; font-weight: 600; letter-spacing: 0.05em;'>DAILY QUOTA LIMIT</p>
                <p style='
                    margin: 0.2rem 0 0 0;
                    color: {"#2563eb" if remaining > 3 else "#ef4444"};
                    font-weight: 600;
                    font-family: var(--font-heading);
                    font-size: 1.05rem;
                '>
                    {remaining} / {ANALYSIS_DAILY_LIMIT} runs left
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<hr style='margin: 1.5rem 0; border: 0; border-top: 1px solid var(--border-light);'>", unsafe_allow_html=True)
        
        # Logout action button
        if st.button("Logout", use_container_width=True, type="secondary"):
            SessionManager.logout()
            st.rerun()
        
        # Sidebar footer
        show_footer(in_sidebar=True)
