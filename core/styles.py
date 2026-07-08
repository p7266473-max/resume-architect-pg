import streamlit as st

def inject_custom_css():
    """Inject custom HTML & CSS styling into Streamlit."""
    st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #FAFAFA;
    color: #1A1A1A;
  }

  /* ---- Hero ---- */
  .hero-container {
    text-align: center;
    padding: 3rem 1rem 2rem;
    background: url('https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80') no-repeat center center;
    background-size: cover;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
    margin-bottom: 3rem;
    border: 1px solid #EAEAEA;
    position: relative;
    overflow: hidden;
  }
  
  .hero-overlay {
    background: rgba(255, 255, 255, 0.90);
    backdrop-filter: blur(10px);
    padding: 3.5rem 2rem;
    border-radius: 16px;
    margin: 1rem auto;
    max-width: 850px;
    border: 1px solid rgba(212, 175, 55, 0.4);
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  }

  .hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.8rem;
    font-weight: 700;
    color: #0A192F;
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin-bottom: 1rem;
  }
  
  .hero-title span {
    background: linear-gradient(135deg, #D4AF37 0%, #AA8000 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero-sub {
    font-size: 1.25rem;
    color: #4A5568;
    font-weight: 400;
    margin: 0 auto;
    max-width: 650px;
    line-height: 1.6;
  }

  /* ---- Primary button ---- */
  div.stButton > button {
    background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    padding: 1rem 2.5rem !important;
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    border-radius: 50px !important;
    width: 100% !important;
    box-shadow: 0 10px 25px rgba(212, 175, 55, 0.4) !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase;
  }
  div.stButton > button:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 15px 35px rgba(212, 175, 55, 0.6) !important;
  }
  div.stButton > button:active { transform: translateY(2px) !important; }

  /* ---- Download buttons ---- */
  div.stDownloadButton > button {
    background: #0A192F !important;
    color: #D4AF37 !important;
    border: 1px solid #D4AF37 !important;
    padding: 0.8rem 1.8rem !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    width: 100% !important;
    box-shadow: 0 8px 20px rgba(10, 25, 47, 0.15) !important;
    transition: all 0.25s ease !important;
  }
  div.stDownloadButton > button:hover {
    background: #112240 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 28px rgba(10, 25, 47, 0.25) !important;
  }

  /* ---- Sidebar ---- */
  section[data-testid="stSidebar"] {
    background: #F4F7F6;
    border-right: 1px solid #E2E8F0;
  }
  section[data-testid="stSidebar"] .stMarkdown {
    color: #2D3748;
  }

  /* ---- Text area & Multiselect ---- */
  .stTextArea textarea, .stMultiSelect div[data-baseweb="select"] {
    background: #FFFFFF !important;
    color: #1A202C !important;
    border-radius: 12px !important;
    font-size: 1.05rem !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
  }

  /* ---- Expander ---- */
  .streamlit-expanderHeader {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    color: #0A192F !important;
  }

  /* ---- Divider ---- */
  .glow-divider {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #D4AF37 30%, #AA8000 70%, transparent);
    margin: 2.5rem 0;
    opacity: 0.6;
  }

  /* ---- Tag chips ---- */
  .skill-chip {
    display: inline-block;
    background: #FDFBF7;
    color: #AA8000;
    border: 1px solid rgba(212, 175, 55, 0.4);
    border-radius: 999px;
    padding: 6px 18px;
    font-size: 0.9rem;
    font-weight: 600;
    margin: 4px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.02);
  }
  
  /* Additional polish */
  div[data-testid="stMarkdownContainer"] h2, div[data-testid="stMarkdownContainer"] h3, div[data-testid="stMarkdownContainer"] h4 {
    color: #0A192F !important;
    font-family: 'Playfair Display', serif;
  }
</style>
""", unsafe_allow_html=True)
