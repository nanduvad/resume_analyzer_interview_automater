# ===== FILE: ./routes/jobs.py =====

from flask import Blueprint, request, jsonify
from backend.utils.parser import parse_job_description
from backend.pinecone_client import store_job_embedding, find_similar_candidates
import uuid

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/analyze", methods=["POST"])
def analyze_job():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        job_text = data.get("job_text", "")
        if not job_text:
            return jsonify({"error": "Job description is required"}), 400

        # Parse job description
        parsed = parse_job_description(job_text)
        
        # Generate unique ID for this job
        job_id = f"job_{uuid.uuid4().hex}"
        
        # Store job embedding
        storage_success = store_job_embedding(
            job_id=job_id,
            job_text=job_text,
            metadata={
                "title": parsed.get("title", ""),
                "skills": parsed.get("skills", []),
                "summary": parsed.get("summary", "")
            }
        )
        
        # Find matching candidates
        similar_candidates = find_similar_candidates(job_text, top_k=10)
        
        # Format response
        matches = []
        if hasattr(similar_candidates, 'matches'):
            for match in similar_candidates.matches:
                # Handle both Pinecone and simple store formats
                if hasattr(match, 'id'):
                    # Pinecone format
                    matches.append({
                        "candidate_id": match.id,
                        "score": round(match.score * 100, 2),
                        "metadata": getattr(match, 'metadata', {})
                    })
                else:
                    # Simple store format (dict)
                    matches.append({
                        "candidate_id": match.get('id', 'unknown'),
                        "score": round(match.get('score', 0) * 100, 2),
                        "metadata": match.get('metadata', {})
                    })
        
        response = {
            **parsed,
            "job_id": job_id,
            "storage_status": "success" if storage_success else "partial",
            "matching_candidates": matches,
            "candidate_count": len(matches)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@jobs_bp.route("/", methods=["GET"])
def jobs_index():
    return jsonify({
        "message": "Jobs endpoint is active.",
        "endpoints": {
            "POST /jobs/analyze": "Analyze job description and find candidates",
            "GET /jobs/": "This info page"
        }
    })