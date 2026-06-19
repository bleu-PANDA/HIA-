import streamlit as st
from auth.session_manager import SessionManager
from config.app_config import APP_ICON, APP_NAME, APP_TAGLINE, APP_DESCRIPTION
from utils.validators import validate_signup_fields
from utils.icons import get_svg_icon, get_image_base64
import time

def show_login_page():
    if 'form_type' not in st.session_state:
        st.session_state['form_type'] = 'login'
    
    current_form = st.session_state['form_type']

    # Inject page marker and configuration CSS
    st.markdown('<div class="login-wrapper"></div>', unsafe_allow_html=True)
    st.markdown("""
        <style>
            div[data-testid="InputInstructions"] > span:nth-child(1) {
                visibility: hidden;
            }
            
            /* Remove padding for login page */
            .stApp:has(.login-wrapper) div[data-testid="stAppViewBlockContainer"] {
                padding: 0px !important;
                max-width: 100% !important;
            }
            .stApp:has(.login-wrapper) header {
                display: none !important;
            }
            .stApp:has(.login-wrapper) footer {
                display: none !important;
            }
            .stApp:has(.login-wrapper) [data-testid="stSidebar"] {
                display: none !important;
            }
            .stApp:has(.login-wrapper) [data-testid="stSidebarCollapsedControl"] {
                display: none !important;
            }
            
            /* Force white/light backgrounds */
            # .stApp:has(.login-wrapper) {
            #     background-color: #ffffff !important;
            #     background-image: none !important;
            # }
              .stApp:has(.login-wrapper) {
                  background-color: #C8DCFF !important;
                  background-image: none !important;
              }
            
            /* Split container layout */
            .stApp:has(.login-wrapper) div[data-testid="stHorizontalBlock"] {
                gap: 0px !important;
                # min-height: 100vh;
                height: auto !important;
                min-height: 575px !important;
            }
            
            .stApp:has(.login-wrapper) div[data-testid="stColumn"]:nth-of-type(1) {
                background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%) !important;
                border-right: 1px solid var(--border-light) !important;
                # padding: 4rem 5rem !important;
                # min-height: 100vh;
                padding: 2rem 3rem !important;
                height: auto !important;
                min-height: unset !important;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            .stApp:has(.login-wrapper) div[data-testid="stColumn"]:nth-of-type(2) {
                background-color: #f8fafc !important;
                # padding: 4rem !important;
                # min-height: 100vh;
                padding: 0.5rem !important;
                height: auto !important;
                min-height: unset !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }
            
            /* Login/Signup Card */
            .stApp:has(.login-wrapper) div[data-testid="stColumn"]:nth-of-type(2) > div {
                background: #ffffff !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 20px !important;
                padding: 1.15rem !important;
                box-shadow: 0 10px 40px -10px rgba(15, 23, 42, 0.05) !important;
                width: 100% !important;
                max-width: 460px !important;
            }
            
            /* Hide inner form card styles */
            .stApp:has(.login-wrapper) div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stForm"] {
                border: none !important;
                background: transparent !important;
                padding: 0 !important;
                box-shadow: none !important;
            }
            
            /* Inputs inside card */
            .stApp:has(.login-wrapper) input[placeholder="you@example.com"] {
                padding-left: 2.75rem !important;
                background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>') !important;
                background-repeat: no-repeat !important;
                background-position: 14px center !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 10px !important;
                height: 42px !important;
                line-height: 42px !important;
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                font-family: var(--font-body) !important;
            }
            
            .stApp:has(.login-wrapper) input[type="password"] {
                padding-left: 2.75rem !important;
                padding-right: 2.75rem !important;
                background-image: 
                    url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'),
                    url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>') !important;
                background-repeat: no-repeat, no-repeat !important;
                background-position: 14px center, right 14px center !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 10px !important;
                height: 42px !important;
                line-height: 42px !important;
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                font-family: var(--font-body) !important;
            }
            
            .stApp:has(.login-wrapper) input[placeholder="John Doe"] {
                padding-left: 2.75rem !important;
                background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>') !important;
                background-repeat: no-repeat !important;
                background-position: 14px center !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 10px !important;
                height: 42px !important;
                font-family: var(--font-body) !important;
            }
            
            /* Primary button */
            .stApp:has(.login-wrapper) button[data-testid="stBaseButton-primary"] {
                background: #2563eb !important;
                color: #ffffff !important;
                border-radius: 10px !important;
                height: 48px !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                box-shadow: none !important;
                border: none !important;
                transition: background-color 0.2s ease !important;
                width: 100% !important;
            }
            .stApp:has(.login-wrapper) button[data-testid="stBaseButton-primary"]:hover {
                background-color: #1d4ed8 !important;
            }
            
            /* Secondary button (signup toggle) */
            .stApp:has(.login-wrapper) button[data-testid="stBaseButton-secondary"] {
                background: #ffffff !important;
                color: #2563eb !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 10px !important;
                height: 48px !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                box-shadow: none !important;
                transition: background-color 0.2s ease !important;
                width: 100% !important;
            }
            .stApp:has(.login-wrapper) button[data-testid="stBaseButton-secondary"]:hover {
                background-color: #f8fafc !important;
                border-color: #cbd5e1 !important;
            }

            .stApp:has(.login-wrapper) .stTextInput input {
                height: 48px !important;
                line-height: 48px !important;
            }

            .stApp:has(.login-wrapper) .stTextInput div[data-baseweb="input"] {
                align-items: center !important;
            }

            .stApp:has(.login-wrapper) div[data-testid="stHorizontalBlock"] {
                max-width: 1520px !important;
                max-height: 80vh !important;
                # margin: 50px auto !important;
                transform: translateY(60px);
                margin: -17px auto !important;
                border-radius: 24px !important;
                overflow: hidden !important;
            }

            .stApp:has(.login-wrapper) {
                height: 100vh !important;
                overflow: hidden !important;
            }

            .stApp:has(.login-wrapper) .main {
                height: 100vh !important;
                overflow: hidden !important;
            }

            .stApp:has(.login-wrapper) section.main > div {
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                height: 100vh !important;
            }

            /* Compress vertical spacing between form elements */
            .stApp:has(.login-wrapper) div[data-testid="stVerticalBlock"] > div {
                margin-bottom: -0.55rem !important;
            }

            # /* Reduce spacing below labels */
            # .stApp:has(.login-wrapper) label {
            #     margin-bottom: -0.3rem !important;
            # }

            /* Pull the form upward */
            .stApp:has(.login-wrapper) div[data-testid="stForm"] {
                margin-top: -0.8rem !important;
            }

            /* Reduce gap around text inputs slightly */
            .stApp:has(.login-wrapper) .stTextInput {
                margin-top: -0.15rem !important;
                margin-bottom: -0.15rem !important;
            }

            /* Reduce gap between labels and textboxes */
            .stApp:has(.login-wrapper) div[data-testid="stWidgetLabel"] {
                margin-bottom: -0.3rem !important;
            }

        </style>
    """, unsafe_allow_html=True)

    # Load sculpture base64
    sculpture_b64 = get_image_base64("src/static/edited-photo-Photoroom.png")
    
    col_left, col_right = st.columns([1.5, 1.0])
    
    with col_left:
        # stethoscope_svg = get_svg_icon("Stethoscope", size=22, color="#2563eb", extra_style="vertical-align: middle; margin-right: 8px;")
        stethoscope_img = get_image_base64("src/static/stethoscope.webp")
        shield_icon = get_svg_icon("ShieldCheck", size=18, color="#2563eb", extra_style="vertical-align: middle; margin-right: 8px;")
        
        # HTML structure mimicking the split pane
        sculpture_img_html = ""
        if sculpture_b64:
