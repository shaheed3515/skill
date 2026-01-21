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
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050a18; }
    .stApp { background: radial-gradient(circle at top right, #1e293b, #050a18); }
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.2em;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        border: none; color: white; font-weight: 700; transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4); }
</style>
""", unsafe_allow_html=True)

def go_to(step):
    st.session_state.step = step
    st.rerun()

# ---------------- MAIN APP ----------------
st.markdown("<h1 style='text-align: center; color: white;'>🎓 SkillBridge</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-top: -15px;'>Empowering Tier-2 & 3 Talent via Skill-First Matching</p>", unsafe_allow_html=True)

# 1. LOGIN PAGE
if st.session_state.step == "login":
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if lottie_coding: st_lottie(lottie_coding, height=180)
        st.subheader("Login to SkillBridge")
        st.text_input("Institutional Email")
        st.text_input("Password", type="password")
        if st.button("Sign In"): go_to("role")
        st.markdown('</div>', unsafe_allow_html=True)

# 2. ROLE SELECTION
elif st.session_state.step == "role":
    st.markdown("<h3 style='text-align: center; color: white;'>Select your portal</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.write("### 👨‍🎓 Student")
        if st.button("Find Internships"):
            st.session_state.user_data["role"] = "Student"
            go_to("student_profile")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.write("### 🏢 Employer")
        if st.button("Hire Talent"):
            st.session_state.user_data["role"] = "Employer"
            go_to("company_dashboard")
        st.markdown('</div>', unsafe_allow_html=True)

# 3. STUDENT PROFILE
elif st.session_state.step == "student_profile":
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Build Your Skill Profile")
        name = st.text_input("Full Name")
        clg = st.text_input("College Name")
        skills = st.multiselect("Select your technical stack", 
                               ["Python", "Java", "React", "SQL", "Tailwind", "Node.js", "Tableau", "AWS", "UI/UX"])
        
        if st.button("Scan Opportunities"):
            st.session_state.user_data.update({"name": name, "skills": skills, "college": clg})
            go_to("matching_loader")
        st.markdown('</div>', unsafe_allow_html=True)

# 4. MATCHING LOADER
elif st.session_state.step == "matching_loader":
    st.markdown('<div style="text-align: center; padding: 40px;">', unsafe_allow_html=True)
    if lottie_coding: st_lottie(lottie_coding, height=250)
    st.markdown("### Matching Skills to Global Roles...")
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    go_to("student_results")

# 5. STUDENT RESULTS (JOB BOARD)
elif st.session_state.step == "student_results":
    st.markdown(f"## 🎯 Matches for {st.session_state.user_data['name']}")
    
    jobs = [
        {"company": "CloudScale Inc.", "req": ["Python", "AWS", "SQL"], "role": "Backend Intern", "type": "Remote"},
        {"company": "PixelPerfect", "req": ["React", "Tailwind", "UI/UX"], "role": "Frontend Intern", "type": "Hybrid"},
        {"company": "DataViz Lab", "req": ["SQL", "Tableau", "Python"], "role": "Data Analyst Intern", "type": "Remote"},
        {"company": "InnoSoft", "req": ["Java", "SQL", "Node.js"], "role": "SDE Intern", "type": "Remote"}
    ]

    user_skills = st.session_state.user_data["skills"]
    
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        for job in jobs:
            matched, missing, score = calculate_match(user_skills, job["req"])
            if score >= 33: # Show jobs with at least 1 skill match
                st.markdown(f"""
                <div class="glass-card">
                    <h3 style="margin:0; color:#60a5fa;">{job['role']}</h3>
                    <p style="color:#94a3b8;">{job['company']} • {job['type']}</p>
                    <p><b>Match: {score}%</b></p>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Details & Skill Gaps"):
                    st.write(f"✅ Matched: {', '.join(matched)}")
                    if missing: st.warning(f"🚀 To hit 100%, learn: {', '.join(missing)}")
                    if st.button(f"Apply to {job['company']}", key=job['company']):
                        st.balloons()
    
    with col_side:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🤖 Career AI")
        st.write("Based on your profile, you are most competitive in **Backend Roles**.")
        st.info("Tip: Projects using SQL increase your hireability by 40%.")
        if st.button("Edit Profile"): go_to("student_profile")
        st.markdown('</div>', unsafe_allow_html=True)

# 6. EMPLOYER DASHBOARD
elif st.session_state.step == "company_dashboard":
    st.markdown("## 🏢 Employer Talent Discovery")
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Available Talent", "12.5k", "+8%")
    k2.metric("Verified Projects", "45k", "Live")
    k3.metric("Tier 2/3 Reach", "94%", "Global")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Filter Tier-2 & Tier-3 Talent")
    skill_filter = st.selectbox("Search Skill", ["Python", "React", "SQL", "Java"])
    score_filter = st.slider("Min Skill Score", 0, 100, 75)

    talent_data = pd.DataFrame({
        "Candidate": ["Arjun M.", "Sriya K.", "Rahul V.", "Ananya S."],
        "Location": ["Nagpur (T2)", "Madurai (T3)", "Lucknow (T2)", "Bhopal (T3)"],
        "Skill Score": [94, 91, 88, 85]
    })
    st.table(talent_data[talent_data["Skill Score"] >= score_filter])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Back to Role"): go_to("role")
