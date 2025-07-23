import streamlit as st
from resume_parser import parse_resume
from job_parser import parse_job_description
from skill_comparator import compare_skills, get_partial_matches
from recommender import generate_recommendations
from utils import extract_skills_from_text
import re
from collections import Counter
import plotly.graph_objects as go

# Set Streamlit theme and page config
st.set_page_config(
    page_title="SkillShift – Real-Time Skill Gap Analyzer",
    page_icon="🧠",
    layout="wide"
)

# Simple logo
st.markdown("## SS")

st.markdown("""
# SkillShift – Real-Time Skill Gap Analyzer

*Empowering your career growth with AI-driven insights*
---
""")

st.header("1. Upload Your Resume")
resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
resume_text = None
resume_skills = []
raw_skills_section = None
if resume_file:
    st.success(f"Uploaded: {resume_file.name}")
    temp_resume_path = f"temp_resume.{resume_file.type.split('/')[-1]}"
    with open(temp_resume_path, "wb") as f:
        f.write(resume_file.getbuffer())
    try:
        resume_text, resume_skills, raw_skills_section = parse_resume(temp_resume_path)
        st.subheader("Extracted Resume Text:")
        st.text_area("Resume Content", resume_text, height=200)
        st.subheader("Raw Extracted Skills Section:")
        if raw_skills_section:
            st.code(raw_skills_section)
        else:
            st.info("No 'Skills' section detected.")
        st.subheader("Extracted Resume Skills:")
        if resume_skills:
            st.write(", ".join([s.title() for s in resume_skills]))
        else:
            st.info("No skills detected in resume. (Try using a more standard 'Skills' section or check the skill list in utils.py)")
    except Exception as e:
        st.error(f"Error parsing resume: {e}")

st.header("2. Paste Job Description Text")
jd_text_input = st.text_area("Paste Job Description Text Here", height=200)
jd_text = None
jd_skills = []
top_keywords = []

st.header("3. Specify Your Target Role")
target_role = st.text_input("Enter your target role (e.g., Data Scientist, Software Engineer, Product Manager)", placeholder="Data Scientist")

process_jd = st.button("Submit Job Description")
if process_jd and jd_text_input.strip():
    jd_text = jd_text_input
    jd_skills = extract_skills_from_text(jd_text)
    st.success("Job description text provided.")
    
    st.subheader("Extracted Job Description Skills:")
    if jd_skills:
        st.write(", ".join([s.title() for s in jd_skills]))
    else:
        st.info("No skills detected in job description text.")
    st.subheader("Top Keywords in Job Description:")
    words = re.findall(r'\b\w+\b', jd_text.lower())
    stopwords = set(['the','and','to','of','in','a','for','on','with','as','is','by','or','be','are','at','an','from','that','this','will','can','has','have','it','was','but','not','if','their','they','we','you','your','our','all','may','who','which','so','such','more','than','other','any','do','does','should','must','were','been','being','into','about','also','these','those','each','per','its','no','yes','i','ii','iii','iv','v','vi','vii','viii','ix','x'])
    filtered = [w for w in words if w not in stopwords and len(w) > 2]
    top_keywords = [w for w, _ in Counter(filtered).most_common(10)]
    if top_keywords:
        st.write(", ".join([w.title() for w in top_keywords]))
    else:
        st.info("No significant keywords found.")

if resume_skills and jd_skills:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.header("4. Skill Gap Analysis")
    comparison = compare_skills(resume_skills, jd_skills)
    st.subheader("Skills Present in Resume:")
    if comparison['present']:
        st.success(", ".join([s.title() for s in comparison['present']]))
    else:
        st.info("No job description skills found in resume.")
    st.subheader("Missing Skills (Required by Job, Not in Resume):")
    if comparison['missing']:
        st.warning(", ".join([s.title() for s in comparison['missing']]))
    else:
        st.success("No missing skills! Your resume covers all listed job skills.")

    st.subheader("Skill Radar Chart")
    all_skills = sorted(set([s.title() for s in jd_skills + resume_skills]))
    resume_vector = [1 if s.lower() in [r.lower() for r in resume_skills] else 0 for s in all_skills]
    jd_vector = [1 if s.lower() in [j.lower() for j in jd_skills] else 0 for s in all_skills]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=resume_vector, theta=all_skills, fill='toself', name='Resume'))
    fig.add_trace(go.Scatterpolar(r=jd_vector, theta=all_skills, fill='toself', name='Job Description'))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,1])),
        showlegend=True,
        height=500,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Skill Fit Progress Bars")
    if len(jd_skills) > 0:
        skill_fit = len(comparison['present']) / len(jd_skills)
    else:
        skill_fit = 0
    st.progress(skill_fit, text=f"{int(skill_fit*100)}% of job skills present in resume")
    if len(resume_skills) > 0:
        resume_relevance = len(comparison['present']) / len(resume_skills)
    else:
        resume_relevance = 0
    st.progress(resume_relevance, text=f"{int(resume_relevance*100)}% of your resume skills match the job")

    if comparison['missing']:
        st.subheader("Dynamic Learning Path")
        recs_and_path = generate_recommendations(comparison['missing'], jd_skills)
        learning_path = recs_and_path.get('learning_path', [])
        if learning_path:
            for step in learning_path:
                st.markdown(f"- {step}")

    if comparison['missing'] and resume_text and jd_text and target_role:
        from recommender import generate_llm_feedback, generate_role_advice
        st.subheader("AI-Powered Resume Feedback")
        with st.spinner("Generating feedback..."):
            feedback = generate_llm_feedback(resume_text, jd_text, comparison['missing'])
        st.markdown(feedback)

        st.subheader("Role-Specific Advice")
        with st.spinner("Generating role-specific advice..."):
            advice = generate_role_advice(jd_text, comparison['missing'], target_role)
        st.markdown(advice)

    if comparison['missing']:
        st.header("5. Upskilling Recommendations")
        recommendations = recs_and_path['recommendations'] if 'recommendations' in recs_and_path else generate_recommendations(comparison['missing'])
        for skill, recs in recommendations.items():
            st.markdown(f"**{skill.title()}**")
            for rec in recs:
                st.markdown(f"- {rec}")

    from utils import generate_pdf_report
    if st.button("Download PDF Report"):
        radar_chart_path = "radar_chart.png"
        fig.write_image(radar_chart_path)
        pdf_path = generate_pdf_report(
            resume_text=resume_text,
            jd_text=jd_text,
            present_skills=comparison['present'],
            missing_skills=comparison['missing'],
            learning_path=recs_and_path.get('learning_path', []),
            ai_feedback=feedback if 'feedback' in locals() else '',
            role_advice=advice if 'advice' in locals() else '',
            radar_chart_path=radar_chart_path
        )
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name="SkillShift_Report.pdf",
                mime="application/pdf"
            )
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
<center><sub>SkillShift &copy; 2024 | Empowering your career with AI | Developed by Chandana Gangaraju</sub></center>
""", unsafe_allow_html=True) 