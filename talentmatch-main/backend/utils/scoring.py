# ===== FILE: ./backend/utils/scoring.py =====

import random
# Remove the problematic import and use a fallback

def score_candidate(candidate_data: dict):
    """Score candidate based on job matching - simplified version"""
    candidate_name = candidate_data.get("name", "Unknown")
    resume_text = candidate_data.get("resume", "")
    
    # Simple scoring based on resume length and keywords
    base_score = random.randint(50, 85)  # Base random score
    
    # Add bonus for resume content
    if resume_text:
        # Simple keyword matching for bonus points
        keywords = ["python", "flask", "react", "django", "javascript", "backend", "developer"]
        keyword_bonus = sum(10 for keyword in keywords if keyword in resume_text.lower())
        base_score = min(100, base_score + keyword_bonus)
    
    return {
        "name": candidate_name,
        "score": base_score,
        "experience": candidate_data.get("experience", "Not specified"),
        "skills": candidate_data.get("skills", [])
    }

def score_candidate_advanced(candidate_data: dict, job_text: str = ""):
    """Advanced scoring if we have job context"""
    base_score = score_candidate(candidate_data)
    
    if job_text:
        # Simple keyword matching between candidate and job
        candidate_text = candidate_data.get("resume", "").lower()
        job_text_lower = job_text.lower()
        
        matching_keywords = []
        keywords = ["python", "flask", "react", "django", "javascript", "backend", "developer", "web", "api"]
        
        for keyword in keywords:
            if keyword in candidate_text and keyword in job_text_lower:
                matching_keywords.append(keyword)
        
        # Add bonus for matching keywords
        match_bonus = len(matching_keywords) * 5
        base_score["score"] = min(100, base_score["score"] + match_bonus)
        base_score["matching_keywords"] = matching_keywords
    
    return base_score