"""
Future Resume Architect (PG Edition) - Clean Orchestrator Shell
==============================================================
Production-ready Streamlit application shell that orchestrates modular logic.
"""

import sys
import subprocess

def install_missing_packages():
    required = ["streamlit", "google-genai", "python-docx", "smolagents", "openai", "xhtml2pdf", "python-pptx", "duckduckgo-search"]
    for pkg in required:
        try:
            if pkg == "google-genai":
                import google.genai
            elif pkg == "python-docx":
                import docx
            elif pkg == "python-pptx":
                import pptx
            elif pkg == "duckduckgo-search":
                import duckduckgo_search
            else:
                __import__(pkg)
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

install_missing_packages()

import logging
import os
import streamlit as st


# Import core configurations & datasets
from core.prompts import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_ICON,
    THEMES,
    THEME_COLORS,
)
from core.data import STREAM_DATA
from core.styles import inject_custom_css
from core.ui import render_hero, render_preview, render_editable_fields

# Import engines & document exporters
from core.engine import (
    get_gemini_client,
    run_research_pass,
    run_planning_pass,
    run_extraction_pass,
    run_enhancement_pass,
    run_scout_pass,
)
from core.doc_maker import (
    generate_docx_bytes,
    generate_markdown,
    generate_ats_text,
    generate_premium_pdf_html,
    generate_pdf_from_html,
    generate_pptx_bytes,
)

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("resume_architect")

# ============================================================
# INITIALIZE PAGE STYLING
# ============================================================

inject_custom_css()
render_hero()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## ⚙️ Configuration")

api_keys_input: str = st.sidebar.text_area(
    "🔑 Gemini API Keys",
    value=os.environ.get("GEMINI_API_KEY", ""),
    height=100,
    help="Paste up to 3 API keys separated by commas or new lines. We will try them in order if one gets exhausted.",
)

theme: str = st.sidebar.selectbox(
    "🎨 Output Theme",
    options=THEMES,
    index=0,
    help="Select the color palette for your final documents.",
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<small style='color:#718096;'>Powered by Gemini 2.5 Flash &bull; Future Resume Edition</small>",
    unsafe_allow_html=True,
)

# ============================================================
# MAIN INPUT AREA
# ============================================================

st.markdown("### 🎓 Academic Stream")
selected_stream = st.selectbox(
    "Choose your postgraduate degree stream:",
    options=list(STREAM_DATA.keys())
)

st.markdown("### 🎯 Career Goals")
available_roles = STREAM_DATA[selected_stream]["roles"]
selected_roles = st.multiselect(
    f"What do you want to become after you graduate with an {selected_stream}? (Select 1 to 3)",
    options=available_roles,
    max_selections=3,
    placeholder="Choose your target roles..."
)

st.markdown("")
build_clicked: bool = st.button("🚀 Generate My Future Resume")

# ============================================================
# PIPELINE
# ============================================================

# Initialize session state keys
if "resume_data" not in st.session_state:
    st.session_state["resume_data"] = None
if "plan_data" not in st.session_state:
    st.session_state["plan_data"] = None
if "research_summary" not in st.session_state:
    st.session_state["research_summary"] = None
if "scout_data" not in st.session_state:
    st.session_state["scout_data"] = None

if build_clicked:
    # Input validation
    if not selected_roles:
        st.warning("⚠️ Please select at least one future career role.")
        st.stop()
        
    keys = [k.strip() for k in api_keys_input.replace(',', '\n').split('\n') if k.strip()]
    if not keys:
        st.error("🔑 Please enter at least one Gemini API Key in the sidebar.")
        st.stop()

    # Clear previous widget states to allow new AI defaults to load
    for key in list(st.session_state.keys()):
        if key.startswith(("edit_", "role_", "company_", "duration_", "achievements_", "pdf_html", "last_theme")):
            del st.session_state[key]
    st.session_state["resume_data"] = None
    st.session_state["plan_data"] = None
    st.session_state["scout_data"] = None

    status = st.empty()
    success = False
    
    for i, current_key in enumerate(keys[:3]):
        try:
            client = get_gemini_client(current_key)
            
            with st.spinner(f"Using API Key {i+1}... Searching the web..."):
                research_summary = run_research_pass(client, selected_roles, status, selected_stream)
                if not research_summary: raise Exception("Research pass failed")
                st.session_state["research_summary"] = research_summary

            with st.spinner(f"Using API Key {i+1}... Architecting proposed structure..."):
                plan = run_planning_pass(client, selected_roles, research_summary, selected_stream)
                if not plan: raise Exception("Planning pass failed")
                st.session_state["plan_data"] = plan
                
            with st.spinner(f"Using API Key {i+1}... Scouting real-time market intelligence..."):
                scout_res = run_scout_pass(client, selected_roles, status)
                st.session_state["scout_data"] = scout_res
                
            success = True
            break
        except Exception as exc:
            logger.warning("Key %d failed: %s", i+1, exc)
            if i < len(keys[:3]) - 1:
                status.info(f"🔄 Switching to API Key {i+2}...")
                
    if not success:
        st.error("❌ All provided API keys failed. Please check your quota or credentials.")
        st.stop()

