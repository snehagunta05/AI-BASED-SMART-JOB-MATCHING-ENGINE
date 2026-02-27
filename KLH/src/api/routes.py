"""Flask API routes for job matching"""

import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from src.models.candidate import Candidate
from src.models.job import Job
from src.matching.matching_engine import MatchingEngine
from src.utils.data_loader import DataLoader


def create_app():
    """Create and configure Flask application"""

    app = Flask(__name__, template_folder='../../templates')
    CORS(app)

    # Initialize components
    data_loader = DataLoader()
    matching_engine = MatchingEngine()

    # Load sample data
    candidates = data_loader.load_candidates()
    jobs = data_loader.load_jobs()

    # ==============================
    # HOME ROUTE - Serve HTML UI
    # ==============================
    @app.route("/", methods=["GET"])
    def home():
        return render_template('index.html')

    # ==============================
    # HEALTH CHECK
    # ==============================
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "AI Job Matching Engine API is running",
            "version": "1.0.0"
        })

    # ==============================
    # GET ALL CANDIDATES
    # ==============================
    @app.route("/api/candidates", methods=["GET"])
    def get_candidates():
        return jsonify({
            "candidates": [c.to_dict() for c in candidates]
        })

    # ==============================
    # GET ALL JOBS
    # ==============================
    @app.route("/api/jobs", methods=["GET"])
    def get_jobs():
        return jsonify({
            "jobs": [j.to_dict() for j in jobs]
        })

    # ==============================
    # MATCH CANDIDATE TO JOBS
    # ==============================
    @app.route("/api/match", methods=["POST"])
    def match_candidate():

        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        candidate = Candidate.from_dict(data)
        min_threshold = data.get("min_threshold", 30.0)

        matches = matching_engine.match_candidate_to_jobs(
            candidate,
            jobs,
            min_threshold
        )

        results = []

        for match in matches:
            job = next((j for j in jobs if j.job_id == match.job_id), None)

            results.append({
                "candidate_id": match.candidate_id,
                "job_id": match.job_id,
                "job_title": job.title if job else "",
                "company": job.company if job else "",
                "match_score": round(match.match_score, 2),
                "skill_match": round(match.skill_match, 2),
                "experience_match": round(match.experience_match, 2),
                "location_match": round(match.location_match, 2),
                "salary_match": round(match.salary_match, 2),
                "matched_skills": match.matched_skills,
                "missing_skills": match.missing_skills,
                "match_level": match.get_match_level()
            })

        return jsonify({
            "candidate": candidate.to_dict(),
            "matches": results,
            "total_matches": len(results)
        })

    # ==============================
    # MATCH ALL CANDIDATES TO A JOB
    # ==============================
    @app.route("/api/match/candidates", methods=["POST"])
    def match_candidates_to_job():

        data = request.get_json()

        if not data or "job_id" not in data:
            return jsonify({"error": "Job ID required"}), 400

        job = next((j for j in jobs if j.job_id == data["job_id"]), None)

        if not job:
            return jsonify({"error": "Job not found"}), 404

        min_threshold = data.get("min_threshold", 30.0)

        matches = matching_engine.match_job_to_candidates(
            job,
            candidates,
            min_threshold
        )

        results = []

        for match in matches:
            candidate = next(
                (c for c in candidates if c.candidate_id == match.candidate_id),
                None
            )

            results.append({
                "candidate_id": match.candidate_id,
                "candidate_name": candidate.name if candidate else "",
                "candidate_email": candidate.email if candidate else "",
                "match_score": round(match.match_score, 2),
                "skill_match": round(match.skill_match, 2),
                "experience_match": round(match.experience_match, 2),
                "location_match": round(match.location_match, 2),
                "salary_match": round(match.salary_match, 2),
                "matched_skills": match.matched_skills,
                "missing_skills": match.missing_skills,
                "match_level": match.get_match_level()
            })

        return jsonify({
            "job": job.to_dict(),
            "matches": results,
            "total_matches": len(results)
        })

    # ==============================
    # GET ALL MATCHES (For Ranking Dashboard)
    # ==============================
    @app.route("/api/match/all", methods=["GET"])
    def get_all_matches():
        """Get all candidate-job matches for ranking dashboard"""
        min_threshold = request.args.get("min_threshold", 30.0, type=float)
        
        # Get top matches across all candidates and jobs
        all_matches = matching_engine.get_top_matches(candidates, jobs, top_n=200)
        
        # Filter by min_threshold
        filtered_matches = [m for m in all_matches if m['match_score'] >= min_threshold]
        
        results = []
        for match in filtered_matches[:100]:  # Limit to 100 results
            results.append({
                "candidate_id": match['candidate_id'],
                "candidate_name": match['candidate_name'],
                "job_id": match['job_id'],
                "job_title": match['job_title'],
                "company": match['company'],
                "match_score": round(match['match_score'], 2),
                "skill_match": round(match['skill_match'], 2),
                "experience_match": round(match['experience_match'], 2),
                "location_match": round(match['location_match'], 2),
                "salary_match": round(match['salary_match'], 2),
                "matched_skills": match['matched_skills'],
                "missing_skills": match['missing_skills']
            })
        
        return jsonify({
            "matches": results,
            "total_matches": len(results)
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000, host='0.0.0.0')
