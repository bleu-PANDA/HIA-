import streamlit as st
from config.prompts import SPECIALIST_PROMPTS
from utils.pdf_extractor import extract_text_from_pdf
from config.sample_data import SAMPLE_REPORT
from config.app_config import MAX_UPLOAD_SIZE_MB

def show_analysis_form():
    if (
        "current_session" in st.session_state
        and "report_source" not in st.session_state
    ):
        st.session_state.report_source = "Upload PDF"

    st.markdown("<p style='font-family: var(--font-heading); font-size: 0.82rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;'>Choose Report Source</p>", unsafe_allow_html=True)
    report_source = st.radio(
        "Choose report source",
        ["Upload PDF", "Use Sample PDF"],
        index=0 if st.session_state.get("report_source") == "Upload PDF" else 1,
        horizontal=True,
        key="report_source",
        label_visibility="collapsed"
    )

    pdf_contents = get_report_contents(report_source)

    if pdf_contents:
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        render_patient_form(pdf_contents)

def get_report_contents(report_source):
    if report_source == "Upload PDF":
        uploaded_file = st.file_uploader(
            f"Upload blood report PDF (Max {MAX_UPLOAD_SIZE_MB}MB)",
            type=["pdf"],
            help=f"Maximum file size: {MAX_UPLOAD_SIZE_MB}MB. Only PDF files containing medical reports are supported",
            label_visibility="collapsed"
        )
        if uploaded_file:
            # Check file size before processing
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > MAX_UPLOAD_SIZE_MB:
                st.error(
                    f"File size ({file_size_mb:.1f}MB) exceeds the {MAX_UPLOAD_SIZE_MB}MB limit."
                )
                return None

            if uploaded_file.type != "application/pdf":
                st.error("Please upload a valid PDF file.")
                return None

            pdf_contents = extract_text_from_pdf(uploaded_file)
            if isinstance(pdf_contents, str) and (
                pdf_contents.startswith(
                    ("File size exceeds", "Invalid file type", "Error validating")
                )
                or pdf_contents.startswith("The uploaded file")
                or "error" in pdf_contents.lower()
            ):
                st.error(pdf_contents)
                return None
            
            with st.expander("🔍 View Extracted Report Details", expanded=False):
                st.text_area("Raw Text Content", value=pdf_contents, height=200, disabled=True)
            return pdf_contents
    else:
        with st.expander("📋 View Sample Report Details", expanded=False):
            st.text_area("Sample Content", value=SAMPLE_REPORT, height=200, disabled=True)
        return SAMPLE_REPORT
    return None

def render_patient_form(pdf_contents):
    st.markdown("<h3 style='margin-bottom: 1rem; font-size:1.15rem; color:var(--primary-blue); border-bottom: 1px solid var(--border-light); padding-bottom:0.4rem; font-family:var(--font-heading);'>📋 Patient Profile Details</h3>", unsafe_allow_html=True)
    with st.form("analysis_form"):
        patient_name = st.text_input("Patient Name", placeholder="e.g. John Doe")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=30)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        if st.form_submit_button("Analyze Report Details", use_container_width=True, type="primary"):
            handle_form_submission(patient_name, age, gender, pdf_contents)

def handle_form_submission(patient_name, age, gender, pdf_contents):
    if not all([patient_name, age, gender]):
        st.error("Please fill in all fields")
        return

    # Check rate limit first
    from services.ai_service import generate_analysis

    can_analyze, error_msg = generate_analysis(None, None, check_only=True)
    if not can_analyze:
        st.error(error_msg)
        st.stop()
        return

    with st.spinner("Analyzing report values with AI..."):
        # Save report content for follow-up chat
        st.session_state.current_report_text = pdf_contents

        # Save user message
        st.session_state.auth_service.save_chat_message(
            st.session_state.current_session["id"],
            f"Analyzing report for patient: {patient_name}",
        )

        # Generate analysis
        result = generate_analysis(
            {
                "patient_name": patient_name,
                "age": age,
                "gender": gender,
                "report": pdf_contents,
            },
            SPECIALIST_PROMPTS["comprehensive_analyst"],
        )

        if result["success"]:
            # Store report text as a system message for persistence
            report_metadata = f"__REPORT_TEXT__\n{pdf_contents}\n__END_REPORT_TEXT__"
            st.session_state.auth_service.save_chat_message(
                st.session_state.current_session["id"], report_metadata, role="system"
            )

            # Add model used information if available
            content = result["content"]
            if "model_used" in result:
                model_info = f"\n\n*Analysis generated using {result['model_used']}*"
                content += model_info

            st.session_state.auth_service.save_chat_message(
                st.session_state.current_session["id"], content, role="assistant"
            )
            st.rerun()
        else:
            st.error(result["error"])
            st.stop()