# ── HUMAN IN THE LOOP PLAN VIEW ──────────────────────────
if st.session_state["plan_data"] is not None and st.session_state["resume_data"] is None:
    st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
    st.markdown("### 🗺️ Proposed 3-Year Resume Blueprint")
    
    if st.session_state.get("scout_data"):
        st.markdown("**📡 Live Market Scout:**")
        with st.expander("🔍 View Live Job Vacancies for your target roles"):
            st.markdown(st.session_state["scout_data"])
                
    st.info(f"**Core Focus Theme:** {st.session_state['plan_data'].get('Core_Focus', '')}")
    
    col_plan1, col_plan2 = st.columns(2)
    with col_plan1:
        st.markdown("**Proposed Business Projects & Case Studies:**")
        for proj in st.session_state["plan_data"].get("Proposed_Projects", []):
            st.markdown(f"- {proj}")
    with col_plan2:
        st.markdown("**Proposed Certifications to Earn:**")
        for cert in st.session_state["plan_data"].get("Proposed_Certifications", []):
            st.markdown(f"- {cert}")
            
    st.markdown("I've designed this 3-year plan sequence. Do you agree with this direction?")
    
    with st.form("feedback_form"):
        user_feedback = st.text_area("Optional changes or directions (e.g. 'Focus more on Cloud', 'Add an AWS cert')", "")
        approve_clicked = st.form_submit_button("✅ Approve Plan & Build Full Resume")
    
    if approve_clicked:
        keys = [k.strip() for k in api_keys_input.replace(',', '\n').split('\n') if k.strip()]
        if not keys:
            st.error("🔑 Please enter your Gemini API Key in the sidebar.")
            st.stop()
            
        progress = st.progress(0, text="Building full resume...")
        status = st.empty()
        success = False
        
        for i, current_key in enumerate(keys[:3]):
            try:
                client = get_gemini_client(current_key)
                
                # Pass 1: Extraction
                progress.progress(20, text=f"Key {i+1}: Structuring your future resume details…")
                extracted = run_extraction_pass(
                    client,
                    selected_roles,
                    st.session_state["research_summary"],
                    status,
                    selected_stream,
                    STREAM_DATA[selected_stream]["degree_placeholder"],
                    user_feedback
                )
                if not extracted: raise Exception("Extraction pipeline failed")
                
                # Pass 2: Enhancement
                progress.progress(60, text=f"Key {i+1}: Polishing vocabulary and ATS style…")
                enhanced = run_enhancement_pass(client, extracted, status)
                if not enhanced: raise Exception("Enhancement pipeline failed")
                
                progress.progress(100, text="Build complete!")
                st.session_state["resume_data"] = enhanced
                st.session_state["plan_data"] = None
                success = True
                break
            except Exception as exc:
                logger.warning("Key %d failed during build: %s", i+1, exc)
                if i < len(keys[:3]) - 1:
                    status.warning(f"⚠️ API Key {i+1} failed. Trying next key...")
                    
        if not success:
            progress.progress(100, text="Pipeline failed on all keys.")
            st.stop()
            
        st.rerun()


if st.session_state["resume_data"] is not None:
    st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
    st.success("🎉 **Your Future Resume is ready! Review, customize the blanks, and download.**")

    # ── EDITABLE FIELDS ────────────────────────────────────
    final_data = render_editable_fields(st.session_state["resume_data"])
    st.session_state["resume_data"] = final_data

    st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

    # ── PREVIEW ────────────────────────────────────────────
    render_preview(final_data)
    
    # ── GENERATE ALL EXPORTS ───────────────────────────────
    with st.spinner("Building export files…"):
        try:
            docx_bytes = generate_docx_bytes(final_data, theme)
        except Exception as exc:
            logger.error("DOCX generation failed: %s", exc)
            st.error(f"❌ DOCX generation failed: {exc}")
            docx_bytes = b""
            
        theme_colors_dict = THEME_COLORS.get(theme, THEME_COLORS["Modern-Tech"])
        pdf_html = generate_premium_pdf_html(final_data, theme_colors_dict)
            
        try:
            pdf_bytes = generate_pdf_from_html(pdf_html)
        except Exception as exc:
            logger.error("PDF generation failed: %s", exc)
            pdf_bytes = b""
            st.error("⚠️ PDF generation failed. If you're on Streamlit Cloud, please reboot the app to install 'wkhtmltopdf' via packages.txt.")

        try:
            pptx_bytes = generate_pptx_bytes(final_data, theme)
        except Exception as exc:
            logger.error("PPTX generation failed: %s", exc)
            pptx_bytes = b""

        md_content = generate_markdown(final_data)
        ats_content = generate_ats_text(final_data)

    # ── DOWNLOAD BUTTONS ───────────────────────────────────
    st.markdown("### 📥 Download Your Masterpiece")
    dl1, dl2, dl3, dl4, dl5 = st.columns(5)

    with dl1:
        if pdf_bytes:
            st.download_button(
                label="🎨 Stunning PDF",
                data=pdf_bytes,
                file_name="Future_Resume_Premium.pdf",
                mime="application/pdf",
                type="primary"
            )
        else:
            st.button("🚫 PDF Error", disabled=True)

    with dl2:
        if docx_bytes:
            st.download_button(
                label="📄 Premium Word",
                data=docx_bytes,
                file_name="Future_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            
    with dl3:
        if pptx_bytes:
            st.download_button(
                label="📊 PowerPoint",
                data=pptx_bytes,
                file_name="Future_Resume.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )

    with dl4:
        st.download_button(
            label="📝 Markdown",
            data=md_content.encode("utf-8"),
            file_name="Future_Resume.md",
            mime="text/markdown",
        )

    with dl5:
        st.download_button(
            label="📃 ATS Text",
            data=ats_content.encode("utf-8"),
            file_name="Future_Resume_ATS.txt",
            mime="text/plain",
        )
