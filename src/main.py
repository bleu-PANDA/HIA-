import streamlit as st
from auth.session_manager import SessionManager
from components.auth_pages import show_login_page
from components.analysis_form import show_analysis_form
from components.footer import show_footer
from config.app_config import APP_NAME, APP_TAGLINE, APP_DESCRIPTION, APP_ICON, ANALYSIS_DAILY_LIMIT
from services.ai_service import get_chat_response
from datetime import datetime
from utils.icons import get_svg_icon, get_image_base64

# Configure Streamlit page layout and sidebar state
st.set_page_config(
    page_title="HIA - Health Insights Agent",
    page_icon="src/static/stethoscope.webp",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS Stylesheet
def load_css():
    css_path = "src/static/styles.css"
    try:
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        pass

load_css()

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

if st.session_state.theme_mode == "dark":
    st.markdown("""
    <style>

    :root{

        --bg-base:#0f172a;
        --bg-white:#1e293b;

        --primary-blue:#60a5fa;
        --secondary-blue:#93c5fd;
        --accent-blue:#bfdbfe;

        --text-main:#f8fafc;
        --text-body:#cbd5e1;
        --text-muted:#94a3b8;

        --border-light:#334155;

        --card-bg:#1e293b;

        --hero-gradient-start:#1e293b;
        --hero-gradient-end:#334155;

        --metric-icon-bg:#334155;

        --status-bg:#1e3a8a;

        --user-chat-bg:#1e3a8a;

        --shadow-premium:
            0 10px 40px -10px rgba(0,0,0,.35);

        --shadow-hover:
            0 20px 50px -12px rgba(0,0,0,.45);

    }

    </style>
    """, unsafe_allow_html=True)

# Hide Streamlit input helper instructions
st.markdown(
    """
    <style>
        div[data-testid="InputInstructions"] > span:nth-child(1) {
            visibility: hidden;
        }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown("""
<style>

div[data-testid="stButton"]:has(button[kind="secondary"]) button{
    width:52px !important;
    height:52px !important;

    min-height:52px !important;
    min-width:52px !important;

    border-radius:50% !important;

    background:white !important;

    backdrop-filter:blur(12px) !important;
    -webkit-backdrop-filter:blur(12px) !important;

    border:none !important;
    box-shadow:none !important;

    font-size:22px !important;

    padding:0 !important;
}

</style>
""", unsafe_allow_html=True)


def show_welcome_screen():
    display_name = st.session_state.user.get("name") or st.session_state.user.get("email", "")
    
    # 30 health-related quotes
    HEALTH_QUOTES = [
        "Health is a state of complete physical, mental and social well-being and not merely the absence of disease or infirmity.",
        "It is health that is real wealth and not pieces of gold and silver.",
        "The groundwork of all happiness is health.",
        "To keep the body in good health is a duty... otherwise we shall not be able to keep our mind strong and clear.",
        "He who has health has hope; and he who has hope has everything.",
        "A fit body, a calm mind, a safe home. These things cannot be bought – they must be earned.",
        "An ounce of prevention is worth a pound of cure.",
        "The greatest of follies is to sacrifice health for any other kind of happiness.",
        "Your body holds deep wisdom. Trust in it, learn from it, nourish it.",
        "Nourishing yourself is not selfish. It’s essential to your survival and your well-being.",
        "Good health is not something we can buy. However, it can be an extremely valuable savings account.",
        "To ensure good health: eat lightly, breathe deeply, live moderately, cultivate cheerfulness, and maintain an interest in life.",
        "Physical fitness is not only one of the most important keys to a healthy body, it is the basis of dynamic and creative intellectual activity.",
        "Sleep is the golden chain that ties health and our bodies together.",
        "Happiness is the highest form of health.",
        "A healthy outside starts from the inside.",
        "Invest in your health today so you can thrive tomorrow.",
        "Every small step toward wellness is a step toward a vibrant life.",
        "Your health is an investment, not an expense.",
        "The human body is the best picture of the human soul.",
        "Keep your vitality. A life without health is like a river without water.",
        "Wellness is a connection of path, progress, and presence.",
        "The doctor of the future will give no medicine, but will interest his patients in the care of the human frame, in diet, and in the cause and prevention of disease.",
        "Rest when you are tired. Refresh and renew yourself, your body, your mind, your spirit. Then get back to work.",
        "Patience, persistence, and perspiration make an unbeatable combination for health and success.",
        "Water is the driving force of all nature. Stay hydrated, stay healthy.",
        "Take care of your body. It's the only place you have to live.",
        "Maintained health is a reflection of daily self-care and mindful choices.",
        "True healthcare begins with self-care and daily habits of wellness.",
        "Let food be thy medicine and medicine be thy food."
    ]
    
    # Select consistent quote per day based on day of year
    day_of_year = datetime.now().timetuple().tm_yday
    quote_index = day_of_year % len(HEALTH_QUOTES)
    daily_quote = HEALTH_QUOTES[quote_index]

    # Render Quote of the Day banner
    # Keep multi-line string aligned to column 0 to prevent raw HTML rendering
    quote_banner_html = f"""<div class="daily-insight-banner" style="
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    border-radius: 20px;
    padding: 2.25rem 2.5rem;
    color: #ffffff;
    box-shadow: 0 10px 30px -5px rgba(37, 99, 235, 0.15);
    margin-top: 19px;
    margin-bottom: 19px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
">
    <div style="position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(255, 255, 255, 0.08); border-radius: 50%;"></div>
    <div style="position: absolute; bottom: -30px; left: 10%; width: 80px; height: 80px; background: rgba(255, 255, 255, 0.05); border-radius: 50%;"></div>
    <div style="position: relative; z-index: 2;">
        <div style="font-family: var(--font-heading); font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: rgba(255, 255, 255, 0.85); margin-bottom: 0.75rem; display: flex; align-items: center; gap: 6px;">
            <span>🛡️</span> Daily Health Insight
        </div>
        <div style="font-family: var(--font-body); font-size: 1.45rem; font-weight: 500; line-height: 1.5; margin-bottom: 1rem; color: #ffffff; max-width: 800px;">
            "{daily_quote}"
        </div>
        <div style="font-family: var(--font-heading); font-size: 0.88rem; font-weight: 600; color: rgba(255, 255, 255, 0.9);">
            — Quote of the Day
        </div>
    </div>
</div>"""
    st.markdown(quote_banner_html, unsafe_allow_html=True)

    # Load sculpture base64
    sculpture_b64 = get_image_base64("src/static/sculpture.png")
    sculpture_html = ""
    if sculpture_b64:
        sculpture_html = f"""<div style="flex: 1; display: flex; justify-content: center; align-items: center; min-width: 200px; max-width: 420px; height: auto;">
<img src="{sculpture_b64}" style="width: 100%; height: auto; object-fit: contain; filter: drop-shadow(0 8px 20px rgba(37, 99, 235, 0.06));" alt="Sculpture">
</div>"""
    else:
        sculpture_html = """<div class="crystal-sculpture-container" style="flex: 1; display: flex; justify-content: center; align-items: center; min-width: 200px; max-width: 420px;">
<div class="csculpture_b64rystal-sculpture" style="width: 100px; height: 100px;"></div>
</div>"""

    # 1. Editorial Landing-page Style Hero Banner (35-40% viewport height) with Crystal Sculpture
    hero_html = f"""<div class="hero-container" style="min-height: 280px; padding: 2.5rem 3rem !important;">
<div style="display: flex; justify-content: space-between; align-items: center; width: 100%; gap: 1rem; flex-wrap: wrap;">
<div style="flex: 1.5; min-width: 280px;">
<div style="font-size: 0.85rem; font-weight: 600; color: var(--primary-blue); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem; font-family: var(--font-heading);">HEALTH WORKSPACE</div>
<div class="hero-title" style="margin-bottom: 0.5rem; font-size: 2.75rem !important; line-height: 1.2 !important;">Hi {display_name}</div>
<div style="color: var(--text-muted); font-size: 1.25rem; margin-bottom: 0.5rem; font-family: var(--font-body); font-weight: 500;">Hope you're doing well.</div>
<div style="color: var(--text-main); font-size: 1.5rem; font-family: var(--font-heading); font-weight: 600; line-height: 1.3;">Ready to analyze your next medical report?</div>
</div>
{sculpture_html}
</div>
</div>"""
    
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown(hero_html, unsafe_allow_html=True)

    # Fetch User Sessions and calculate stats
    success, sessions = SessionManager.get_user_sessions()
    
    total_sessions = len(sessions) if (success and sessions) else 0
    reports_analyzed = total_sessions # Baseline estimation: each session represents one analysis report upload
    
    last_analysis_str = "None"
    if success and sessions and len(sessions) > 0:
        latest_created = sessions[0].get("created_at", "")
        try:
            date_obj = datetime.fromisoformat(latest_created.replace("Z", "+00:00"))
            last_analysis_str = date_obj.strftime("%b %d, %Y")
        except Exception:
            last_analysis_str = latest_created[:10]

    # Calculate remaining quota runs
    if 'analysis_count' not in st.session_state:
        st.session_state.analysis_count = 0
    remaining = ANALYSIS_DAILY_LIMIT - st.session_state.analysis_count
    quota_percentage = int((remaining / ANALYSIS_DAILY_LIMIT) * 100)

    # Ingest SVG icons for the 4 metrics columns
    svg_clipboard = get_svg_icon("ClipboardList", size=22, color="var(--primary-blue)")
    svg_chat = get_svg_icon("MessageCircle", size=22, color="var(--primary-blue)")
    svg_calendar = get_svg_icon("Calendar", size=22, color="var(--primary-blue)")
    svg_clock = get_svg_icon("Clock3", size=22, color="var(--primary-blue)")

    # 2. Statistics Row (Reference B - Single Horizontal Card Row divided into 4 symmetric columns)
    st.markdown(
        f"""
        <div class="metrics-row-card">
            <div class="metric-col-section">
                <div class="metric-icon-box">{svg_clipboard}</div>
                <div class="metric-text-box">
                    <div class="metric-num-val">{reports_analyzed}</div>
                    <div class="metric-label-val">Reports Analyzed</div>
                    <div class="metric-desc-val">Total reports processed</div>
                </div>
            </div>
            <div class="metric-col-section">
                <div class="metric-icon-box">{svg_chat}</div>
                <div class="metric-text-box">
                    <div class="metric-num-val">{total_sessions}</div>
                    <div class="metric-label-val">Total Sessions</div>
                    <div class="metric-desc-val">Conversations held</div>
                </div>
            </div>
            <div class="metric-col-section">
                <div class="metric-icon-box">{svg_calendar}</div>
                <div class="metric-text-box">
                    <div class="metric-num-val">{last_analysis_str}</div>
                    <div class="metric-label-val">Last Analysis</div>
                    <div class="metric-desc-val">Most recent report</div>
                </div>
            </div>
            <div class="metric-col-section">
                <div class="metric-icon-box">{svg_clock}</div>
                <div class="metric-text-box" style="width: 100%; min-width: 150px;">
                    <div class="metric-num-val">{remaining} / {ANALYSIS_DAILY_LIMIT}</div>
                    <div class="metric-label-val">Daily Quota</div>
                    <div class="metric-desc-val" style="margin-bottom: 0.35rem;">Runs left today</div>
                    <div style="background: #e2e8f0; border-radius: 99px; height: 6px; width: 100%; overflow: hidden;">
                        <div style="background: var(--primary-blue); height: 100%; width: {quota_percentage}%;"></div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-top: 0rem;'></div>", unsafe_allow_html=True)

    # 3. Session Cards History Grid
    # if success and sessions:
    #     sessions = sorted(sessions,key=lambda x: x.get("created_at", ""),reverse=True)[:6]
    #     clipboard_icon = get_svg_icon("ClipboardList", size=24, color="var(--primary-blue)", extra_style="vertical-align: middle; margin-right: 8px;")
    #     st.markdown(f"<h3 style='margin-bottom: 1.5rem; font-size: 1.6rem; font-family: var(--font-heading);'>{clipboard_icon}Recent Analyses</h3>", unsafe_allow_html=True)
        
    #     cols_per_row = 3
    #     for i in range(0, len(sessions), cols_per_row):
    #         row_sessions = sessions[i:i+cols_per_row]
    #         cols = st.columns(cols_per_row)
    #         for idx, session in enumerate(row_sessions):
    #             with cols[idx]:
    #                 created_at = session.get("created_at", "")
    #                 try:
    #                     date_obj = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    #                     date_str = date_obj.strftime("%B %d, %Y")
    #                 except Exception:
    #                     date_str = created_at[:10]
                    
    #                 card_icon = get_svg_icon("ClipboardList", size=16, color="var(--primary-blue)", extra_style="vertical-align: middle; margin-right: 6px;")
    #                 clock_icon = get_svg_icon("Clock3", size=14, color="var(--text-muted)", extra_style="vertical-align: middle; margin-right: 4px;")
                    
    #                 st.markdown(
    #                     f"""
    #                     <div class="session-card">
    #                         <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
    #                             <div class="session-card-title">{card_icon}{session['title']}</div>
    #                             <span class="status-indicator status-active">Analyzed</span>
    #                         </div>
    #                         <div class="session-card-date">{clock_icon}Created: {date_str}</div>
    #                         <div class="session-card-preview">Contains the clinical health report analysis, extracted blood biomarkers, and AI follow-up queries. Click to enter workspace.</div>
    #                     </div>
    #                     """,
    #                     unsafe_allow_html=True
    #                 )
                    
    #                 if st.button("Enter Workspace", key=f"open_welcome_{session['id']}", use_container_width=True, type="secondary"):
    #                     st.session_state.current_session = session
    #                     st.rerun()
 
    # 4. Large modern CTA Analysis trigger
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    # st.markdown(
    #     f"""
    #     <div class="glass-card" style="text-align: center; padding: 2rem 3rem 2rem 3rem; background: var(--bg-white) !important; border: 1px solid var(--border-light) !important; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1rem; border-radius: 20px; box-shadow: var(--shadow-premium);">
    #         <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 1rem; animation: float 8s ease-in-out infinite;">
    #             <img src="{sculpture_b64}" style="max-height: 120px; object-fit: contain; filter: drop-shadow(0 15px 35px rgba(37, 99, 235, 0.12));">
    #         </div>
    #         <h2 style="margin-top: 0; font-size: 2rem; color: var(--primary-blue); font-family: var(--font-heading);">Begin Your Next Analysis Workspace</h2>
    #         <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto; font-size: 1.05rem; font-family: var(--font-body);">
    #             Upload a lab report PDF or choose our pre-loaded patient sample files to automatically generate clinical explanations and interact in a RAG workspace.
    #         </p>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
    st.markdown(
f"""
<div style="
background: linear-gradient(
135deg,
var(--hero-gradient-start) 0%,
var(--hero-gradient-end) 100%);
border:1px solid rgba(96,165,250,0.12);
border-radius:32px;
padding:3rem 3.5rem;
box-shadow:var(--shadow-premium);
overflow:hidden;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
gap:2rem;
flex-wrap:wrap;
">

<!-- Left side -->
<div style="
flex:1.5;
min-width:280px;
">

<div style="
font-size:0.85rem;
font-weight:700;
letter-spacing:0.08em;
text-transform:uppercase;
color:var(--primary-blue);
margin-bottom:0.7rem;
font-family:var(--font-heading);
">
NEW ANALYSIS
</div>

<h2 style="
margin:0;
font-size:2rem;
font-family:var(--font-heading);
color:var(--text-main);
line-height:1.2;
">
Begin Your Next Analysis Workspace
</h2>

<div style="
color:var(--text-muted);
font-size:1.1rem;
line-height:1.7;
margin-top:1rem;
max-width:650px;
font-family:var(--font-body);
">
Upload a lab report PDF or choose our pre-loaded patient sample files to automatically generate clinical explanations and interact in a RAG workspace.
</div>

</div>

<!-- Right side -->
<div style="
flex:1;
display:flex;
justify-content:flex-end;
min-width:250px;
">

<img src="{sculpture_b64}"
style="
width:320px;
object-fit:contain;
filter:drop-shadow(0 15px 35px rgba(37,99,235,0.12));
">

</div>

</div>

</div>
""",
unsafe_allow_html=True
)
    
    # col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
    col_cta1, col_cta2, col_cta3 = st.columns([1.2,2,1.2])
    with col_cta2:
        if st.button("Start New Analysis Workspace", key="cta_new_analysis", use_container_width=True, type="primary"):
            success, session = SessionManager.create_chat_session()
            if success:
                st.session_state.current_session = session
                st.rerun()
            else:
                st.error("Failed to create session")

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    if success and sessions:
        sessions = sorted(sessions,key=lambda x: x.get("created_at", ""),reverse=True)[:6]
        clipboard_icon = get_svg_icon("ClipboardList", size=24, color="var(--primary-blue)", extra_style="vertical-align: middle; margin-right: 8px;")
        st.markdown(f"<h3 style='margin-bottom: 1.5rem; font-size: 1.6rem; font-family: var(--font-heading);'>{clipboard_icon}Recent Analyses</h3>", unsafe_allow_html=True)
        
        cols_per_row = 3
        for i in range(0, len(sessions), cols_per_row):
            row_sessions = sessions[i:i+cols_per_row]
            cols = st.columns(cols_per_row)
            for idx, session in enumerate(row_sessions):
                with cols[idx]:
                    created_at = session.get("created_at", "")
                    try:
                        date_obj = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                        date_str = date_obj.strftime("%B %d, %Y")
                    except Exception:
                        date_str = created_at[:10]
                    
                    card_icon = get_svg_icon("ClipboardList", size=16, color="var(--primary-blue)", extra_style="vertical-align: middle; margin-right: 6px;")
                    clock_icon = get_svg_icon("Clock3", size=14, color="var(--text-muted)", extra_style="vertical-align: middle; margin-right: 4px;")
                    
                    st.markdown(
                        f"""
                        <div class="session-card">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                                <div class="session-card-title">{card_icon}{session['title']}</div>
                                <span class="status-indicator status-active">Analyzed</span>
                            </div>
                            <div class="session-card-date">{clock_icon}Created: {date_str}</div>
                            <div class="session-card-preview">Contains the clinical health report analysis, extracted blood biomarkers, and AI follow-up queries. Click to enter workspace.</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    if st.button("Enter Workspace", key=f"open_welcome_{session['id']}", use_container_width=True, type="primary"):
                        st.session_state.current_session = session
                        st.rerun()
                
    # 5. Footer (Reference C)
    show_footer()


def get_first_assistant_report(messages):
    """Scan history to locate the main comprehensive analysis report message."""
    if messages:
        for msg in messages:
            if msg.get("role") == "assistant" and len(msg.get("content", "")) > 100:
                return msg.get("content", "")
    return None


def show_chat_history():
    success, messages = st.session_state.auth_service.get_session_messages(
        st.session_state.current_session["id"]
    )

    if success:
        for msg in messages:
            if msg.get("role") == "system":
                continue
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar="🩺"):
                    st.markdown(msg["content"])
        return messages
    return []


def handle_chat_input(messages):
    if prompt := st.chat_input("Ask a follow-up question about the report..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Save user query
        st.session_state.auth_service.save_chat_message(
            st.session_state.current_session["id"], prompt, role="user"
        )

        # Load context report text
        context_text = st.session_state.get("current_report_text", "")

        # Re-extract from system messages if not cached in memory
        if not context_text and messages:
            for msg in messages:
                if msg.get("role") == "system" and "__REPORT_TEXT__" in msg.get(
                    "content", ""
                ):
                    content = msg.get("content", "")
                    start_idx = content.find("__REPORT_TEXT__\n") + len(
                        "__REPORT_TEXT__\n"
                    )
                    end_idx = content.find("\n__END_REPORT_TEXT__")
                    if start_idx > len("__REPORT_TEXT__\n") - 1 and end_idx > start_idx:
                        context_text = content[start_idx:end_idx]
                        st.session_state.current_report_text = context_text
                        break

        with st.spinner("Thinking..."):
            response = get_chat_response(prompt, context_text, messages)

            with st.chat_message("assistant", avatar="🩺"):
                st.markdown(response)

            # Save assistant reply
            st.session_state.auth_service.save_chat_message(
                st.session_state.current_session["id"], response, role="assistant"
            )
            st.rerun()


def show_user_greeting():
    if st.session_state.user:
        display_name = st.session_state.user.get("name") or st.session_state.user.get(
            "email", ""
        )
        st.markdown(
            f"""
            <div class="user-greeting-container" style='text-align: right; padding: 0.5rem 0.6rem 0rem 1rem; color: var(--primary-blue); font-size: 0.95rem; font-weight: 600; font-family: var(--font-heading);'>
                👤 Hi, {display_name}
            </div>
        """,
            unsafe_allow_html=True,
        )

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

def show_theme_toggle():
    icons = {
        "light": "☀️",
        "dark": "🌙"
    }

    if st.button(
    icons[st.session_state.theme_mode],
    key="theme_toggle_btn",
    help="Change theme",
    type="secondary"
    ):
        if st.session_state.theme_mode == "light":
            st.session_state.theme_mode = "dark"
        else:
            st.session_state.theme_mode = "light"

        st.rerun()

def main():
    # Check for exit workspace parameter
    if st.query_params.get("exit") == "1":
        st.query_params.clear()
        st.session_state.current_session = None
        st.rerun()

    SessionManager.init_session()

    if not SessionManager.is_authenticated():
        show_login_page()
        return

    # col1, col2 = st.columns([20,1])

    # with col2:
    #     show_theme_toggle()

    # User details greeting row
    st.markdown("<div style='height:0px'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([25,1])

    with col1:
        show_user_greeting()

    with col2:
        show_theme_toggle()

    # Profile display check
    if st.session_state.get("show_profile"):
        name = st.session_state.user.get("name") or st.session_state.user.get("email", "")
        email = st.session_state.user.get("email", "")
        st.markdown(
            f"""
            <div style="background: #ffffff; border: 1px solid #e2e8f0; padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 40px -10px rgba(15,23,42,0.05); margin-bottom: 2rem; max-width: 500px; margin-left: auto; margin-right: auto; position: relative;">
                <h3 style="margin-top: 0; color: #2563eb; font-family: var(--font-heading); font-size: 1.5rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.75rem; margin-bottom: 1.25rem;">Patient Profile</h3>
                <div style="font-family: var(--font-body); font-size: 0.95rem; color: #334155; line-height: 2.0;">
                    <p style="margin: 0.5rem 0;">👤 <strong>Full Name:</strong> {name}</p>
                    <p style="margin: 0.5rem 0;">✉️ <strong>Email Address:</strong> {email}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Close Profile View", key="close_profile_view_btn", use_container_width=True, type="primary"):
            st.session_state.show_profile = False
            st.rerun()

    # Session Workspace Router
    if st.session_state.get("current_session"):
        # Inject marker to style the horizontal columns block as a banner card
        st.markdown('<div class="workspace-header-marker"></div>', unsafe_allow_html=True)
        st.markdown("""
            <style>
                div:has(> .workspace-header-marker) {
                    display: none !important;
                }
                div:has(> .workspace-header-marker) + div[data-testid="stHorizontalBlock"] {
                    background: linear-gradient(135deg, #eff6ff 0%, #e0f2fe 100%) !important;
                    border: 1px solid rgba(96, 165, 250, 0.15) !important;
                    border-radius: 20px !important;
                    padding: 1.5rem 2rem !important;
                    margin-bottom: 2.25rem !important;
                    box-shadow: var(--shadow-premium) !important;
                    align-items: center !important;
                }
                div:has(> .workspace-header-marker) + div[data-testid="stHorizontalBlock"] button {
                    background-color: var(--bg-white) !important;
                    border: 1px solid var(--border-light) !important;
                    color: var(--text-main) !important;
                    font-family: var(--font-heading) !important;
                    font-weight: 600 !important;
                    border-radius: 10px !important;
                    padding: 0.4rem 1.2rem !important;
                    font-size: 0.85rem !important;
                    float: right !important;
                    box-shadow: none !important;
                }
                div:has(> .workspace-header-marker) + div[data-testid="stHorizontalBlock"] button:hover {
                    border-color: var(--secondary-blue) !important;
                    color: var(--primary-blue) !important;
                }
            </style>
        """, unsafe_allow_html=True)

        col_title, col_btn = st.columns([3, 1])
        with col_title:
            st.markdown(
                f"""
                <h2 style="margin:0; font-size:1.6rem; color: var(--text-main); font-family: var(--font-heading);">📊 {st.session_state.current_session['title']}</h2>
                <div style="color:var(--text-muted); font-size:0.85rem; margin-top:0.2rem; font-family: var(--font-body);">Health Workspace Panel</div>
                """,
                unsafe_allow_html=True
            )
        with col_btn:
            if st.button("↩ Exit Workspace", key="exit_workspace_btn"):
                st.session_state.current_session = None
                st.rerun()

        # Retrieve messages
        success, messages = st.session_state.auth_service.get_session_messages(
            st.session_state.current_session["id"]
        )
        if not success:
            messages = []

        # If analysis report exists, divide main content area into 3 columns
        if messages:
            # Workspace columns
            col_left, col_center, col_right = st.columns([1, 2.2, 1.2])

            with col_left:
                st.markdown(
                    """
                    <div class="workspace-left-card">
                        <h4 style="margin-top:0; color:var(--primary-blue); font-size:1.1rem; border-bottom:1px solid var(--border-light); padding-bottom:0.4rem;">Patient Profile</h4>
                        <div style="font-size:0.9rem; line-height:1.8; color:var(--text-body);">
                            <p style="margin: 0.4rem 0;">👤 <strong>Name</strong>: Patient Profile</p>
                            <p style="margin: 0.4rem 0;">🕒 <strong>Status</strong>: Workspace Open</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                with st.expander("📝 Update Report / Re-analyze", expanded=False):
                    show_analysis_form()

            with col_center:
                # Main Chat flow area
                for msg in messages:
                    if msg.get("role") == "system":
                        continue
                    if msg["role"] == "user":
                        with st.chat_message("user", avatar="👤"):
                            st.markdown(msg["content"])
                    else:
                        with st.chat_message("assistant", avatar="🩺"):
                            st.markdown(msg["content"])

                handle_chat_input(messages)

            with col_right:
                # Core Report summary card
                report_content = get_first_assistant_report(messages)
                if report_content:
                    st.markdown(
                        """
                        <div class="workspace-right-card">
                            <h4 style="margin-top:0; color:var(--primary-blue); font-size:1.1rem; border-bottom:1px solid var(--border-light); padding-bottom:0.4rem;">📋 Insights & Findings</h4>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(report_content)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown(
                        """
                        <div class="workspace-right-card" style="text-align:center; padding:3rem 1.5rem; color:var(--text-muted);">
                            <p>No report insights generated yet.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            # Brand new session where report hasn't been uploaded yet
            show_analysis_form()
    else:
        show_welcome_screen()


if __name__ == "__main__":
    main()
