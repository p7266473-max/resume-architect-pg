"""
Resume Architect PG (Streamlit Edition)
==============================================================
Production-ready Streamlit application that generates high-impact,
ATS-optimized resumes for PG (MBA) and UG students.
"""

import logging
import os
import json
import streamlit as st

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
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Resume Architect PG",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DATA STRUCTS
# ============================================================

THEMES = ["Classic Navy", "Slate Minimal", "Emerald Tech", "Burgundy Corporate"]

STREAM_DATA = {
    "Postgraduate (PG) - MBA": {
        "roles": [
            "MBA - Finance & Investment Banking",
            "MBA - Marketing & Brand Strategy",
            "MBA - Human Resource Management",
            "MBA - Operations & Supply Chain",
            "MBA - Systems & Business Analytics"
        ],
        "degree_placeholder": "Master of Business Administration (MBA)",
        "suggestions": {
            "MBA - Finance & Investment Banking": {
                "title": "MBA Candidate | Finance Specialist",
                "summary": "Analytical MBA candidate with a strong foundation in corporate finance, financial modeling, and investment banking principles. Proficient in performing company valuations using DCF and Comparable Company Analysis (CCA). Adept at translating complex financial data into strategic recommendations to optimize capital budgeting.",
                "bullets": [
                    "Constructed detailed three-statement financial models and projected future cash flows for valuations.",
                    "Analyzed capital structure optimization strategies, improving theoretical cost of capital by 40bps.",
                    "Conducted risk assessment reports for M&A scenarios, evaluating strategic synergies and premium pricing."
                ],
                "skills": ["Corporate Valuation", "Equity Analysis", "Asset Allocation", "Financial Modeling", "Bloomberg Terminal", "Excel VBA"]
            },
            "MBA - Marketing & Brand Strategy": {
                "title": "MBA Candidate | Marketing & Brand Strategist",
                "summary": "Creative and analytical MBA specializing in Marketing and Brand Management. Experienced in conducting customer acquisition cost (CAC) analyses, customer journey mapping, and digital campaign planning. Skilled at leveraging data analytics to craft high-conversion product positioning strategies.",
                "bullets": [
                    "Designed and executed comprehensive market research surveys, identifying key growth segments.",
                    "Formulated a go-to-market (GTM) strategy for a digital product launch, boosting target conversions by 15%.",
                    "Optimized social media campaign budgets, reducing overall customer acquisition cost (CAC) by 18%."
                ],
                "skills": ["Brand Architecture", "GTM Strategy", "Consumer Behavior", "Tableau", "Google Analytics", "SQL"]
            },
            "MBA - Human Resource Management": {
                "title": "MBA Candidate | Strategic HR Specialist",
                "summary": "People-centric MBA candidate specializing in Strategic Human Resources and Organizational Development. Proficient in designing talent acquisition pipelines, performance appraisal frameworks, and employee engagement programs. Committed to building diverse and high-performing workplace cultures.",
                "bullets": [
                    "Formulated structured competency mapping models for technical profiles, aligning hiring with corporate objectives.",
                    "Redesigned the onboarding workflow, reducing the employee attrition rate by 12% in the first quarter.",
                    "Analyzed annual performance appraisal data to identify training needs and gaps across core departments."
                ],
                "skills": ["Competency Mapping", "Talent Acquisition", "Employee Relations", "HRIS Tools", "Strategic Staffing", "Conflict Resolution"]
            },
            "MBA - Operations & Supply Chain": {
                "title": "MBA Candidate | Operations & Logistics Manager",
                "summary": "Process-oriented MBA candidate specializing in Operations Management and Logistics. Proficient in Six Sigma methodologies, bottleneck identification, and lean supply chain principles. Skilled in leveraging linear programming models to optimize distribution networks.",
                "bullets": [
                    "Mapped warehouse layouts and logistics workflows, enhancing daily order fulfillment speeds by 22%.",
                    "Managed inventory optimization audits using ABC analysis, reducing carrying costs by 15%.",
                    "Applied Lean principles to operational pipelines, eliminating redundant processing steps for faster delivery."
                ],
                "skills": ["Six Sigma", "Logistics Planning", "Inventory Control", "Process Mapping", "SAP ERP", "Linear Programming"]
            },
            "MBA - Systems & Business Analytics": {
                "title": "MBA Candidate | Business Systems Analyst",
                "summary": "Data-driven MBA candidate specializing in Business Analytics and Systems Management. Skilled in translating complex database inputs into readable business intelligence dashboards. Proficient in SQL, Tableau, and applying predictive analytical algorithms.",
                "bullets": [
                    "Developed dynamic Tableau dashboards tracking key operational KPIs, cutting weekly reporting time by 10 hours.",
                    "Formulated predictive customer churn models using regression analysis to support retention programs.",
                    "Coordinated cross-functional IT projects, managing sprints and product backlogs under Agile scrum methodologies."
                ],
                "skills": ["SQL", "Tableau", "Business Analytics", "Agile / Scrum", "Python", "Predictive Modeling"]
            }
        }
    },
    "Undergraduate (UG) - Streams": {
        "roles": [
            "BSc - Computer Science & IT",
            "BCom - Commerce & Accounting",
            "BSc - General & Life Sciences",
            "BA - Humanities & Arts",
            "BBA - Business Administration"
        ],
        "degree_placeholder": "Bachelor of Undergraduate Studies",
        "suggestions": {
            "BSc - Computer Science & IT": {
                "title": "Software Engineering Undergraduate",
                "summary": "Aspiring Software Engineer and Undergraduate student in Computer Science. Proficient in full-stack development, algorithms, and database management systems. Experienced in building scalable web solutions using modern programming architectures.",
                "bullets": [
                    "Designed and implemented RESTful APIs using Node.js and Express, enhancing backend scalability.",
                    "Developed a fully responsive web application with React.js, improving average user engagement times.",
                    "Optimized database queries in MySQL, reducing average load times by 20% on production systems."
                ],
                "skills": ["Python", "Java", "React.js", "SQL", "Git", "REST APIs", "Data Structures"]
            },
            "BCom - Commerce & Accounting": {
                "title": "B.Com Candidate | Accounting & Finance",
                "summary": "Detail-oriented Bachelor of Commerce student with solid knowledge in accounting principles, taxation guidelines, and corporate finance laws. Proficient in Tally ERP, Excel modeling, and preparing financial audit summaries.",
                "bullets": [
                    "Maintained ledger accounts and prepared general financial balance sheets for quarterly reviews.",
                    "Assisted in reviewing tax compliance worksheets, identifying opportunities for deduplication.",
                    "Conducted basic ratio analysis to assess liquidity and financial health of case study projects."
                ],
                "skills": ["Financial Accounting", "Corporate Law", "Taxation", "Tally ERP", "Excel Modeling", "Auditing"]
            },
            "BSc - General & Life Sciences": {
                "title": "B.Sc Undergraduate | Research & Data Analyst",
                "summary": "Methodical Bachelor of Science undergraduate with experience in statistical computing and data modeling. Proficient in running experimental trials, analyzing data arrays, and writing structured research reports.",
                "bullets": [
                    "Conducted structured statistical analysis on laboratory datasets using R programming and Python.",
                    "Authored research reports detailing chemical properties and presenting data trends in visual graphs.",
                    "Coordinated laboratory safety guidelines, ensuring compliance with academic protocols."
                ],
                "skills": ["R Programming", "Statistical Analysis", "Data Visualization", "Research Writing", "Laboratory Safety", "SPSS"]
            },
            "BA - Humanities & Arts": {
                "title": "BA Undergraduate | Content & Communications Specialist",
                "summary": "Creative Humanities and Arts student specializing in communication systems, media writing, and research methodology. Proficient in content creation, editing, and executing structured qualitative studies.",
                "bullets": [
                    "Published articles in the university newsletter, increasing student engagement by 25%.",
                    "Conducted qualitative field research surveys, presenting analytical findings at local student symposiums.",
                    "Managed social media copy and communication logs for student-led activities and events."
                ],
                "skills": ["Creative Writing", "Communications", "Social Media Copy", "Qualitative Research", "Public Relations", "Content Strategy"]
            },
            "BBA - Business Administration": {
                "title": "BBA Undergraduate | Management Associate",
                "summary": "Proactive Business Administration student with a foundation in sales strategy, project management, and business communication. Skilled in organizing campus-wide events and pitching client proposals.",
                "bullets": [
                    "Led a student task force of 12 peers to execute community service initiatives.",
                    "Managed marketing budgets for the annual college fest, securing corporate sponsorships of $5k+.",
                    "Coordinated product pitch decks for business competition presentations, winning top ranks."
                ],
                "skills": ["Management Strategy", "Sales Pitching", "Team Leadership", "Budgeting", "Project Coordination", "Public Speaking"]
            }
        }
    }
}

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #090b10;
    color: #f3f4f6;
  }

  /* ---- Hero ---- */
  .hero-container {
    text-align: center;
    padding: 3rem 1rem 2rem;
    background: #0f172a;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    margin-bottom: 3rem;
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
  }
  
  .hero-overlay {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(10px);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin: 1rem auto;
    max-width: 850px;
    border: 1px solid rgba(99, 102, 241, 0.4);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  }

  .hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin-bottom: 1rem;
  }
  
  .hero-title span {
    background: linear-gradient(135deg, #6366f1 0%, #10b981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero-sub {
    font-size: 1.2rem;
    color: #9ca3af;
    font-weight: 400;
    margin: 0 auto;
    max-width: 650px;
    line-height: 1.6;
  }

  /* ---- Primary button ---- */
  div.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    padding: 0.8rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    width: 100% !important;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3) !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase;
  }
  div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 28px rgba(99, 102, 241, 0.5) !important;
  }
  div.stButton > button:active { transform: translateY(1px) !important; }

  /* ---- Download buttons ---- */
  div.stDownloadButton > button {
    background: #0f172a !important;
    color: #818cf8 !important;
    border: 1px solid rgba(99, 102, 241, 0.4) !important;
    padding: 0.8rem 1.8rem !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    width: 100% !important;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.25s ease !important;
  }
  div.stDownloadButton > button:hover {
    background: #1e293b !important;
    transform: translateY(-2px) !important;
  }

  /* ---- Sidebar ---- */
  section[data-testid="stSidebar"] {
    background: #0b0e14;
    border-right: 1px solid rgba(255,255,255,0.08);
  }

  /* ---- Divider ---- */
  .glow-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #6366f1 30%, #10b981 70%, transparent);
    margin: 2.5rem 0;
    opacity: 0.6;
  }

  /* ---- Tag chips ---- */
  .skill-chip {
    display: inline-block;
    background: #1e293b;
    color: #818cf8;
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 999px;
    padding: 6px 18px;
    font-size: 0.9rem;
    font-weight: 600;
    margin: 4px;
  }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO HEADER
