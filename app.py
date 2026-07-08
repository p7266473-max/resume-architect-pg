"""
Future Resume Architect (PG Edition) - Clean Orchestrator Shell
==============================================================
Production-ready Streamlit application shell that orchestrates modular logic.
"""

import logging
import os
import streamlit as st

# Import core configurations & datasets
from core.prompts import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_ICON,
    THEMES,
)
from core.data import STREAM_DATA
from core.styles import inject_custom_css
from core.ui import render_hero, render_preview, render_editable_fields

# Import engines & document exporters
from core.engine import (
    get_gemini_client,
    run_research_pass,
    run_extraction_pass,
    run_enhancement_pass,
)
from core.doc_maker import (
    generate_docx_bytes,
    generate_markdown,
    generate_ats_text,
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

api_key: str = st.sidebar.text_input(
    "🔑 Gemini API Key",
    value=os.environ.get("GEMINI_API_KEY", ""),
    type="password",
    help="Get your key at https://aistudio.google.com/apikey",
)

theme: str = st.sidebar.selectbox(
    "🎨 Output Theme",
    options=THEMES,
    index=0,
    help="Select the color palette for your final Word document.",
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

# Initialize session state for resume data
if "resume_data" not in st.session_state:
    st.session_state["resume_data"] = None

if build_clicked:
    # Input validation
    if not selected_roles:
        st.warning("⚠️ Please select at least one future career role.")
        st.stop()
    if not api_key.strip():
        st.error("🔑 Please enter your Gemini API Key in the sidebar.")
        st.stop()

    # Clear previous widget states to allow new AI defaults to load
    for key in list(st.session_state.keys()):
        if key.startswith(("edit_", "role_", "company_", "duration_", "achievements_")):
            del st.session_state[key]

    # Client
    try:
        client = get_gemini_client(api_key.strip())
    except Exception as exc:
        logger.error("Client init failed: %s", exc)
        st.error(f"❌ Failed to initialise Gemini client: {exc}")
        st.stop()

    progress = st.progress(0, text="Initialising pipeline…")
    status = st.empty()

    # Web Research Grounding Pass
    progress.progress(5, text="Web Research: Finding the best free courses…")
    with st.spinner("Searching the web for top free/open-source certifications for your path..."):
        research_summary = run_research_pass(client, selected_roles, status, selected_stream)

    # Pass 1
    progress.progress(15, text="Pass 1: Architecting your future resume…")
    with st.spinner("Building your 3-year career trajectory…"):
        extracted = run_extraction_pass(
            client,
            selected_roles,
            research_summary,
            status,
            selected_stream,
            STREAM_DATA[selected_stream]["degree_placeholder"]
        )

    if extracted is None:
        progress.progress(100, text="Pipeline failed.")
        st.stop()

    progress.progress(55, text="Pass 1 complete ✓")
    status.success("✅ Architecture complete.")

    # Pass 2
    progress.progress(60, text="Pass 2: Polishing vocabulary…")
    with st.spinner("Elevating resume language to a top-tier standard…"):
        enhanced = run_enhancement_pass(client, extracted, status)

    progress.progress(85, text="Pass 2 complete ✓")
    status.success("✅ Enhancement complete.")
    progress.progress(100, text="Pipeline complete!")
    status.empty()

    st.session_state["resume_data"] = enhanced

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

        md_content = generate_markdown(final_data)
        ats_content = generate_ats_text(final_data)

    # ── DOWNLOAD BUTTONS ───────────────────────────────────
    st.markdown("### 📥 Download Your Masterpiece")
    dl1, dl2, dl3 = st.columns(3)

    with dl1:
        if docx_bytes:
            st.download_button(
                label="📄 Premium Word Document (.docx)",
                data=docx_bytes,
                file_name="Future_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

    with dl2:
        st.download_button(
            label="📝 Markdown (.md)",
            data=md_content.encode("utf-8"),
            file_name="Future_Resume.md",
            mime="text/markdown",
        )

    with dl3:
        st.download_button(
            label="📃 ATS Plain Text (.txt)",
            data=ats_content.encode("utf-8"),
            file_name="Future_Resume_ATS.txt",
            mime="text/plain",
        )
