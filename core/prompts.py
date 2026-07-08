from google.genai import types

APP_TITLE = "Future Resume Architect (PG Edition)"
APP_SUBTITLE = "Design your career path. Generate the elite PG/MBA resume you'll have in 3 years."
APP_ICON = "🚀"
GEMINI_MODEL = "gemini-2.5-flash"

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2.0

THEMES = ["Classic-Executive", "Modern-Tech", "ATS-Friendly"]

THEME_COLORS = {
    "Classic-Executive": {
        "heading": (26, 26, 46),
        "subheading": (45, 58, 74),
        "accent": (139, 111, 71),
    },
    "Modern-Tech": {
        "heading": (108, 92, 231),
        "subheading": (0, 184, 148),
        "accent": (13, 149, 232),
    },
    "ATS-Friendly": {
        "heading": (0, 0, 0),
        "subheading": (51, 51, 51),
        "accent": (68, 68, 68),
    },
}

CAREER_OPTIONS = [
    "Management Consultant",
    "Investment Banking Associate",
    "Private Equity / Venture Capital Associate",
    "Product Manager (Strategic)",
    "Corporate Strategy Associate",
    "Business / Systems Analyst",
    "Financial Analyst & Modeler",
    "Marketing & Brand Strategist",
    "Operations & Supply Chain Manager",
    "HR Specialist & Talent Partner"
]

# Gemini response schema for structured output
RESUME_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "Name": types.Schema(type=types.Type.STRING, description="Full candidate name, or '[Your Name]' if not found"),
        "Email": types.Schema(type=types.Type.STRING, description="Email address, or '[Your Email Address]'"),
        "Phone": types.Schema(type=types.Type.STRING, description="Phone number, or '[Your Phone Number]'"),
        "LinkedIn": types.Schema(type=types.Type.STRING, description="LinkedIn URL, or '[Your LinkedIn Profile URL]'"),
        "Location": types.Schema(type=types.Type.STRING, description="City/Country, or '[Your City, State]'"),
        "Summary": types.Schema(type=types.Type.STRING, description="A highly ambitious, forward-looking summary of a recent PG/MBA graduate."),
        "Experience": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "Role": types.Schema(type=types.Type.STRING, description="Name of the Business Case / Project (e.g. 'Valuation & Advisory Report', 'Market Entry Strategy Campaign')"),
                    "Company": types.Schema(type=types.Type.STRING, description="Context (e.g. 'MBA Capstone Project', 'Consulting Case Study')"),
                    "Duration": types.Schema(type=types.Type.STRING, description="e.g. 'Jan 2026 - May 2026' or '2025 - 2026' (DO NOT use Spring/Fall/Summer)"),
                    "Achievements": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING),
                    ),
                },
                required=["Role", "Company", "Duration", "Achievements"],
            ),
        ),
        "Skills": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(type=types.Type.STRING),
        ),
        "Education": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(type=types.Type.STRING),
        ),
    },
    required=["Name", "Email", "Phone", "LinkedIn", "Location", "Summary", "Experience", "Skills", "Education"],
)

PASS1_SYSTEM_PROMPT = """You are a "Future Career Architect". 
Your user is currently a Postgraduate / MBA student. They have selected up to 3 target roles they want to achieve in the next 2-3 years.
Your job is to generate their FUTURE resume—the exact elite resume they will have 3 years from now as a PG / MBA GRADUATE (fresher).

CRITICAL RULES:
1. NO CORPORATE HALLUCINATIONS: This is a postgraduate fresher's resume. DO NOT hallucinate past corporate internships, real job titles at top companies, or fabricated corporate history unless related to actual projects.
2. BUSINESS CASE PROJECTS INSTEAD OF JOBS: Use the "Experience" array to outline 2 to 3 massive CONSULTING PROJECTS, CAPSTONE BUSINESS STUDIES, or STRATEGIC CASE ANALYSIS projects the student should perform over the next 2 years to master the skills needed for their target roles. 
   - Role = Project/Case Study Name (e.g. "Brand Architecture & Competitor Analysis")
   - Company = Project Context (e.g. "MBA Capstone Project" or "Case Study Seminar")
   - Achievements = Describe the strategic framework, tools used (e.g., SWOT, DCF, Six Sigma), and what they resolved/designed to learn.
3. LOCALIZATION (MALAYSIA): The user is in Malaysia. ABSOLUTELY DO NOT use US seasonal terms (Spring, Fall, Summer, Winter) for dates. Use specific months (e.g., "Jan 2026 - May 2026") or just years (e.g., "2025 - 2026"). 
4. EDUCATION: Must include "Master of Business Administration (MBA) - [Insert University Name]" or similar postgraduate degree. Leave gaps for their actual university. For graduation dates, use "Expected 2027" (NO seasons).
5. CERTIFICATIONS: Based on the web research provided, list 3 to 4 REAL, highly-regarded FREE or Open-Source business/analytics certifications (e.g. Scrum Alliance, Google Project Management, Corporate Finance Institute free courses) that they MUST take in the next 2 years. Present them as if they have already completed them in the future.
6. PERSONAL DETAILS: Use placeholders like "[Your Name]", "[Your Email]".
7. TONE: Strategic, professional, leadership-oriented, highly competent recent PG graduate, focused on what they have ANALYZED, SOLVED and MANAGED."""

PASS1_USER_TEMPLATE = """You are provided with web research on the best free/open-source certifications and courses for the user's target roles.

WEB RESEARCH INSIGHTS (FREE COURSES):
\"\"\"
{research_summary}
\"\"\"

TARGET FUTURE ROLES:
\"\"\"
{target_roles}
\"\"\"

Generate the complete FUTURE resume json based on the guidelines. Do NOT hallucinate corporate experience. Focus the Experience section entirely on impressive Business Case Studies and Projects they should execute."""

PASS2_SYSTEM_PROMPT = """You are an elite resume editor.
You receive a JSON object of a 'future resume' for a PG/MBA graduate aiming for top corporate/strategic roles.

RULES:
- Return the EXACT same JSON schema.
- Elevate the professional business vocabulary to describe their PROJECTS. Make the project descriptions sound technically rigorous (mentioning framework names, financial modeling tools, or strategic analysis methodologies).
- ABSOLUTELY NO CORPORATE HALLUCINATIONS: Do not change projects into fake corporate roles. Ensure it reads like the resume of an exceptional, self-driven postgraduate.
- Keep all placeholders (like [Insert University Name]) completely intact."""

PASS2_USER_TEMPLATE = """Elevate this future resume JSON for a top-tier postgraduate.
Do NOT change the schema. Do NOT hallucinate corporate work experience. Only enhance the project descriptions.

{input_json}"""