# ============================================================

st.markdown("""
<div class="hero-container">
  <div class="hero-overlay">
    <div class="hero-title">Resume Architect <span>PG & UG Suite</span></div>
    <p class="hero-sub">Generate high-impact, ATS-optimized resumes specifically tailored for MBA Candidates and Undergraduate Students. Craft your industry-aligned profile instantly.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# STATE PERSISTENCE
# ============================================================

if "resume_data" not in st.session_state:
    st.session_state["resume_data"] = {
        "Name": "Alexander Morgan",
        "Email": "alex.morgan@domain.com",
        "Phone": "+1 (312) 442-9901",
        "Location": "Chicago, IL",
        "LinkedIn": "linkedin.com/in/alexmorgan",
        "GitHub": "github.com/alexmorgan-dev",
        "Title": "MBA Candidate | Finance Specialist",
        "Summary": "Analytical MBA candidate with a strong foundation in corporate finance, financial modeling, and investment banking principles. Proficient in performing company valuations using DCF and Comparable Company Analysis (CCA). Adept at translating complex financial data into strategic recommendations to optimize capital budgeting.",
        "Experience": [
            {
                "Role": "Investment Analyst (Intern)",
                "Company": "Apex Advisory Group",
                "Duration": "June 2024 - August 2024",
                "Achievements": [
                    "Constructed detailed three-statement financial models and projected future cash flows for valuations.",
                    "Analyzed capital structure optimization strategies, improving theoretical cost of capital by 40bps.",
                    "Conducted risk assessment reports for M&A scenarios, evaluating strategic synergies and premium pricing."
                ]
            }
        ],
        "Education": [
            {
                "Degree": "MBA - Specialization in Finance & Investment Banking",
                "School": "Kellogg School of Management",
                "Location": "Evanston, IL",
                "GPA": "3.8/4.0",
                "Year": "2026"
            }
        ],
        "Skills": ["Corporate Valuation", "Equity Analysis", "Asset Allocation", "Financial Modeling", "Bloomberg Terminal", "Excel VBA"],
        "Certs": ["CFA Level 1 Candidate", "Project Management Professional (PMP)"],
        "Awards": ["Recipient of Dean's List Award (2024)", "Academic Merit Scholarship"]
    }

# ============================================================
# SIDEBAR / CONTROLS
# ============================================================

st.sidebar.markdown("## ⚙️ Configuration")

selected_stream_cat = st.sidebar.selectbox(
    "1. Choose Stream Category",
    options=list(STREAM_DATA.keys())
)

available_roles = STREAM_DATA[selected_stream_cat]["roles"]
selected_role = st.sidebar.selectbox(
    "2. Choose Specialization / Branch",
    options=available_roles
)

selected_theme = st.sidebar.selectbox(
    "3. Output Design Theme",
    options=THEMES
)

load_preset = st.sidebar.button("🚀 Load Preset Suggestion")

if load_preset:
    stream_obj = STREAM_DATA[selected_stream_cat]
    preset = stream_obj["suggestions"].get(selected_role)
    if preset:
        st.session_state["resume_data"]["Title"] = preset["title"]
        st.session_state["resume_data"]["Summary"] = preset["summary"]
        st.session_state["resume_data"]["Skills"] = preset["skills"]
        
        # Override experience and education targets
        st.session_state["resume_data"]["Experience"] = [{
            "Role": preset["title"].split("|")[1].strip() if "|" in preset["title"] else preset["title"],
            "Company": "Elite Partners Group",
            "Duration": "Summer 2025",
            "Achievements": preset["bullets"]
        }]
        
        st.session_state["resume_data"]["Education"] = [{
            "Degree": selected_role if "MBA" in selected_role else stream_obj["degree_placeholder"],
            "School": "Premier Academic Institute",
            "Location": "New York, NY",
            "GPA": "3.9/4.0",
            "Year": "2026"
        }]
        st.sidebar.success("Loaded values!")

# ============================================================
# WORKSPACE WIDGETS
# ============================================================

st.markdown("## ✏️ Workspace Builder")

c1, c2 = st.columns(2)
with c1:
    with st.expander("👤 Contact Details", expanded=True):
        st.session_state["resume_data"]["Name"] = st.text_input("Full Name", value=st.session_state["resume_data"]["Name"])
        st.session_state["resume_data"]["Title"] = st.text_input("Profile Subtitle", value=st.session_state["resume_data"]["Title"])
        st.session_state["resume_data"]["Email"] = st.text_input("Email", value=st.session_state["resume_data"]["Email"])
        st.session_state["resume_data"]["Phone"] = st.text_input("Phone Number", value=st.session_state["resume_data"]["Phone"])
        st.session_state["resume_data"]["Location"] = st.text_input("City, Country", value=st.session_state["resume_data"]["Location"])
        st.session_state["resume_data"]["LinkedIn"] = st.text_input("LinkedIn Profile", value=st.session_state["resume_data"]["LinkedIn"])
        st.session_state["resume_data"]["GitHub"] = st.text_input("GitHub / Portfolio", value=st.session_state["resume_data"]["GitHub"])

    with st.expander("📝 Career Summary", expanded=True):
        st.session_state["resume_data"]["Summary"] = st.text_area(
            "Summary Narrative", value=st.session_state["resume_data"]["Summary"], height=120
        )

with c2:
    with st.expander("🎓 Education Details", expanded=True):
        edu_list = []
        for i, edu in enumerate(st.session_state["resume_data"].get("Education", [])):
            st.markdown(f"**Academic Record {i+1}**")
            degree = st.text_input("Degree / Branch", value=edu.get("Degree", ""), key=f"edu_deg_{i}")
            school = st.text_input("School / University", value=edu.get("School", ""), key=f"edu_sch_{i}")
            loc = st.text_input("Location", value=edu.get("Location", ""), key=f"edu_loc_{i}")
            gpa = st.text_input("GPA / Grade", value=edu.get("GPA", ""), key=f"edu_gpa_{i}")
            year = st.text_input("Passing Year", value=edu.get("Year", ""), key=f"edu_yr_{i}")
            edu_list.append({
                "Degree": degree,
                "School": school,
                "Location": loc,
                "GPA": gpa,
                "Year": year
            })
        st.session_state["resume_data"]["Education"] = edu_list

with st.expander("💼 Experience & Key Achievements", expanded=True):
    exp_list = []
    for i, exp in enumerate(st.session_state["resume_data"].get("Experience", [])):
        st.markdown(f"**Experience / Project Entry {i+1}**")
        ec1, ec2, ec3 = st.columns([3, 3, 2])
        role = ec1.text_input("Role / Project Name", value=exp.get("Role", ""), key=f"exp_role_{i}")
        company = ec2.text_input("Company / Context", value=exp.get("Company", ""), key=f"exp_comp_{i}")
        duration = ec3.text_input("Duration / Period", value=exp.get("Duration", ""), key=f"exp_dur_{i}")
        
        ach_text = st.text_area(
            "Achievements (One bullet point per line)", 
            value="\n".join(exp.get("Achievements", [])),
            key=f"exp_ach_{i}",
            height=120
        )
        bullets = [line.strip() for line in ach_text.split("\n") if line.strip()]
        exp_list.append({
            "Role": role,
            "Company": company,
            "Duration": duration,
            "Achievements": bullets
        })
    st.session_state["resume_data"]["Experience"] = exp_list

with st.expander("🛠️ Competencies & Certifications", expanded=True):
    cols = st.columns(2)
    with cols[0]:
        skills_raw = st.text_area(
            "Skills (Comma separated list)",
            value=", ".join(st.session_state["resume_data"].get("Skills", []))
        )
        st.session_state["resume_data"]["Skills"] = [s.strip() for s in skills_raw.split(",") if s.strip()]
    with cols[1]:
        certs_raw = st.text_area(
            "Certifications (Comma separated list)",
            value=", ".join(st.session_state["resume_data"].get("Certs", []))
        )
        st.session_state["resume_data"]["Certs"] = [c.strip() for c in certs_raw.split(",") if c.strip()]
        
        awards_raw = st.text_area(
            "Awards & Honors (Comma separated list)",
            value=", ".join(st.session_state["resume_data"].get("Awards", []))
        )
        st.session_state["resume_data"]["Awards"] = [a.strip() for a in awards_raw.split(",") if a.strip()]

# ============================================================
# LIVE RENDER
# ============================================================

st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
st.markdown("## 📄 Real-time A4 Live Preview")

data = st.session_state["resume_data"]

# Map theme colors
theme_styles = {
    "Classic Navy": {"heading": "#0f172a", "accent": "#1e3a8a", "border": "#cbd5e1"},
    "Slate Minimal": {"heading": "#1e293b", "accent": "#475569", "border": "#e2e8f0"},
    "Emerald Tech": {"heading": "#064e3b", "accent": "#047857", "border": "#d1fae5"},
    "Burgundy Corporate": {"heading": "#4c0519", "accent": "#9d174d", "border": "#fce7f3"}
}
style = theme_styles[selected_theme]

preview_html = f"""
<div style="background-color: white; color: #1f2937; padding: 25px; border-radius: 8px; border: 1px solid {style['border']}; font-family: 'Inter', sans-serif; line-height: 1.4; max-width: 900px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
    <div style="text-align: center; border-bottom: 2px solid {style['heading']}; padding-bottom: 10px; margin-bottom: 15px;">
        <h1 style="color: {style['heading']}; margin: 0; font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 700;">{data.get('Name', '')}</h1>
        <div style="color: {style['accent']}; font-size: 14px; font-weight: 600; text-transform: uppercase; margin-top: 4px;">{data.get('Title', '')}</div>
        <div style="color: #4b5563; font-size: 12px; margin-top: 6px;">
            {data.get('Location', '')} &nbsp;|&nbsp; {data.get('Phone', '')} &nbsp;|&nbsp; {data.get('Email', '')}
        </div>
        <div style="color: #4b5563; font-size: 12px; margin-top: 2px;">
            {data.get('LinkedIn', '')} &nbsp;|&nbsp; {data.get('GitHub', '')}
        </div>
    </div>
    
    <div style="margin-bottom: 15px; font-size: 13px; color: #374151; text-align: justify;">
        {data.get('Summary', '')}
    </div>
"""

# Render Education
if data.get("Education"):
    preview_html += f"""
    <div style="margin-bottom: 15px;">
        <h3 style="color: {style['heading']}; border-bottom: 1px solid #d1d5db; padding-bottom: 2px; margin-top: 15px; margin-bottom: 8px; font-size: 15px; text-transform: uppercase;">Education</h3>
    """
    for edu in data.get("Education", []):
        preview_html += f"""
        <div style="margin-bottom: 6px; font-size: 13px;">
            <div style="display: flex; justify-content: space-between; font-weight: 700; color: #111827;">
                <span>{edu.get('Degree', '')}</span>
                <span>{edu.get('Year', '')}</span>
            </div>
            <div style="display: flex; justify-content: space-between; color: #4b5563; font-style: italic;">
                <span>{edu.get('School', '')}, {edu.get('Location', '')}</span>
                <span>{edu.get('GPA') if edu.get('GPA') else ''}</span>
            </div>
        </div>
        """
    preview_html += "</div>"

# Render Experience
if data.get("Experience"):
    preview_html += f"""
    <div style="margin-bottom: 15px;">
        <h3 style="color: {style['heading']}; border-bottom: 1px solid #d1d5db; padding-bottom: 2px; margin-top: 15px; margin-bottom: 8px; font-size: 15px; text-transform: uppercase;">Experience</h3>
    """
    for exp in data.get("Experience", []):
        bullets_html = "".join(f"<li style='margin-bottom: 2px;'>{ach}</li>" for ach in exp.get("Achievements", []))
        preview_html += f"""
        <div style="margin-bottom: 8px; font-size: 13px;">
            <div style="display: flex; justify-content: space-between; font-weight: 700; color: #111827;">
                <span>{exp.get('Role', '')}</span>
                <span>{exp.get('Duration', '')}</span>
            </div>
            <div style="color: #4b5563; font-style: italic; margin-bottom: 4px;">{exp.get('Company', '')}</div>
            <ul style="margin: 0; padding-left: 20px; color: #374151;">
                {bullets_html}
            </ul>
        </div>
        """
    preview_html += "</div>"

# Skills and Certifications
preview_html += f"""
    <div style="margin-bottom: 15px;">
        <h3 style="color: {style['heading']}; border-bottom: 1px solid #d1d5db; padding-bottom: 2px; margin-top: 15px; margin-bottom: 8px; font-size: 15px; text-transform: uppercase;">Skills & Competencies</h3>
        <div style="font-size: 13px; color: #374151; display: grid; grid-template-columns: 150px 1fr; gap: 6px;">
            <strong style="color: #111827;">Core Skills:</strong>
            <span>{", ".join(data.get('Skills', []))}</span>
            
            <strong style="color: #111827;">Certifications:</strong>
            <span>{", ".join(data.get('Certs', []))}</span>
            
            <strong style="color: #111827;">Honors & Leadership:</strong>
            <span>{", ".join(data.get('Awards', []))}</span>
        </div>
    </div>
</div>
"""

st.markdown(preview_html, unsafe_allow_html=True)

# ============================================================
# EXPORT EXPORTS
# ============================================================

st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
st.markdown("## 📥 Export Outputs")

# 1. Generate Markdown content
md_content = f"""# {data.get('Name', '')}
**{data.get('Title', '')}**  
{data.get('Location', '')} | {data.get('Phone', '')} | {data.get('Email', '')} | {data.get('LinkedIn', '')} | {data.get('GitHub', '')}

## Executive Summary
{data.get('Summary', '')}

## Education
"""
for edu in data.get("Education", []):
    md_content += f"- **{edu.get('Degree', '')}** | {edu.get('School', '')} ({edu.get('Year', '')}) - GPA: {edu.get('GPA', '')}\n"

md_content += "\n## Professional Experience\n"
for exp in data.get("Experience", []):
    md_content += f"### {exp.get('Role', '')} - {exp.get('Company', '')} ({exp.get('Duration', '')})\n"
    for ach in exp.get("Achievements", []):
        md_content += f"- {ach}\n"

md_content += "\n## Skills & Competencies\n"
md_content += f"- **Skills**: {', '.join(data.get('Skills', []))}\n"
md_content += f"- **Certifications**: {', '.join(data.get('Certs', []))}\n"
md_content += f"- **Honors**: {', '.join(data.get('Awards', []))}\n"


# 2. Plain Text
plain_text = f"""{data.get('Name', '').upper()}
{data.get('Title', '')}
-----------------------------------------------------------
Contact: {data.get('Location', '')} | {data.get('Phone', '')} | {data.get('Email', '')}
Profiles: {data.get('LinkedIn', '')} | {data.get('GitHub', '')}

SUMMARY:
{data.get('Summary', '')}

EDUCATION:
"""
for edu in data.get("Education", []):
    plain_text += f"- {edu.get('Degree', '')}, {edu.get('School', '')} ({edu.get('Year', '')}) GPA: {edu.get('GPA', '')}\n"

plain_text += "\nEXPERIENCE:\n"
for exp in data.get("Experience", []):
    plain_text += f"\n* {exp.get('Role', '')} at {exp.get('Company', '')} ({exp.get('Duration', '')})\n"
    for ach in exp.get("Achievements", []):
        plain_text += f"  - {ach}\n"

plain_text += f"\nSKILLS: {', '.join(data.get('Skills', []))}"
plain_text += f"\nCERTIFICATIONS: {', '.join(data.get('Certs', []))}"
plain_text += f"\nAWARDS: {', '.join(data.get('Awards', []))}"


col1, col2 = st.columns(2)
with col1:
    st.download_button(
        label="📝 Download Markdown (.md)",
        data=md_content.encode("utf-8"),
        file_name="Resume.md",
        mime="text/markdown"
    )
with col2:
    st.download_button(
        label="📃 Download Plain Text (.txt)",
        data=plain_text.encode("utf-8"),
        file_name="Resume_ATS.txt",
        mime="text/plain"
    )
