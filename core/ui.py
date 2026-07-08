import streamlit as st

def render_hero():
    """Render the hero section on top of the app."""
    st.markdown("""
<div class="hero-container">
  <div class="hero-overlay">
    <div class="hero-title">Design Your <span>Future PG Resume</span></div>
    <p class="hero-sub">Are you a Postgraduate or MBA student? Select your dream career roles, and we will architect the exact resume you'll have in 3 years—complete with the free online certifications you need to take to get there.</p>
  </div>
</div>
""", unsafe_allow_html=True)

def render_preview(data: dict) -> None:
    """Render a rich, read-only in-app preview of the resume."""
    with st.expander("📄 Future Resume Preview", expanded=True):
        name = data.get("Name", "").strip()
        if name:
            st.markdown(f"<h2 style='text-align:center; font-size: 2.5rem; margin-bottom: 0;'>{name}</h2>", unsafe_allow_html=True)
        
        contact_items = [
            data.get("Location", ""), data.get("Phone", ""),
            data.get("Email", ""), data.get("LinkedIn", "")
        ]
        contact_line = "  &nbsp;|&nbsp;  ".join(f"{c}" for c in contact_items if c)
        if contact_line:
            st.markdown(f"<p style='text-align:center; color:#555;'>{contact_line}</p>", unsafe_allow_html=True)
        
        st.markdown('<hr class="glow-divider" style="margin: 1rem 0;">', unsafe_allow_html=True)

        st.markdown("### 📋 Executive Summary")
        st.info(data.get("Summary", ""))
        
        st.markdown('<hr class="glow-divider" style="margin: 1.5rem 0;">', unsafe_allow_html=True)

        st.markdown("### 💼 Strategic Projects & Business Cases")
        for exp in data.get("Experience", []):
            role = exp.get('Role', '')
            company = exp.get('Company', '')
            duration = exp.get('Duration', '')
            
            st.markdown(f"**{role}** &nbsp;|&nbsp; *{company}* <span style='float:right;'>*{duration}*</span>", unsafe_allow_html=True)
            
            for ach in exp.get("Achievements", []):
                st.markdown(f"- {ach}")
            st.markdown("")
        
        st.markdown('<hr class="glow-divider" style="margin: 1.5rem 0;">', unsafe_allow_html=True)

        st.markdown("### 🛠️ Core Competencies")
        skills_html = "".join(f'<span class="skill-chip">{s}</span>' for s in data.get("Skills", []))
        st.markdown(skills_html, unsafe_allow_html=True)
        
        st.markdown('<hr class="glow-divider" style="margin: 1.5rem 0;">', unsafe_allow_html=True)

        st.markdown("### 🎓 Education & Professional Certifications")
        st.caption("Complete these free courses over the next 2 years to make this resume a reality!")
        for edu in data.get("Education", []):
            st.markdown(f"- **{edu}**")

def render_editable_fields(data: dict) -> dict:
    """Display editable Streamlit widgets pre-filled with AI output."""
    st.markdown("### ✏️ Customize Your Future Profile")
    st.caption("Fill in the blanks (like target companies or university names) before exporting.")

    edited = dict(data)

    with st.expander("👤 Contact Information", expanded=False):
        c1, c2 = st.columns(2)
        edited["Name"] = c1.text_input("Full Name", value=data.get("Name", ""), key="edit_name")
        edited["Email"] = c2.text_input("Email", value=data.get("Email", ""), key="edit_email")
        c3, c4 = st.columns(2)
        edited["Phone"] = c3.text_input("Phone", value=data.get("Phone", ""), key="edit_phone")
        edited["Location"] = c4.text_input("Location", value=data.get("Location", ""), key="edit_location")
        edited["LinkedIn"] = st.text_input("LinkedIn URL", value=data.get("LinkedIn", ""), key="edit_linkedin")

    with st.expander("📋 Executive Summary", expanded=False):
        edited["Summary"] = st.text_area(
            "Summary",
            value=data.get("Summary", ""),
            height=150,
            key="edit_summary",
        )

    with st.expander("💼 Strategic Projects & Business Cases", expanded=False):
        edited_exp: list[dict] = []
        for i, exp in enumerate(data.get("Experience", [])):
            st.markdown(f"**Project {i+1}**")
            ec1, ec2, ec3 = st.columns([3, 3, 2])
            role = ec1.text_input("Project Name", value=exp.get("Role", ""), key=f"role_{i}")
            company = ec2.text_input("Context (e.g. MBA Capstone)", value=exp.get("Company", ""), key=f"company_{i}")
            duration = ec3.text_input("Duration", value=exp.get("Duration", ""), key=f"duration_{i}")
            achievements_text = st.text_area(
                "Achievements (one per line)",
                value="\n".join(exp.get("Achievements", [])),
                height=180,
                key=f"achievements_{i}",
            )
            edited_exp.append({
                "Role": role,
                "Company": company,
                "Duration": duration,
                "Achievements": [a.strip() for a in achievements_text.split("\n") if a.strip()],
            })
            st.markdown("---")
        edited["Experience"] = edited_exp

    with st.expander("🛠️ Core Competencies", expanded=False):
        skills_text = st.text_area(
            "Skills (one per line)",
            value="\n".join(data.get("Skills", [])),
            height=150,
            key="edit_skills",
        )
        edited["Skills"] = [s.strip() for s in skills_text.split("\n") if s.strip()]

    with st.expander("🎓 Education & Certifications", expanded=False):
        edu_text = st.text_area(
            "Education (one per line)",
            value="\n".join(data.get("Education", [])),
            height=120,
            key="edit_education",
        )
        edited["Education"] = [e.strip() for e in edu_text.split("\n") if e.strip()]

    return edited
