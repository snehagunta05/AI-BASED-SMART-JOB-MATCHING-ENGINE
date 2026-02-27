"""Main matching engine that combines all matching algorithms"""

from typing import List, Dict, Tuple
from ..models.candidate import Candidate
from ..models.job import Job
from ..models.match_result import MatchResult
from .skill_matcher import SkillMatcher
from .experience_matcher import ExperienceMatcher
from .location_matcher import LocationMatcher
from .salary_matcher import SalaryMatcher


class MatchingEngine:
    """
    Main matching engine that combines skill, experience, location, 
    and salary matching algorithms.
    """
    
    # Weights for different matching criteria
    DEFAULT_WEIGHTS = {
        'skills': 0.40,      # 40% - Most important
        'experience': 0.25,  # 25% - Requirement fulfillment
        'salary': 0.20,      # 20% - Mutual compatibility
        'location': 0.15      # 15% - Preference matching
    }
    
    # Minimum threshold for considering a match
    MIN_MATCH_THRESHOLD = 30.0
    
    def __init__(self, weights: Dict = None):
        """
        Initialize the matching engine.
        
        Args:
            weights: Optional custom weights for matching criteria
        """
        self.weights = weights or self.DEFAULT_WEIGHTS
        
        # Initialize individual matchers
        self.skill_matcher = SkillMatcher()
        self.experience_matcher = ExperienceMatcher()
        self.location_matcher = LocationMatcher()
        self.salary_matcher = SalaryMatcher()
    
    def match_candidate_to_job(
        self, 
        candidate: Candidate, 
        job: Job
    ) -> MatchResult:
        """
        Match a single candidate to a single job.
        
        Args:
            candidate: The candidate to match
            job: The job to match against
            
        Returns:
            MatchResult with all matching details
        """
        # Calculate individual match scores
        skill_match, matched_skills, missing_skills = self.skill_matcher.calculate_skill_match(
            candidate.skills, 
            job.required_skills
        )
        
        experience_match = self.experience_matcher.calculate_combined_experience_match(
            candidate.years_experience,
            job.min_experience,
            candidate.education,
            job.education_required
        )
        
        location_match = self.location_matcher.calculate_location_match(
            candidate.preferred_location,
            job.location,
            job.is_remote
        )
        
        salary_match = self.salary_matcher.calculate_salary_match(
            candidate.expected_salary,
            job.salary_min,
            job.salary_max
        )
        
        # Calculate weighted overall match score
        overall_match = (
            (skill_match * self.weights['skills']) +
            (experience_match * self.weights['experience']) +
            (salary_match * self.weights['salary']) +
            (location_match * self.weights['location'])
        )
        
        # Create match result
        result = MatchResult(
            candidate_id=candidate.candidate_id,
            job_id=job.job_id,
            match_score=overall_match,
            skill_match=skill_match,
            experience_match=experience_match,
            location_match=location_match,
            salary_match=salary_match,
            matched_skills=matched_skills,
            missing_skills=missing_skills
        )
        
        return result
    
    def match_candidate_to_jobs(
        self, 
        candidate: Candidate, 
        jobs: List[Job],
        min_threshold: float = None
    ) -> List[MatchResult]:
        """
        Match a candidate to multiple jobs.
        
        Args:
            candidate: The candidate to match
            jobs: List of jobs to match against
            min_threshold: Minimum match score to include (default: MIN_MATCH_THRESHOLD)
            
        Returns:
            List of MatchResults, sorted by match score (descending)
        """
        threshold = min_threshold or self.MIN_MATCH_THRESHOLD
        
        results = []
        for job in jobs:
            result = self.match_candidate_to_job(candidate, job)
            if result.match_score >= threshold:
                results.append(result)
        
        # Sort by match score (highest first)
        results.sort(key=lambda x: x.match_score, reverse=True)
        
        return results
    
    def match_job_to_candidates(
        self, 
        job: Job, 
        candidates: List[Candidate],
        min_threshold: float = None
    ) -> List[MatchResult]:
        """
        Match a job to multiple candidates.
        
        Args:
            job: The job to match
            candidates: List of candidates to match against
            min_threshold: Minimum match score to include
            
        Returns:
            List of MatchResults, sorted by match score (descending)
        """
        threshold = min_threshold or self.MIN_MATCH_THRESHOLD
        
        results = []
        for candidate in candidates:
            result = self.match_candidate_to_job(candidate, job)
            if result.match_score >= threshold:
                results.append(result)
        
        # Sort by match score (highest first)
        results.sort(key=lambda x: x.match_score, reverse=True)
        
        return results
    
    def match_all(
        self, 
        candidates: List[Candidate], 
        jobs: List[Job],
        min_threshold: float = None
    ) -> Dict[str, List[MatchResult]]:
        """
        Match all candidates to all jobs.
        
        Args:
            candidates: List of candidates
            jobs: List of jobs
            min_threshold: Minimum match score to include
            
        Returns:
            Dictionary mapping candidate_id to their matched jobs
        """
        threshold = min_threshold or self.MIN_MATCH_THRESHOLD
        
        matches = {}
        for candidate in candidates:
            matches[candidate.candidate_id] = self.match_candidate_to_jobs(
                candidate, 
                jobs, 
                threshold
            )
        
        return matches
    
    def get_top_matches(
        self, 
        candidates: List[Candidate], 
        jobs: List[Job],
        top_n: int = 10
    ) -> List[Dict]:
        """
        Get top N matches across all candidate-job pairs.
        
        Args:
            candidates: List of candidates
            jobs: List of jobs
            top_n: Number of top matches to return
            
        Returns:
            List of dictionaries with match details
        """
        all_matches = []
        
        for candidate in candidates:
            for job in jobs:
                result = self.match_candidate_to_job(candidate, job)
                all_matches.append({
                    'candidate_id': candidate.candidate_id,
                    'candidate_name': candidate.name,
                    'job_id': job.job_id,
                    'job_title': job.title,
                    'company': job.company,
                    'match_score': result.match_score,
                    'skill_match': result.skill_match,
                    'experience_match': result.experience_match,
                    'location_match': result.location_match,
                    'salary_match': result.salary_match,
                    'matched_skills': result.matched_skills,
                    'missing_skills': result.missing_skills
                })
        
        # Sort by match score and get top N
        all_matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return all_matches[:top_n]
    
    def get_match_statistics(self, matches: List[MatchResult]) -> Dict:
        """
        Get statistics about a set of matches.
        
        Args:
            matches: List of MatchResults
            
        Returns:
            Dictionary with statistics
        """
        if not matches:
            return {
                'count': 0,
                'avg_score': 0,
                'min_score': 0,
                'max_score': 0,
                'excellent_matches': 0,
                'good_matches': 0,
                'fair_matches': 0,
                'low_matches': 0
            }
        
        scores = [m.match_score for m in matches]
        
        return {
            'count': len(matches),
            'avg_score': sum(scores) / len(scores),
            'min_score': min(scores),
            'max_score': max(scores),
            'excellent_matches': len([s for s in scores if s >= 70]),
            'good_matches': len([s for s in scores if 50 <= s < 70]),
            'fair_matches': len([s for s in scores if 30 <= s < 50]),
            'low_matches': len([s for s in scores if s < 30])
        }
