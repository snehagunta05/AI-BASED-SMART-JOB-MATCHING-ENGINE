"""Skill matching algorithm using TF-IDF and cosine similarity"""

from typing import List, Tuple, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SkillMatcher:
    """Handles skill-based matching between candidates and jobs"""
    
    # Skill aliases for fuzzy matching
    SKILL_ALIASES = {
        'ML': 'MACHINE LEARNING',
        'DL': 'DEEP LEARNING',
        'JS': 'JAVASCRIPT',
        'TS': 'TYPESCRIPT',
        'AWS': 'AMAZON WEB SERVICES',
        'GCP': 'GOOGLE CLOUD PLATFORM',
        'AZURE': 'MICROSOFT AZURE',
        'REACT NATIVE': 'MOBILE DEVELOPMENT',
        'FLUTTER': 'MOBILE DEVELOPMENT',
        'XAMARIN': 'MOBILE DEVELOPMENT',
        'POSTGRES': 'POSTGRESQL',
        'MYSQL': 'MYSQL',
        'REDIS': 'REDIS',
        'MONGO': 'MONGODB',
        'REST': 'REST API',
        'GRAPHQL': 'GRAPHQL',
        'CI/CD': 'CI CD',
        'DATA SCIENCE': 'DATA SCIENCE',
        'DATA ANALYTICS': 'DATA ANALYSIS',
        'AI': 'ARTIFICIAL INTELLIGENCE',
    }
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            token_pattern=r'(?u)\b\w+\b',
            ngram_range=(1, 2)
        )
    
    def normalize_skill(self, skill: str) -> str:
        """Normalize skill name using aliases"""
        skill_upper = skill.strip().upper()
        return self.SKILL_ALIASES.get(skill_upper, skill_upper)
    
    def calculate_skill_match(
        self, 
        candidate_skills: List[str], 
        job_skills: List[str]
    ) -> Tuple[float, List[str], List[str]]:
        """
        Calculate skill match percentage between candidate and job requirements.
        
        Args:
            candidate_skills: List of skills the candidate has
            job_skills: List of skills required by the job
            
        Returns:
            Tuple of (match_percentage, matched_skills, missing_skills)
        """
        # Normalize skills
        normalized_candidate = [self.normalize_skill(s) for s in candidate_skills]
        normalized_job = [self.normalize_skill(s) for s in job_skills]
        
        # Find exact matches
        matched = set(normalized_candidate) & set(normalized_job)
        missing = set(normalized_job) - set(normalized_candidate)
        
        # Calculate exact match percentage
        if len(normalized_job) == 0:
            return 100.0, list(matched), list(missing)
        
        exact_match_pct = (len(matched) / len(normalized_job)) * 100
        
        # Use TF-IDF for partial matching
        if len(normalized_candidate) > 0 and len(normalized_job) > 0:
            # Create corpus for TF-IDF
            corpus = normalized_candidate + normalized_job
            try:
                tfidf_matrix = self.vectorizer.fit_transform(corpus)
                
                # Get vectors for candidate and job skills
                candidate_vector = tfidf_matrix[:len(normalized_candidate)]
                job_vector = tfidf_matrix[len(normalized_candidate):]
                
                # Calculate cosine similarity
                similarities = cosine_similarity(candidate_vector, job_vector)
                
                # Get best match for each job skill
                best_matches = similarities.max(axis=0)
                partial_match_pct = np.mean(best_matches) * 100
                
                # Combine exact and partial matching (weighted)
                final_match = (exact_match_pct * 0.7) + (partial_match_pct * 0.3)
            except:
                final_match = exact_match_pct
        else:
            final_match = exact_match_pct
        
        return min(100.0, final_match), list(matched), list(missing)
    
    def get_skill_gap_analysis(
        self, 
        candidate_skills: List[str], 
        job_skills: List[str]
    ) -> Dict:
        """
        Get detailed skill gap analysis.
        
        Args:
            candidate_skills: List of skills the candidate has
            job_skills: List of skills required by the job
            
        Returns:
            Dictionary with detailed analysis
        """
        normalized_candidate = [self.normalize_skill(s) for s in candidate_skills]
        normalized_job = [self.normalize_skill(s) for s in job_skills]
        
        matched = set(normalized_candidate) & set(normalized_job)
        missing = set(normalized_job) - set(normalized_candidate)
        extra = set(normalized_candidate) - set(normalized_job)
        
        return {
            'matched_skills': list(matched),
            'missing_skills': list(missing),
            'extra_skills': list(extra),
            'match_percentage': (len(matched) / len(normalized_job) * 100) if normalized_job else 100,
            'total_required': len(normalized_job),
            'total_matched': len(matched)
        }
