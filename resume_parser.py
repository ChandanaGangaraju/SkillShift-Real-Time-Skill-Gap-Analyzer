import pdfplumber
import docx
from utils import extract_skills_from_text
import re

def extract_skills_section(text):
    """
    Extract all skills from the 'Skills' section, handling category headers (e.g., 'Languages:') and comma-separated lists.
    Returns a flat list of all found skills and the raw section text.
    """
    lines = text.splitlines()
    skills_lines = []
    in_skills = False
    for line in lines:
        if not in_skills and re.match(r'^\s*skills\s*[:\-]?', line, re.IGNORECASE):
            in_skills = True
            continue
        if in_skills:
            # Stop at next section header (all caps, or common section names), or empty line
            if re.match(r'^\s*[A-Z][A-Z\s]{2,}$', line) or re.match(r'^\s*(experience|education|projects|summary|certifications|work|profile|professional|languages|interests|contact)\b', line, re.IGNORECASE) or not line.strip():
                break
            skills_lines.append(line.strip())
    # Extract all comma-separated skills from each line after a colon
    all_skills = []
    for line in skills_lines:
        if ':' in line:
            _, skills_part = line.split(':', 1)
        else:
            skills_part = line
        raw_skills = re.split(r'[\u2022\u2023\u25E6\u2043\u2219\-•;\,\n]', skills_part)
        all_skills.extend([s.strip() for s in raw_skills if s.strip()])
    raw_section = '\n'.join(skills_lines)
    return all_skills if all_skills else None, raw_section if skills_lines else None

def parse_resume(file_path):
    """Extract text and skills from a PDF or DOCX resume, focusing on the 'Skills' section if present. Returns (text, skills, raw_skills_section)."""
    if file_path.lower().endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() or '' for page in pdf.pages)
    elif file_path.lower().endswith('.docx'):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type for resume.")
    skills_section, raw_section = extract_skills_section(text)
    if skills_section:
        skills = extract_skills_from_text(' '.join(skills_section))
    else:
        skills = extract_skills_from_text(text)
    return text, skills, raw_section 