#             sculpture_img_html = f"""<div style="flex: 1; display: flex; justify-content: center; align-items: center; padding-left: 2rem;">
# <img src="{sculpture_b64}" style="max-width: 100%; max-height: 600px; object-fit: contain; filter: drop-shadow(0 15px 35px rgba(37, 99, 235, 0.08));">
# </div>"""
              sculpture_img_html = f"""
<div style="
flex:1;
align-self:stretch;
position:relative;
margin-right:-3rem;
# overflow:hidden;
background:red;
">

<img src="{sculpture_b64}"
style="
position:absolute;
right:-48px;
top:60%;
transform:translateY(-56%);
height:100%;
width:auto;
filter:drop-shadow(0 15px 35px rgba(37,99,235,0.08));
">

</div>
"""

# <div style="
# flex:1;
# align-self:stretch;
# display:flex;
# justify-content:center;
# align-items:center;
# margin-right:-3rem;
# margin-left:-6rem;
# overflow:hidden;
# ">

# <img src="{sculpture_b64}"
# style="
# width:auto;
# height:auto;
# object-fit:contain;
# filter:drop-shadow(0 15px 35px rgba(37,99,235,0.08));
# ">

# </div>
# """

# <div style="
# flex:1;
# align-self:stretch;
# background:red;
# display:flex;
# justify-content:center;
# align-items:center;
# margin-right:-3rem;
# margin-left:-4rem;
# ">
# HELLO
# </div>
# """
        
        # Keep multi-line string aligned to column 0 to prevent raw HTML rendering
        left_panel_html = f"""
<div style="
display:flex;
flex-direction:row;
justify-content:space-between;
align-items:stretch;
height:100%;
min-height:500px;
width:100%;
">

<div style="flex: 1.2; display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 500px;">

<!-- Logo -->
<div style="
display:flex;
align-items:center;
gap:10px;
font-family:var(--font-heading);
font-size:1.6rem;
font-weight:700;
color:#0f172a;
margin-bottom:2rem;
">

<img src="{stethoscope_img}"
style="
width:28px;
height:28px;
object-fit:contain;
">

<span style="
font-weight:1000;
letter-spacing:-0.6px;
">
    HIA
</span>

</div>

<!-- Content -->
<div style="margin-top: auto; margin-bottom: auto;">

<h1 style="font-size: 3.8rem; font-weight: 800; line-height: 1.1; color: #0f172a; margin-top: -40px; margin-bottom: 1.5rem; font-family: var(--font-heading); letter-spacing: -0.04em;">
Your medical<br>reports.<br>
<span style="color: #2563eb;">Translated.</span>
</h1>

<p style="color: #475569; font-size: 1.1rem; line-height: 1.6; max-width: 440px; font-family: var(--font-body); margin-bottom: 0;">
Upload any blood test or clinical report PDF. Our health AI deciphers raw laboratory values into clear, readable summaries and answers follow-up questions in real time.
</p>

</div>

<!-- Bottom HIPAA info -->
<div style="display: flex; align-items: center; color: #2563eb; font-weight: 600; font-size: 0.92rem; font-family: var(--font-heading); margin-top: 2rem;">
{shield_icon}
HIPAA-compliant data encryption
</div>

</div>

{sculpture_img_html}

</div>
"""

        st.markdown(left_panel_html, unsafe_allow_html=True)


