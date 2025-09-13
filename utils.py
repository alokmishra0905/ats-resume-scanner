import re
from PyPDF2 import PdfReader
import docx

KNOWN_SKILLS = {
    "python", "flask", "sql", "javascript", "html", "css", "git", "machine learning", "django"
}

def extract_text_from_pdf(path):
    text = ""
    reader = PdfReader(path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return '\n'.join([p.text for p in doc.paragraphs])

def extract_resume_data(path):
    if path.endswith('.pdf'):
        text = extract_text_from_pdf(path)
    elif path.endswith('.docx'):
        text = extract_text_from_docx(path)
    else:
        return {"name": "", "email": "", "skills": "", "raw_text": ""}

    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    email = email_match.group() if email_match else "Not Found"

    skills_found = set()
    for skill in KNOWN_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            skills_found.add(skill.capitalize())

    return {
        "name": "Unknown",
        "email": email,
        "skills": ", ".join(sorted(skills_found)),
        "raw_text": text
    }

def extract_keywords(text):
    """
    Extract known skills from the given text using case-insensitive matching.
    """
    found = set()
    text_lower = text.lower()
    for skill in KNOWN_SKILLS:
        if skill.lower() in text_lower:
            found.add(skill.lower())
    return found


def calculate_ats_score(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    if not job_keywords:
        return 0  # Avoid division by zero

    matches = resume_keywords & job_keywords
    score = int((len(matches) / len(job_keywords)) * 100)
    return score
