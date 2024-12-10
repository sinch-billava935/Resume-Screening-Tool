from fuzzywuzzy import fuzz

def calculate_score(resume_data, job_role_data):
    # Calculate skill match score
    max_skill_score = 50  # Maximum points for skills
    total_skills_required = len(job_role_data.get('skills', []))
    skill_match = len(set(resume_data.get('skills', [])) & set(job_role_data.get('skills', [])))
    skill_score = (skill_match / total_skills_required) * max_skill_score if total_skills_required > 0 else 0

    # Calculate education match score using fuzzy matching
    max_education_score = 20  # Maximum points for education
    required_education = job_role_data.get('education', '').strip().lower()
    resume_education = resume_data.get('education', '').strip().lower()
    if required_education and resume_education:
        match_score = fuzz.partial_ratio(resume_education, required_education)
        education_match = 1 if match_score >= 65 else 0  # 80% similarity threshold
    else:
        education_match = 0
    education_score = education_match * max_education_score

    # Calculate experience match score
    max_experience_score = 30  # Maximum points for experience
    required_experience = job_role_data.get('experience', 0)
    resume_experience = resume_data.get('experience', 0)
    experience_match = min(resume_experience, required_experience)
    experience_score = (experience_match / required_experience) * max_experience_score if required_experience > 0 else 0

    # Calculate total score
    total_score = skill_score + education_score + experience_score
    max_total_score = max_skill_score + max_education_score + max_experience_score
    overall_score = (total_score / max_total_score) * 100  # Normalize to 100

    # Determine verdict based on score
    verdict = "Selected" if overall_score >= 60 else "Not Selected"

    # Return detailed scoring breakdown
    return {
        "overall_score": overall_score,
        "verdict": verdict,
        "skill_score": skill_score,
        "education_score": education_score,
        "experience_score": experience_score
    }