#          left_panel_html = f"""<div style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; height: 100%; min-height: 520px; width: 100%;">
# <div style="flex: 1.2; display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 520px;">
# <!-- Logo -->
# <div style="display: flex; align-items: center; font-family: var(--font-heading); font-size: 1.6rem; font-weight: 700; color: #0f172a; margin-bottom: 2rem;">
# {stethoscope_svg}HIA
# </div>
# <!-- Content -->
# <div style="margin-top: auto; margin-bottom: auto;">
# <h1 style="font-size: 3.8rem; font-weight: 800; line-height: 1.1; color: #0f172a; margin-bottom: 1.5rem; font-family: var(--font-heading); letter-spacing: -0.04em;">
# Your medical<br>reports.<br><span style="color: #2563eb;">Translated.</span>
# </h1>
# <p style="color: #475569; font-size: 1.1rem; line-height: 1.6; max-width: 440px; font-family: var(--font-body); margin-bottom: 0;">
# Upload any blood test or clinical report PDF. Our health AI deciphers raw laboratory values into clear, readable summaries and answers follow-up questions in real time.
# </p>
# </div>
# <!-- Bottom HIPAA info -->
# <div style="display: flex; align-items: center; color: #2563eb; font-weight: 600; font-size: 0.92rem; font-family: var(--font-heading); margin-top: 2rem;">
# {shield_icon}HIPAA-compliant data encryption
# </div>
# </div>
# {sculpture_img_html}
#  </div>"""

        #  left_panel_html = f"""
        #  <div style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; height: 100%; min-height: 520px; width: 100%;">

        #  <div style="flex: 1.2; display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 520px;">

        #  <!-- Logo -->
        #  <div style="display: flex; align-items: center; font-family: var(--font-heading); font-size: 1.6rem; font-weight: 700; color: #0f172a; margin-bottom: 2rem;">
        #  {stethoscope_svg}HIA
        #  </div>

        #  <!-- Content -->
        #  <div style="margin-top: auto; margin-bottom: auto;">

        #  <h1 style="font-size: 3.8rem; font-weight: 800; line-height: 1.1; color: #0f172a; margin-bottom: 1.5rem; font-family: var(--font-heading); letter-spacing: -0.04em;">
        #  Your medical<br>reports.<br>
        #  <span style="color: #2563eb;">Translated.</span>
        #  </h1>

        #  <p style="color: #475569; font-size: 1.1rem; line-height: 1.6; max-width: 440px; font-family: var(--font-body); margin-bottom: 0;">
        #  Upload any blood test or clinical report PDF. Our health AI deciphers raw laboratory values into clear, readable summaries and answers follow-up questions in real time.
        #  </p>

        #  </div>

        #  <!-- Bottom HIPAA info -->
        #  <div style="display: flex; align-items: center; color: #2563eb; font-weight: 600; font-size: 0.92rem; font-family: var(--font-heading); margin-top: 2rem;">
        #  {shield_icon}
        #  HIPAA-compliant data encryption
        #  </div>

        #  </div>

        #  <!-- IMAGE REMOVED FOR TEST -->

        #  </div>
        #  """           

        # # left_panel_html = f"""
        # # <h1 style="font-size: 3.8rem; font-weight: 800; line-height: 1.1; color: #0f172a; margin-bottom: 1.5rem; font-family: var(--font-heading); letter-spacing: -0.04em;">
        # # Your medical<br>reports.<br>
        # # <span style="color: #2563eb;">Translated.</span>
        # # </h1>
        # # <p style="color: #475569; font-size: 1.1rem; line-height: 1.6; max-width: 440px;">
        # # Upload any blood test or clinical report PDF.
        # # Our health AI deciphers raw laboratory values into clear,
        # # readable summaries and answers follow-up questions in real time.
        # # </p>
        # # <div style="display: flex; align-items: center; color: #2563eb; font-weight: 600; font-size: 0.92rem; font-family: var(--font-heading); margin-top: 2rem;">
        # # {shield_icon}HIPAA-compliant data encryption
        # # </div>
        # # """

        #  st.markdown(left_panel_html, unsafe_allow_html=True)
        # # st.code(left_panel_html)
        
    with col_right:
        if current_form == 'login':
            show_login_form()
            
            # Divider "or"
            divider_html = """<div style="display: flex; align-items: center; text-align: center; margin: 0.75rem 0; color: #cbd5e1; width: 100%;">
    <div style="flex-grow: 1; border-top: 1px solid #e2e8f0;"></div>
    <span style="padding: 0 10px; font-size: 0.82rem; color: #94a3b8; font-family: var(--font-body);">or</span>
    <div style="flex-grow: 1; border-top: 1px solid #e2e8f0;"></div>
</div>"""
            st.markdown(divider_html, unsafe_allow_html=True)
            
            # Toggle button
            if st.button("Don't have an account? Sign up", key="toggle_to_signup", use_container_width=True, type="secondary"):
                st.session_state['form_type'] = 'signup'
                st.rerun()
        else:
            show_signup_form()
            
            # Divider "or"
            divider_html = """<div style="display: flex; align-items: center; text-align: center; margin: 1.25rem 0; color: #cbd5e1; width: 100%;">
    <div style="flex-grow: 1; border-top: 1px solid #e2e8f0;"></div>
    <span style="padding: 0 10px; font-size: 0.82rem; color: #94a3b8; font-family: var(--font-body);">or</span>
    <div style="flex-grow: 1; border-top: 1px solid #e2e8f0;"></div>
</div>"""
            st.markdown(divider_html, unsafe_allow_html=True)
            
            # Toggle button
            if st.button("Already have an account? Login", key="toggle_to_login", use_container_width=True, type="secondary"):
                st.session_state['form_type'] = 'login'
                st.rerun()

