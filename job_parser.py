import pdfplumber
import docx
from utils import extract_skills_from_text

def parse_job_description(file_path):
    """Extract text and skills from a PDF, DOCX, or TXT job description."""
    if file_path.lower().endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() or '' for page in pdf.pages)
    elif file_path.lower().endswith('.docx'):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file_path.lower().endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file type for job description.")
    skills = extract_skills_from_text(text)
    return text, skills 