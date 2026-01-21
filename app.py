import streamlit as st
import pandas as pd
import time
import requests
from streamlit_lottie import st_lottie

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SkillBridge | Skill-Based Internship Matching",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------- ASSETS & HELPERS ----------------
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
lottie_analytics = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_qpwb7t6f.json")

def calculate_match(student_skills, required_skills):
    student_set = set([s.lower().strip() for s in student_skills])
    required_set = set([s.lower().strip() for s in required_skills])
    matched = list(student_set & required_set)
    missing = list(required_set - student_set)
    score = int((len(matched) / len(required_set)) * 100) if required_set else 0
    return matched, missing, score

# ---------------- SESSION STATE ----------------
if "step" not in st.session_state:
    st.session_state.step = "login"
if "user_data" not in st.session_state:
    st.session_state.user_data = {"name": "", "skills": [], "role": "", "college": ""}

# ---------------- MODERN CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #050a18;
    }

    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #050a18);
    }

    /* Glassmorphism Card */
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Professional Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.2em;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        border: none;
        color: white;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }

    .result-box {
        background: rgba(16, 185, 129, 0.1);
        border-left: 5px solid #10b981;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
def go_to(step):
    st.session_state.step = step
    st.rerun()

# ---------------- MAIN APP ----------------
st.markdown("<h1 style='text-align: center; color: white;'>🎓 SkillBridge</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-top: -15px;'>Connecting Tier-2 & 3 Talent to Global Opportunities</p>", unsafe_allow_html=True)

# 1. LOGIN PAGE
if st.session_state.step == "login":
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if lottie_coding: st_lottie(lottie_coding, height=180)
        st.subheader("Login to your Portal")
        st.text_input("Username / Email")
        st.text_input("Password", type="password")
        if st.button("Sign In"): go_to("role")
        st.markdown('</div>', unsafe_allow_html=True)

# 2. ROLE SELECTION
elif st.session_state.step == "role":
    st.markdown("<h3 style='text-align: center; color: white;'>Select your path</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.write("### 👨‍🎓")
        st.write("I am a Student")
        if st.button("Enter Student Hub"):
            st.session_state.user_data["role"] = "Student"
            go_to("student_profile")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.write("### 🏢")
        st.write("I am an Employer")
        if st.button("Enter Company Hub"):
            st.session_state.user_data["role"] = "Employer"
            go_to("company_dashboard")
        st.markdown('</div>', unsafe_allow_html=True)

# 3. STUDENT PROFILE INPUT
elif st.session_state.step == "student_profile":
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Personalize Your Skill Profile")
        name = st.text_input("Full Name")
        clg = st.text_input("College / Institute")
        skills = st.multiselect("Select your technical stack", 
                               ["Python", "Java", "React", "SQL", "Tailwind", "Node.js", "Tableau", "AWS"])
        
        if st.button("Analyze Matches"):
            st.session_state.user_data.update({"name": name, "skills": skills, "college": clg})
            go_to("matching_loader")
        st.markdown('</div>', unsafe_allow_html=True)

# 4. MATCHING LOADER
elif st.session_state.step == "matching_loader":
    st.markdown('<div style="text-align: center; padding: 40px;">', unsafe_allow_html=True)
    if lottie_coding: st_lottie(lottie_coding, height=250)
    st.markdown("### Scanning Remote Opportunities...")
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.015)
        progress_bar.progress(i + 1)
    go_to("student_results")

# 5. STUDENT RESULTS & CAREER ASSISTANT
elif st.session_state.step == "student_results":
    # Mock data for demonstration
    company_req = ["Python", "SQL", "AWS", "FastAPI"]
    matched, missing, score = calculate_match(st.session_state.user_data["skills"], company_req)
    
    st.markdown(f"## Welcome, {st.session_state.user_data['name']}!")
    
    # Sidebar Chatbot Career Assistant
    with st.sidebar:
        st.markdown("### 🤖 Career Assistant")
        st.info("I've reviewed your match with **CloudScale Inc.**")
        if missing:
            st.write(f"To reach 100% match, I recommend learning: **{', '.join(missing)}**")
            st.markdown("[Start Free Course on Coursera →](https://coursera.org)")
        else:
            st.success("Your profile is a perfect match! Ready for the interview?")
        
        st.divider()
        if st.button("Reset Session"): go_to("login")

    # Match Score Results
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Overall Match", f"{score}%")
        st.write("**Top Match:** CloudScale Inc.")
        st.write("**Role:** Backend Developer Intern")
        if st.button("Apply Instantly"):
            st.balloons()
            st.toast("Application submitted!")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("### Skill Breakdown")
        st.success(f"**Found:** {', '.join(matched) if matched else 'None'}")
        st.warning(f"**Missing:** {', '.join(missing) if missing else 'None'}")
        st.markdown('</div>', unsafe_allow_html=True)

# 6. EMPLOYER DASHBOARD
elif st.session_state.step == "company_dashboard":
    st.markdown("## 🏢 Talent Discovery Dashboard")
    
    # KPIs
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Tier-2/3 Talent", "8,450", "+14%")
    kpi2.metric("Verified Projects", "12.4k", "Live")
    kpi3.metric("Avg. Match Rate", "82%", "Optimal")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Filter Candidates by Performance")
    
    f_skill = st.selectbox("Desired Skillset", ["Python", "Data Science", "React", "DevOps"])
    f_score = st.slider("Min. Assessment Score", 0, 100, 80)

    # Mock Candidate Table
    talent_df = pd.DataFrame({
        "Candidate Name": ["Aarav Patel", "Meera Rao", "Ishaan Singh", "Sana Khan"],
        "Location": ["Nagpur (T2)", "Kochi (T2)", "Hubli (T3)", "Bhopal (T2)"],
        "Technical Score": [96, 92, 89, 84],
        "Verified Projects": [7, 4, 5, 8]
    })
    
    filtered_df = talent_df[talent_df["Technical Score"] >= f_score]
    st.dataframe(filtered_df, use_container_width=True)
    
    if st.button("Download Talent Reports"):
        st.success("Report generated for selected candidates.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Visualizing the Talent Pool
    
    st.write("### 📈 Talent Supply vs Industry Demand")
    chart_data = pd.DataFrame({
        "Skills": ["React", "Python", "SQL", "Cloud", "UI/UX"],
        "Student Supply": [90, 85, 70, 45, 60],
        "Industry Demand": [75, 95, 80, 85, 50]
    })
    st.line_chart(chart_data.set_index("Skills"))
    
    if st.button("← Back to Role"): go_to("role")
