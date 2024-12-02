def calculate_score(resume_data, job_role_data):
    skill_match = len(set(resume_data['skills']) & set(job_role_data['skills'])) / len(job_role_data['skills'])
    education_match = 1 if resume_data.get('education') in job_role_data.get('education', []) else 0
    experience_match = 1 if resume_data.get('experience', 0) >= job_role_data.get('experience', 0) else 0

    total_score = (skill_match * 50) + (education_match * 30) + (experience_match * 20)
    return total_score
