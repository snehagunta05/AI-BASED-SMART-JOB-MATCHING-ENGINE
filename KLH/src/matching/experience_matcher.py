"""Experience matching algorithm"""

from typing import Tuple


class ExperienceMatcher:
    """Handles experience-based matching between candidates and jobs"""
    
    # Education level hierarchy
    EDUCATION_LEVELS = {
        'high school': 1,
        'associate': 2,
        'bachelor\'s': 3,
        'bachelors': 3,
        'master\'s': 4,
        'masters': 4,
        'phd': 5,
        'doctorate': 5
    }
    
    def __init__(self):
        pass
    
    def calculate_experience_match(
        self, 
        candidate_experience: int, 
        min_experience_required: int
    ) -> float:
        """
        Calculate experience match percentage.
        
        Args:
            candidate_experience: Years of experience the candidate has
            min_experience_required: Minimum years required for the job
            
        Returns:
            Match percentage (0-100)
        """
        if min_experience_required == 0:
            return 100.0
        
        if candidate_experience >= min_experience_required:
            # Perfect or exceeding match
            excess = candidate_experience - min_experience_required
            # Cap the bonus at 2 years
            bonus = min(excess, 2) * 2.5  # Up to 5% bonus
            return min(100.0, 100.0 + bonus)
        else:
            # Partial match based on how close they are
            deficit = min_experience_required - candidate_experience
            # Lose 15% per year of deficit, but not below 30%
            match = 100.0 - (deficit * 15.0)
            return max(30.0, match)
    
    def calculate_education_match(
        self, 
        candidate_education: str, 
        education_required: str
    ) -> float:
        """
        Calculate education match percentage.
        
        Args:
            candidate_education: Candidate's highest education level
            education_required: Minimum education required for the job
            
        Returns:
            Match percentage (0-100)
        """
        # Normalize education levels
        candidate_level = self._get_education_level(candidate_education)
        required_level = self._get_education_level(education_required)
        
        if candidate_level >= required_level:
            return 100.0
        else:
            # Calculate partial match
            deficit = required_level - candidate_level
            match = 100.0 - (deficit * 25.0)  # 25% per level deficit
            return max(50.0, match)
    
    def _get_education_level(self, education: str) -> int:
        """Get numeric education level"""
        if not education:
            return 3  # Default to Bachelor's
        
        edu_lower = education.lower().strip()
        return self.EDUCATION_LEVELS.get(edu_lower, 3)
    
    def calculate_combined_experience_match(
        self,
        candidate_experience: int,
        min_experience_required: int,
        candidate_education: str,
        education_required: str
    ) -> float:
        """
        Calculate combined experience and education match.
        
        Args:
            candidate_experience: Years of experience
            min_experience_required: Minimum experience required
            candidate_education: Candidate's education level
            education_required: Required education level
            
        Returns:
            Combined match percentage
        """
        exp_match = self.calculate_experience_match(
            candidate_experience, 
            min_experience_required
        )
        edu_match = self.calculate_education_match(
            candidate_education, 
            education_required
        )
        
        # Weight: 70% experience, 30% education
        combined = (exp_match * 0.7) + (edu_match * 0.3)
        
        return combined
