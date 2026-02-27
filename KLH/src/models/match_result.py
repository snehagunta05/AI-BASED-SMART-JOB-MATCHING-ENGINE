"""MatchResult model for storing matching results"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class MatchResult:
    """Represents the matching result between a candidate and a job"""
    
    candidate_id: str
    job_id: str
    match_score: float = 0.0
    skill_match: float = 0.0
    experience_match: float = 0.0
    location_match: float = 0.0
    salary_match: float = 0.0
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Ensure scores are within valid range"""
        self.match_score = max(0.0, min(100.0, self.match_score))
        self.skill_match = max(0.0, min(100.0, self.skill_match))
        self.experience_match = max(0.0, min(100.0, self.experience_match))
        self.location_match = max(0.0, min(100.0, self.location_match))
        self.salary_match = max(0.0, min(100.0, self.salary_match))
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'match_score': round(self.match_score, 2),
            'skill_match': round(self.skill_match, 2),
            'experience_match': round(self.experience_match, 2),
            'location_match': round(self.location_match, 2),
            'salary_match': round(self.salary_match, 2),
            'matched_skills': self.matched_skills,
            'missing_skills': self.missing_skills
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MatchResult':
        """Create MatchResult from dictionary"""
        return cls(
            candidate_id=data.get('candidate_id', ''),
            job_id=data.get('job_id', ''),
            match_score=data.get('match_score', 0.0),
            skill_match=data.get('skill_match', 0.0),
            experience_match=data.get('experience_match', 0.0),
            location_match=data.get('location_match', 0.0),
            salary_match=data.get('salary_match', 0.0),
            matched_skills=data.get('matched_skills', []),
            missing_skills=data.get('missing_skills', [])
        )
    
    def get_match_level(self) -> str:
        """Get the match level category"""
        if self.match_score >= 70:
            return "Excellent Match"
        elif self.match_score >= 50:
            return "Good Match"
        elif self.match_score >= 30:
            return "Fair Match"
        else:
            return "Low Match"
    
    def __str__(self) -> str:
        return f"Match({self.candidate_id}-{self.job_id}): {self.match_score:.1f}%"
    
    def __repr__(self) -> str:
        return self.__str__()