def show_login_form():
    with st.form("login_form"):
        heading_html = """<div style="text-align: center; margin-bottom: 2rem;">
    <h2 style="margin: 0; margin-top: 3rem; font-size: 1.8rem; color: #0f172a; font-family: var(--font-heading); font-weight: 700;">Welcome</h2>
    <p style="color: #64748b; font-size: 0.88rem; margin-bottom: 3rem; margin-top: 0rem; font-family: var(--font-body);">
        Enter your credentials to access your health workspace
    </p>
</div>"""
        st.markdown(heading_html, unsafe_allow_html=True)
        
        email = st.text_input("Email", key="login_email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        
        # Forgot password right-aligned link
        forgot_html = """<div style="text-align: right; margin-top: -0.5rem; margin-bottom: 1.25rem;">
    <a href="#" style="font-size: 0.82rem; color: #2563eb; text-decoration: none; font-family: var(--font-body); font-weight: 600;">
        Forgot password?
    </a>
</div>"""
        st.markdown(forgot_html, unsafe_allow_html=True)
        
        if st.form_submit_button("Enter Workspace \u2192", use_container_width=True, type="primary"):
            if email and password:
                success, result = SessionManager.login(email, password)
                if success:
                    st.rerun()
                else:
                    st.error(f"Login failed: {result}")
            else:
                st.error("Please enter both email and password")

def show_signup_form():
    with st.form("signup_form"):
#         heading_html = """<div style="text-align: center; margin-bottom: 0rem;">
#     <h2 style="margin: 0; font-size: 1.4rem; color: #0f172a; font-family: var(--font-heading); font-weight: 700;">Create Account</h2>
#     <p style="color: #64748b; font-size: 0.88rem; margin-top: 0.4rem; font-family: var(--font-body);">
#         Sign up to start analyzing health reports
#     </p>
# </div>"""
#         heading_html = """<div style="text-align: center; margin-bottom: -0.4rem;">
# <h2 style="
# margin:0;
# font-size:1.4rem;
# color:#0f172a;
# font-family:var(--font-heading);
# font-weight:700;
# ">
# Create Account
# </h2>

# <p style="
# color:#64748b;
# font-size:0.88rem;
# margin-top:0.1rem;
# margin-bottom:0;
# font-family:var(--font-body);
# ">
# Sign up to start analyzing health reports
# </p>
# </div>"""
        heading_html = """
<div style="text-align:center; margin-bottom: 1.25rem;">

<h2 style="
margin:0;
padding:0;
line-height:1.1;
margin-top:1.7rem;
font-size:1.4rem;
color:#0f172a;
font-family:var(--font-heading);
font-weight:700;
">
Create Account
</h2>

</div>
"""
        st.markdown(heading_html, unsafe_allow_html=True)
        
        new_name = st.text_input("Full Name", key="signup_name", placeholder="John Doe")
        new_email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
        new_password = st.text_input("Password", type="password", key="signup_password", placeholder="Min. 8 characters")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_password2", placeholder="Confirm password")
        
#         requirements_html = """<div style="background: rgba(37, 99, 235, 0.02); border: 1px solid var(--border-light); padding: 0.5rem; border-radius: 12px; font-size: 0.8rem; margin: 0.5rem 0;">
#     <strong style="color: var(--text-main); font-family: var(--font-heading);">Password requirements:</strong>
#     <ul style="margin: 0.4rem 0 0 0; padding-left: 1.2rem; color: var(--text-muted); line-height: 1.4; font-family: var(--font-body);">
#         <li>At least 8 characters</li>
#         <li>One uppercase letter (A-Z)</li>
#         <li>One lowercase letter (a-z)</li>
#         <li>One numerical digit (0-9)</li>
#     </ul>
# </div>"""
        requirements_html = """
<div style="
background: rgba(37,99,235,0.03);
border:1px solid #e2e8f0;
padding:0.4rem 0.7rem;
border-radius:10px;
font-size:0.72rem;
margin:0.3rem 0;
line-height:1.25;
color:#64748b;
">
<b>Password requirements:</b><br>
• 8 characters   • A-Z   • a-z   • 0-9
</div>
"""
        st.markdown(requirements_html, unsafe_allow_html=True)
        
        if st.form_submit_button("Create Account", use_container_width=True, type="primary"):
            validation_result = validate_signup_fields(
                new_name, new_email, new_password, confirm_password
            )
            
            if not validation_result[0]:
                st.error(validation_result[1])
                return
            
            success, response = st.session_state.auth_service.sign_up(
                new_email, new_password, new_name
            )
            
            if success:
                st.session_state.authenticated = True
                st.session_state.user = response
                st.rerun()
            else:
                st.error(f"Sign up failed: {response}")





# import streamlit as st
# from auth.session_manager import SessionManager
# from config.app_config import APP_ICON, APP_NAME, APP_TAGLINE, APP_DESCRIPTION
# from utils.validators import validate_signup_fields
# from utils.icons import get_svg_icon, get_image_base64
# import time

# def show_login_page():
#     if 'form_type' not in st.session_state:
#         st.session_state['form_type'] = 'login'
    
#     current_form = st.session_state['form_type']

#     # Inject page marker and configuration CSS
#     st.markdown('<div class="login-wrapper"></div>', unsafe_allow_html=True)
#     st.markdown("""
#         <style>
#             div[data-testid="InputInstructions"] > span:nth-child(1) {
#                 visibility: hidden;
#             }
            
#             /* Remove padding for login page */
#             .stApp:has(.login-wrapper) div[data-testid="stAppViewBlockContainer"] {
#                 padding: 0px !important;
#                 max-width: 100% !important;
#                 height: 100vh !important;
#                 display: flex !important;
#                 align-items: center !important;
#                 justify-content: center !important;
#                 overflow: hidden !important;
#                 background-color: #C8DCFF !important;
#             }
#             .stApp:has(.login-wrapper) header {
#                 display: none !important;
#             }
#             .stApp:has(.login-wrapper) footer {
#                 display: none !important;
#             }
#             .stApp:has(.login-wrapper) [data-testid="stSidebar"] {
#                 display: none !important;
#             }
#             .stApp:has(.login-wrapper) [data-testid="stSidebarCollapsedControl"] {
#                 display: none !important;
#             }
            
#             .stApp:has(.login-wrapper) {
#                 background-color: #C8DCFF !important;
#                 background-image: none !important;
#                 height: 100vh !important;
#                 overflow: hidden !important;
#             }
            
#             .stApp:has(.login-wrapper) .main {
#                 height: 100vh !important;
#                 overflow: hidden !important;
#                 background-color: #C8DCFF !important;
#             }

#             .stApp:has(.login-wrapper) section.main > div {
#                 padding: 0px !important;
#                 height: 100vh !important;
#                 display: flex !important;
#                 align-items: center !important;
#                 justify-content: center !important;
#                 overflow: hidden !important;
#             }
            
#             /* Center columns block and size it nicely */
#             .stApp:has(.login-wrapper) div[data-testid="stHorizontalBlock"] {
#                 gap: 0px !important;
#                 width: 90% !important;
#                 max-width: 1180px !important;
#                 height: 560px !important;
#                 background-color: #ffffff !important;
#                 border-radius: 24px !important;
#                 box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08) !important;
#                 overflow: hidden !important;
#                 display: flex !important;
#                 flex-direction: row !important;
#                 margin: 0 auto !important;
#             }
            
#             /* Make columns and their inner blocks fill the parent height */
#             .stApp:has(.login-wrapper) div[data-testid="stColumn"] {
#                 height: 100% !important;
#                 min-height: 100% !important;
#                 margin: 0 !important;
#             }
#             .stApp:has(.login-wrapper) div[data-testid="stColumn"] > div {
#                 height: 100% !important;
#                 min-height: 100% !important;
#             }
#             .stApp:has(.login-wrapper) div[data-testid="stColumn"] [data-testid="stVerticalBlock"] {
#                 height: 100% !important;
#                 min-height: 100% !important;
#             }
            
#             .stApp:has(.login-wrapper) div[data-testid="stColumn"]:nth-of-type(1) {
#                 background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%) !important;
#                 border-right: 1px solid #e2e8f0 !important;
#                 padding: 3rem 3.5rem !important;
#                 height: 100% !important;
#                 display: flex !important;
#                 flex-direction: column !important;
#                 justify-content: center !important;
#                 position: relative !important;
#                 overflow: hidden !important;
#             }
            
#             .stApp:has(.login-wrapper) div[data-testid="stColumn"]:nth-of-type(2) {
#                 background-color: #f8fafc !important;
#                 padding: 2rem !important;
#                 height: 100% !important;
#                 display: flex !important;
#                 align-items: center !important;
#                 justify-content: center !important;
#             }
            
#             /* Login/Signup Card */
#             .stApp:has(.login-wrapper) div[data-testid="stColumn"]:nth-of-type(2) > div {
#                 background: #ffffff !important;
#                 border: 1px solid #cbd5e1 !important;
#                 border-radius: 24px !important;
#                 padding: 2.25rem 2.5rem !important;
#                 box-shadow: 0 10px 40px -10px rgba(15, 23, 42, 0.04) !important;
#                 width: 100% !important;
#                 max-width: 410px !important;
#                 display: flex !important;
#                 flex-direction: column !important;
#                 justify-content: center !important;
#                 box-sizing: border-box !important;
#             }
            
#             /* Hide inner form card styles */
#             .stApp:has(.login-wrapper) div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stForm"] {
#                 border: none !important;
#                 background: transparent !important;
#                 padding: 0 !important;
#                 box-shadow: none !important;
#             }
            
#             /* Inputs inside card */
#             .stApp:has(.login-wrapper) input[placeholder="you@example.com"] {
#                 padding-left: 2.75rem !important;
#                 background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>') !important;
#                 background-repeat: no-repeat !important;
#                 background-position: 14px center !important;
#                 border: 1px solid #cbd5e1 !important;
#                 border-radius: 10px !important;
#                 height: 48px !important;
#                 line-height: 48px !important;
#                 padding-top: 0 !important;
#                 padding-bottom: 0 !important;
#                 font-family: var(--font-body) !important;
#             }
            
#             .stApp:has(.login-wrapper) input[type="password"] {
#                 padding-left: 2.75rem !important;
#                 padding-right: 2.75rem !important;
#                 background-image: 
#                     url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'),
#                     url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>') !important;
#                 background-repeat: no-repeat, no-repeat !important;
#                 background-position: 14px center, right 14px center !important;
#                 border: 1px solid #cbd5e1 !important;
#                 border-radius: 10px !important;
#                 height: 48px !important;
#                 line-height: 48px !important;
#                 padding-top: 0 !important;
#                 padding-bottom: 0 !important;
#                 font-family: var(--font-body) !important;
#             }
            
#             .stApp:has(.login-wrapper) input[placeholder="John Doe"] {
#                 padding-left: 2.75rem !important;
#                 background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>') !important;
#                 background-repeat: no-repeat !important;
#                 background-position: 14px center !important;
#                 border: 1px solid #cbd5e1 !important;
#                 border-radius: 10px !important;
#                 height: 48px !important;
#                 font-family: var(--font-body) !important;
#             }
            
#             /* Primary button */
#             .stApp:has(.login-wrapper) button[data-testid="stBaseButton-primary"] {
#                 background: #2563eb !important;
#                 color: #ffffff !important;
#                 border-radius: 10px !important;
#                 height: 48px !important;
#                 font-weight: 600 !important;
#                 font-size: 1rem !important;
#                 box-shadow: none !important;
#                 border: none !important;
#                 transition: background-color 0.2s ease !important;
#                 width: 100% !important;
#             }
#             .stApp:has(.login-wrapper) button[data-testid="stBaseButton-primary"]:hover {
#                 background-color: #1d4ed8 !important;
#             }
            
#             /* Secondary button (signup toggle) */
#             .stApp:has(.login-wrapper) button[data-testid="stBaseButton-secondary"] {
#                 background: #ffffff !important;
#                 color: #2563eb !important;
#                 border: 1px solid #cbd5e1 !important;
#                 border-radius: 10px !important;
#                 height: 48px !important;
#                 font-weight: 600 !important;
#                 font-size: 0.95rem !important;
#                 box-shadow: none !important;
#                 transition: background-color 0.2s ease !important;
#                 width: 100% !important;
#             }
#             .stApp:has(.login-wrapper) button[data-testid="stBaseButton-secondary"]:hover {
#                 background-color: #f8fafc !important;
#                 border-color: #cbd5e1 !important;
#             }

#             .stApp:has(.login-wrapper) .stTextInput input {
#                 height: 48px !important;
#                 line-height: 48px !important;
#             }

#             .stApp:has(.login-wrapper) .stTextInput div[data-baseweb="input"] {
#                 align-items: center !important;
#             }
#         </style>
#     """, unsafe_allow_html=True)

#     # Load sculpture base64
#     sculpture_b64 = get_image_base64("src/static/sculpture.png")
    
#     col_left, col_right = st.columns([1.5, 1.0])
    
#     with col_left:
#         stethoscope_svg = get_svg_icon("Stethoscope", size=28, color="#2563eb", extra_style="margin-right: 10px; flex-shrink: 0;")
#         shield_icon = get_svg_icon("ShieldCheck", size=18, color="#2563eb", extra_style="margin-right: 8px; flex-shrink: 0;")
        
#         sculpture_img_html = ""
#         if sculpture_b64:
#             sculpture_img_html = f"""
# <div style="position: absolute; right: 0px; bottom: 0px; top: 0px; width: 44%; display: flex; align-items: flex-end; justify-content: flex-end; z-index: 1; pointer-events: none;">
#     <img src="{sculpture_b64}"
#          style="
#             width: 100%;
#             height: 100%;
#             object-fit: contain;
#             object-position: right bottom;
#             filter: drop-shadow(0 15px 35px rgba(37,99,235,0.08));
#          ">
# </div>
# """
        
#         # Left panel layout centering content with z-index above the absolute sculpture image
#         left_panel_html = f"""
# <div style="display: flex; flex-direction: column; justify-content: center; height: 100%; width: 100%; position: relative;">

#     <!-- Logo -->
#     <div style="display: flex; align-items: center; font-family: var(--font-heading); font-size: 1.6rem; font-weight: 700; color: #0f172a; margin-bottom: 2.5rem; z-index: 2;">
#         {stethoscope_svg}HIA
#     </div>

#     <!-- Content -->
#     <div style="max-width: 56%; z-index: 2; margin-bottom: 2rem;">
#         <h1 style="font-size: 3.4rem; font-weight: 800; line-height: 1.1; color: #0f172a; margin-bottom: 1.25rem; font-family: var(--font-heading); letter-spacing: -0.04em;">
#             Your medical<br>reports.<br>
#             <span style="color: #2563eb;">Translated.</span>
#         </h1>
#         <p style="color: #475569; font-size: 1.05rem; line-height: 1.5; font-family: var(--font-body); margin: 0;">
#             Upload any blood test or clinical report PDF. Our health AI deciphers raw laboratory values into clear, readable summaries and answers follow-up questions in real time.
#         </p>
#     </div>

#     <!-- Bottom HIPAA info -->
#     <div style="display: flex; align-items: center; color: #2563eb; font-weight: 600; font-size: 0.92rem; font-family: var(--font-heading); z-index: 2;">
#         {shield_icon}
#         <span>HIPAA-compliant data encryption</span>
#     </div>

#     {sculpture_img_html}

# </div>
# """
#         st.markdown(left_panel_html, unsafe_allow_html=True)
        
#     with col_right:
#         if current_form == 'login':
#             show_login_form()
            
#             # Divider "or"
#             divider_html = """<div style="display: flex; align-items: center; text-align: center; margin: 0.75rem 0; color: #cbd5e1; width: 100%;">
#     <div style="flex-grow: 1; border-top: 1px solid #e2e8f0;"></div>
#     <span style="padding: 0 10px; font-size: 0.82rem; color: #94a3b8; font-family: var(--font-body);">or</span>
#     <div style="flex-grow: 1; border-top: 1px solid #e2e8f0;"></div>
# </div>"""
#             st.markdown(divider_html, unsafe_allow_html=True)
            
#             # Toggle button
#             if st.button("Don't have an account? Sign up", key="toggle_to_signup", use_container_width=True, type="secondary"):
#                 st.session_state['form_type'] = 'signup'
#                 st.rerun()
#         else:
#             show_signup_form()
            
#             # Divider "or"
#             divider_html = """<div style="display: flex; align-items: center; text-align: center; margin: 1.25rem 0; color: #cbd5e1; width: 100%;">
#     <div style="flex-grow: 1; border-top: 1px solid #e2e8f0;"></div>
#     <span style="padding: 0 10px; font-size: 0.82rem; color: #94a3b8; font-family: var(--font-body);">or</span>
#     <div style="flex-grow: 1; border-top: 1px solid #e2e8f0;"></div>
# </div>"""
#             st.markdown(divider_html, unsafe_allow_html=True)
            
#             # Toggle button
#             if st.button("Already have an account? Login", key="toggle_to_login", use_container_width=True, type="secondary"):
#                 st.session_state['form_type'] = 'login'
#                 st.rerun()

# def show_login_form():
#     with st.form("login_form"):
#         heading_html = """<div style="text-align: center; margin-bottom: 2rem;">
#     <h2 style="margin: 0; font-size: 1.8rem; color: #0f172a; font-family: var(--font-heading); font-weight: 700;">Welcome</h2>
#     <p style="color: #64748b; font-size: 0.88rem; margin-top: 0.4rem; font-family: var(--font-body);">
#         Enter your credentials to access your health workspace
#     </p>
# </div>"""
#         st.markdown(heading_html, unsafe_allow_html=True)
        
#         email = st.text_input("Email", key="login_email", placeholder="you@example.com")
#         password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        
#         # Forgot password right-aligned link
#         forgot_html = """<div style="text-align: right; margin-top: -0.5rem; margin-bottom: 1.25rem;">
#     <a href="#" style="font-size: 0.82rem; color: #2563eb; text-decoration: none; font-family: var(--font-body); font-weight: 600;">
#         Forgot password?
#     </a>
# </div>"""
#         st.markdown(forgot_html, unsafe_allow_html=True)
        
#         if st.form_submit_button("Enter Workspace \u2192", use_container_width=True, type="primary"):
#             if email and password:
#                 success, result = SessionManager.login(email, password)
#                 if success:
#                     st.rerun()
#                 else:
#                     st.error(f"Login failed: {result}")
#             else:
#                 st.error("Please enter both email and password")

# def show_signup_form():
#     with st.form("signup_form"):
#         heading_html = """<div style="text-align: center; margin-bottom: 2rem;">
#     <h2 style="margin: 0; font-size: 1.8rem; color: #0f172a; font-family: var(--font-heading); font-weight: 700;">Create Account</h2>
#     <p style="color: #64748b; font-size: 0.88rem; margin-top: 0.4rem; font-family: var(--font-body);">
#         Sign up to start analyzing health reports
#     </p>
# </div>"""
#         st.markdown(heading_html, unsafe_allow_html=True)
        
#         new_name = st.text_input("Full Name", key="signup_name", placeholder="John Doe")
#         new_email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
#         new_password = st.text_input("Password", type="password", key="signup_password", placeholder="Min. 8 characters")
#         confirm_password = st.text_input("Confirm Password", type="password", key="signup_password2", placeholder="Confirm password")
        
#         requirements_html = """<div style="background: rgba(37, 99, 235, 0.02); border: 1px solid var(--border-light); padding: 1rem; border-radius: 12px; font-size: 0.8rem; margin: 1rem 0;">
#     <strong style="color: var(--text-main); font-family: var(--font-heading);">Password requirements:</strong>
#     <ul style="margin: 0.4rem 0 0 0; padding-left: 1.2rem; color: var(--text-muted); line-height: 1.4; font-family: var(--font-body);">
#         <li>At least 8 characters</li>
#         <li>One uppercase letter (A-Z)</li>
#         <li>One lowercase letter (a-z)</li>
#         <li>One numerical digit (0-9)</li>
#     </ul>
# </div>"""
#         st.markdown(requirements_html, unsafe_allow_html=True)
        
#         if st.form_submit_button("Create Account", use_container_width=True, type="primary"):
#             validation_result = validate_signup_fields(
#                 new_name, new_email, new_password, confirm_password
#             )
            
#             if not validation_result[0]:
#                 st.error(validation_result[1])
#                 return
            
#             success, response = st.session_state.auth_service.sign_up(
#                 new_email, new_password, new_name
#             )
            
#             if success:
#                 st.session_state.authenticated = True
#                 st.session_state.user = response
#                 st.rerun()
#             else:
#                 st.error(f"Sign up failed: {response}")
