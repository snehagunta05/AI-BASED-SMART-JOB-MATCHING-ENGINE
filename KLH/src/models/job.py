"""Job model for job matching"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Job:
    """Represents a job posting"""
    
    job_id: str
    title: str
    company: str
    required_skills: List[str] = field(default_factory=list)
    min_experience: int = 0
    education_required: str = "Bachelor's"
    location: str = ""
    salary_min: int = 0
    salary_max: int = 0
    description: str = ""
    is_remote: bool = False
    
    def __post_init__(self):
        """Normalize skills to uppercase for consistent matching"""
        self.required_skills = [skill.strip().upper() for skill in self.required_skills]
        self.location = self.location.strip()
        self.education_required = self.education_required.strip()
        self.title = self.title.strip()
        self.company = self.company.strip()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'job_id': self.job_id,
            'title': self.title,
            'company': self.company,
            'required_skills': self.required_skills,
            'min_experience': self.min_experience,
            'education_required': self.education_required,
            'location': self.location,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'description': self.description,
            'is_remote': self.is_remote
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Job':
        """Create Job from dictionary"""
        return cls(
            job_id=data.get('job_id', ''),
            title=data.get('title', ''),
            company=data.get('company', ''),
            required_skills=data.get('required_skills', []),
            min_experience=data.get('min_experience', 0),
            education_required=data.get('education_required', "Bachelor's"),
            location=data.get('location', ''),
            salary_min=data.get('salary_min', 0),
            salary_max=data.get('salary_max', 0),
            description=data.get('description', ''),
            is_remote=data.get('is_remote', False)
        )
    
    def __str__(self) -> str:
        return f"Job({self.job_id}): {self.title} at {self.company}"
    
    def __repr__(self) -> str:
        return self.__str__()
