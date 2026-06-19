import streamlit as st
from auth.session_manager import SessionManager
from utils.icons import get_svg_icon, get_image_base64

def show_footer(in_sidebar=False):
    if in_sidebar:
        return

    # Footer Specific Styles for Card Layout and separators
    st.markdown("""
        <style>
            .footer-card-container {
                background: #ffffff !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 20px !important;
                padding: 2rem !important;
                margin-top: 4rem !important;
                margin-bottom: 2rem !important;
                box-shadow: 0 10px 40px -10px rgba(15, 23, 42, 0.02) !important;
            }
            
            .footer-card-container div[data-testid="stColumn"] {
                border-right: 1px solid #e2e8f0 !important;
                padding-left: 1.5rem !important;
                padding-right: 1.5rem !important;
            }
            
            .footer-card-container div[data-testid="stColumn"]:first-of-type {
                padding-left: 0 !important;
            }
            
            .footer-card-container div[data-testid="stColumn"]:last-of-type {
                border-right: none !important;
                padding-right: 0 !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: center !important;
                align-items: flex-end !important;
                text-align: right !important;
            }
            
            /* Style footer buttons as text links with hover effect */
            .footer-card-container button {
                background: transparent !important;
                border: none !important;
                color: #475569 !important;
                text-align: left !important;
                padding: 0 !important;
                margin: 0 !important;
                font-size: 0.85rem !important;
                font-family: var(--font-body) !important;
                box-shadow: none !important;
                display: flex !important;
                align-items: center !important;
                gap: 8px !important;
                height: auto !important;
                min-height: 0 !important;
                line-height: 1.8 !important;
                cursor: pointer !important;
            }
            .footer-card-container button:hover {
                color: #2563eb !important;
                text-decoration: underline !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="footer-card-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1.5, 1.0, 1.0, 1.0, 1.0])

    # Col 1: Brand Logo & Tagline
    with col1:
        stethoscope_img = get_image_base64("src/static/stethoscope.webp")
        st.markdown(
            f"""
            <div style="
            font-family:var(--font-heading);
            font-size:1.25rem;
            font-weight:700;
            color:#0f172a;
            margin-bottom:0.75rem;
            display:flex;
            align-items:center;
            gap:8px;
            ">

            <img src="{stethoscope_img}"
            style="
            width:22px;
            height:22px;
            object-fit:contain;
            ">

            <span>HIA</span>

            </div>
            <p style="color: #64748b; font-size: 0.82rem; line-height: 1.5; font-family: var(--font-body); margin: 0; padding-right: 1rem;">
                AI-powered health intelligence that understands your reports and empowers your health decisions.
            </p>
            """,
            unsafe_allow_html=True
        )

    # Col 2: Account actions (Profile, Logout)
    with col2:
        st.markdown(
            """
            <div style="font-family: var(--font-heading); font-size: 0.88rem; font-weight: 700; color: #0f172a; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">
                Account
            </div>
            """,
            unsafe_allow_html=True
        )
        if SessionManager.is_authenticated():
            # if st.button("👤 Profile", key="footer_profile_btn", use_container_width=True):
            #     st.session_state.show_profile = True
            #     st.rerun()
            st.markdown("<div style='margin-top: 0.25rem;'></div>", unsafe_allow_html=True)
            if st.button("-> Logout", key="footer_logout_btn"):
                SessionManager.logout()
                st.rerun()
        else:
            st.markdown("<p style='color: #94a3b8; font-size: 0.82rem; font-family: var(--font-body); margin: 0;'>Sign in required</p>", unsafe_allow_html=True)

    # Col 3: Security Certifications
    with col3:
        shield_svg = get_svg_icon("ShieldCheck", size=14, color="#2563eb", extra_style="vertical-align: middle; margin-right: 6px;")
        lock_svg = get_svg_icon("Lock", size=14, color="#2563eb", extra_style="vertical-align: middle; margin-right: 6px;")
        st.markdown(
            f"""
            <div style="font-family: var(--font-heading); font-size: 0.88rem; font-weight: 700; color: #0f172a; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">
                Security
            </div>
            <div style="font-family: var(--font-body); font-size: 0.85rem; color: #475569; display: flex; flex-direction: column; gap: 8px;">
                <span style="display: flex; align-items: center;">{shield_svg}HIPAA Compliant</span>
                <span style="display: flex; align-items: center;">{lock_svg}Data Encryption</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Col 4: Support links
    with col4:
        mail_svg = get_svg_icon("Mail", size=14, color="#2563eb", extra_style="vertical-align: middle; margin-right: 6px;")
        shield_small_svg = get_svg_icon("Shield", size=14, color="#2563eb", extra_style="vertical-align: middle; margin-right: 6px;")
        st.markdown(
            f"""
            <div style="font-family: var(--font-heading); font-size: 0.88rem; font-weight: 700; color: #0f172a; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">
                Support
            </div>
            <div style="font-family: var(--font-body); font-size: 0.85rem; color: #475569; display: flex; flex-direction: column; gap: 8px;">
                <a href="#" style="color: #475569; text-decoration: none; display: flex; align-items: center;">{mail_svg}Contact Us</a>
                <a href="#" style="color: #475569; text-decoration: none; display: flex; align-items: center;">{shield_small_svg}Privacy Policy</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Col 5: Copyright text
    with col5:
        st.markdown(
            """
            <div style="font-family: var(--font-body); font-size: 0.82rem; color: #94a3b8; line-height: 1.5;">
                <div>© 2026 HIA</div>
                <div>All rights reserved.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)
