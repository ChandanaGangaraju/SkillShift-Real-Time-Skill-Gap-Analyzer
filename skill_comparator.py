import difflib

def compare_skills(resume_skills, job_skills):
    """
    Compare resume and job description skills.
    Returns a dict with 'present', 'missing', and 'partial' (empty for now).
    """
    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])
    present = sorted(list(resume_set & job_set))
    missing = sorted(list(job_set - resume_set))
    partial = []  # Placeholder for future fuzzy/semantic matching
    return {
        'present': present,
        'missing': missing,
        'partial': partial
    }

def get_partial_matches(resume_skills, job_skills, max_distance=2):
    """
    Return pairs of (resume_skill, job_skill) that are similar but not exact matches (Levenshtein distance <= max_distance).
    """
    from difflib import SequenceMatcher
    matches = []
    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])
    for r in resume_set:
        for j in job_set:
            if r == j:
                continue
            # Use SequenceMatcher ratio as a proxy for similarity
            ratio = SequenceMatcher(None, r, j).ratio()
            # Consider as partial match if ratio is high but not 1.0
            if 0.75 < ratio < 1.0:
                matches.append((r, j))
    return matches 