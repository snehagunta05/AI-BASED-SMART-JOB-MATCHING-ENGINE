
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Candidate:
    """Represents a job seeker candidate"""
    
    candidate_id: str
    name: str
    email: str
    skills: List[str] = field(default_factory=list)
    years_experience: int = 0
    education: str = "Bachelor's"
    preferred_location: str = ""
    expected_salary: int = 0
    resume_text: str = ""
    
    def __post_init__(self):
        """Normalize skills to uppercase for consistent matching"""
        self.skills = [skill.strip().upper() for skill in self.skills]
        self.preferred_location = self.preferred_location.strip()
        self.education = self.education.strip()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'candidate_id': self.candidate_id,
            'name': self.name,
            'email': self.email,
            'skills': self.skills,
            'years_experience': self.years_experience,
            'education': self.education,
            'preferred_location': self.preferred_location,
            'expected_salary': self.expected_salary,
            'resume_text': self.resume_text
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Candidate':
        """Create Candidate from dictionary"""
        return cls(
            candidate_id=data.get('candidate_id', ''),
            name=data.get('name', ''),
            email=data.get('email', ''),
            skills=data.get('skills', []),
            years_experience=data.get('years_experience', 0),
            education=data.get('education', "Bachelor's"),
            preferred_location=data.get('preferred_location', ''),
            expected_salary=data.get('expected_salary', 0),
            resume_text=data.get('resume_text', '')
        )
    
    def __str__(self) -> str:
        return f"Candidate({self.candidate_id}): {self.name}, {self.years_experience}yrs exp, {len(self.skills)} skills"
    
    def __repr__(self) -> str:
        return self.__str__()
