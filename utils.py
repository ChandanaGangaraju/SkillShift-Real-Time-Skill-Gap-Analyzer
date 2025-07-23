# Expanded list of common technical and soft skills (user-provided and common variants)
COMMON_SKILLS = [
    # Programming Languages
    'python', 'sql', 'r', 'javascript', 'xml', 'scala', 'bash',
    # Data Analysis & Reporting
    'excel', 'tableau', 'power bi', 'business objects', 'a/b testing', 'statistical analysis', 'spss', 'sas',
    # Databases
    'postgresql', 'sql server', 'mysql', 'mongodb', 'cassandra', 'snowflake', 'amazon aurora', 'oracle', 'hive',
    # ETL & Big Data Tools
    'apache spark', 'pyspark', 'hadoop', 'airflow', 'aws emr', 'aws s3', 'amazon aurora',
    # Frameworks & Libraries
    'pandas', 'numpy', 'scikit-learn', 'scikit learn', 'xgboost', 'tensorflow', 'pytorch', 'keras', 'transformers', 'clip', 'bert', 'u-net', 'opencv', 'nltk', 'spacy', 'mllib', 'prophet', 'arima', 'sarima',
    # Tools & Platforms
    'aws', 'git', 'gitlab', 'gitlab ci/cd', 'docker', 'jupyter', 'gradio', 'lucidchart', 'superset', 'looker', 'qgis', 'databricks', 'github', 'bitbucket', 'jenkins', 'jira',
    # Visualization & Dashboarding
    'tableau', 'power bi', 'excel (pivot tables, macros)', 'superset', 'looker',
    # Process Modeling & Documentation
    'lucidchart', 'youtrack', 'agile', 'scrum', 'business process mapping', 'cost-benefit analysis',
    # Machine Learning/AI
    'machine learning', 'deep learning', 'ml', 'ai', 'generative ai', 'nlp', 'drift detection', 'error analysis',
    # Cloud
    'azure', 'gcp', 'oci',
    # Other
    'object oriented programming', 'functional programming', 'quality assurance', 'data pipelines', 'model creation', 'production environments', 'data science', 'big data', 'data analysis', 'data scientist',
    # Soft Skills
    'communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking', 'adaptability', 'creativity', 'time management', 'collaboration', 'project management', 'presentation', 'negotiation', 'empathy', 'organization',
]

import re
from fpdf import FPDF

def extract_skills_from_text(text, skills_list=COMMON_SKILLS):
    """Extract skills from text using case-insensitive substring matching."""
    found_skills = set()
    text_lower = text.lower()
    for skill in skills_list:
        if skill.lower() in text_lower:
            found_skills.add(skill)
    return sorted(found_skills)

def extract_job_title(jd_text):
    """
    Extract job title from job description text using regex patterns and common job titles.
    """
    # Common job title patterns
    patterns = [
        r'(?:job title|position|role|title)[:\s]+([A-Z][A-Za-z\s]+(?:Engineer|Scientist|Manager|Analyst|Developer|Architect|Lead|Specialist|Consultant|Coordinator|Director|VP|CTO|CEO|CFO|COO))',
        r'(?:we are looking for|seeking|hiring)[\s\w]+([A-Z][A-Za-z\s]+(?:Engineer|Scientist|Manager|Analyst|Developer|Architect|Lead|Specialist|Consultant|Coordinator|Director|VP|CTO|CEO|CFO|COO))',
        r'([A-Z][A-Za-z\s]+(?:Engineer|Scientist|Manager|Analyst|Developer|Architect|Lead|Specialist|Consultant|Coordinator|Director|VP|CTO|CEO|CFO|COO))',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, jd_text, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            # Clean up the title
            title = re.sub(r'\s+', ' ', title)  # Remove extra spaces
            return title
    
    # If no pattern matches, try to find common job titles in the text
    common_titles = [
        'Data Scientist', 'Software Engineer', 'Data Engineer', 'Machine Learning Engineer',
        'Product Manager', 'Business Analyst', 'Data Analyst', 'DevOps Engineer',
        'Frontend Developer', 'Backend Developer', 'Full Stack Developer', 'UI/UX Designer',
        'Project Manager', 'Scrum Master', 'Technical Lead', 'Architect'
    ]
    
    for title in common_titles:
        if title.lower() in jd_text.lower():
            return title
    
    return "Professional Role"  # Default fallback

def generate_pdf_report(
    resume_text,
    jd_text,
    present_skills,
    missing_skills,
    learning_path,
    ai_feedback,
    role_advice,
    radar_chart_path=None
):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "SkillShift – Skill Gap Analysis Report", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, f"Resume Summary:\n{resume_text[:800]}...", align="L")
    pdf.ln(2)
    pdf.multi_cell(0, 8, f"Job Description Summary:\n{jd_text[:800]}...", align="L")
    pdf.ln(2)
    if radar_chart_path:
        pdf.image(radar_chart_path, x=10, w=pdf.w-20)
        pdf.ln(2)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Skill Gap Analysis", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, f"Skills Present: {', '.join([s.title() for s in present_skills])}")
    pdf.multi_cell(0, 8, f"Missing Skills: {', '.join([s.title() for s in missing_skills])}")
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Dynamic Learning Path", ln=True)
    pdf.set_font("Arial", size=10)
    for step in learning_path:
        pdf.multi_cell(0, 8, step)
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "AI-Powered Resume Feedback", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, ai_feedback)
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Role-Specific Advice", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, role_advice)
    pdf.ln(2)
    pdf.output("SkillShift_Report.pdf")
    return "SkillShift_Report.pdf" 