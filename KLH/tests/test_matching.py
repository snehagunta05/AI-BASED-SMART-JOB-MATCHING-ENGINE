"""Tests for the matching engine"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.models.candidate import Candidate
from src.models.job import Job
from src.matching.matching_engine import MatchingEngine
from src.matching.skill_matcher import SkillMatcher
from src.matching.experience_matcher import ExperienceMatcher
from src.matching.location_matcher import LocationMatcher
from src.matching.salary_matcher import SalaryMatcher


class TestSkillMatcher:
    """Tests for skill matching"""
    
    def setup_method(self):
        self.matcher = SkillMatcher()
    
    def test_exact_skill_match(self):
        """Test exact skill matching"""
        candidate_skills = ["Python", "Machine Learning", "SQL"]
        job_skills = ["Python", "Machine Learning", "SQL", "TensorFlow"]
        
        match_score, matched, missing = self.matcher.calculate_skill_match(
            candidate_skills, job_skills
        )
        
        assert match_score > 0
        assert len(matched) == 3
        assert "TENSORFLOW" in missing
    
    def test_partial_skill_match(self):
        """Test partial skill matching"""
        candidate_skills = ["Python", "ML"]
        job_skills = ["Python", "Machine Learning", "TensorFlow"]
        
        match_score, matched, missing = self.matcher.calculate_skill_match(
            candidate_skills, job_skills
        )
        
        assert match_score > 0
    
    def test_no_skill_match(self):
        """Test no skill matching"""
        candidate_skills = ["Java", "Spring"]
        job_skills = ["Python", "Machine Learning"]
        
        match_score, matched, missing = self.matcher.calculate_skill_match(
            candidate_skills, job_skills
        )
        
        assert match_score < 50


class TestExperienceMatcher:
    """Tests for experience matching"""
    
    def setup_method(self):
        self.matcher = ExperienceMatcher()
    
    def test_exact_experience_match(self):
        """Test exact experience matching"""
        match = self.matcher.calculate_experience_match(5, 5)
        assert match >= 100
    
    def test_exceeding_experience(self):
        """Test exceeding experience"""
        match = self.matcher.calculate_experience_match(8, 5)
        assert match >= 100
    
    def test_insufficient_experience(self):
        """Test insufficient experience"""
        match = self.matcher.calculate_experience_match(2, 5)
        assert match < 100
        assert match >= 30
    
    def test_education_match(self):
        """Test education matching"""
        # Candidate has higher education
        match = self.matcher.calculate_education_match("Master's", "Bachelor's")
        assert match == 100
        
        # Candidate has lower education
        match = self.matcher.calculate_education_match("Bachelor's", "Master's")
        assert match < 100


class TestLocationMatcher:
    """Tests for location matching"""
    
    def setup_method(self):
        self.matcher = LocationMatcher()
    
    def test_exact_location_match(self):
        """Test exact location matching"""
        match = self.matcher.calculate_location_match(
            "San Francisco, CA", 
            "San Francisco, CA",
            False
        )
        assert match == 100
    
    def test_same_state_match(self):
        """Test same state matching"""
        match = self.matcher.calculate_location_match(
            "Los Angeles, CA",
            "San Francisco, CA",
            False
        )
        assert 50 < match < 100
    
    def test_remote_job_match(self):
        """Test remote job matching"""
        match = self.matcher.calculate_location_match(
            "New York, NY",
            "Remote",
            True
        )
        assert match >= 80
    
    def test_remote_candidate(self):
        """Test candidate who wants remote"""
        match = self.matcher.calculate_location_match(
            "Remote",
            "San Francisco, CA",
            False
        )
        assert match == 60


class TestSalaryMatcher:
    """Tests for salary matching"""
    
    def setup_method(self):
        self.matcher = SalaryMatcher()
    
    def test_salary_in_range(self):
        """Test salary within range"""
        match = self.matcher.calculate_salary_match(100000, 80000, 120000)
        assert match == 100
    
    def test_salary_below_range(self):
        """Test salary below range"""
        match = self.matcher.calculate_salary_match(50000, 80000, 120000)
        assert match < 100
        assert match >= 30
    
    def test_salary_above_range(self):
        """Test salary above range"""
        match = self.matcher.calculate_salary_match(150000, 80000, 120000)
        assert match < 100
        assert match >= 30
    
    def test_no_salary_info(self):
        """Test when no salary info provided"""
        match = self.matcher.calculate_salary_match(100000, 0, 0)
        assert match == 100


class TestMatchingEngine:
    """Tests for the main matching engine"""
    
    def setup_method(self):
        self.engine = MatchingEngine()
        
        # Create sample candidates
        self.candidates = [
            Candidate(
                candidate_id="C001",
                name="Alice",
                email="alice@test.com",
                skills=["Python", "Machine Learning", "SQL"],
                years_experience=5,
                education="Master's",
                preferred_location="San Francisco, CA",
                expected_salary=120000,
                resume_text=""
            ),
            Candidate(
                candidate_id="C002",
                name="Bob",
                email="bob@test.com",
                skills=["Java", "Spring Boot"],
                years_experience=3,
                education="Bachelor's",
                preferred_location="New York, NY",
                expected_salary=80000,
                resume_text=""
            )
        ]
        
        # Create sample jobs
        self.jobs = [
            Job(
                job_id="J001",
                title="ML Engineer",
                company="TechCorp",
                required_skills=["Python", "Machine Learning", "TensorFlow"],
                min_experience=4,
                education_required="Master's",
                location="San Francisco, CA",
                salary_min=130000,
                salary_max=180000,
                description="",
                is_remote=False
            ),
            Job(
                job_id="J002",
                title="Java Developer",
                company="Enterprise Inc",
                required_skills=["Java", "Spring Boot"],
                min_experience=2,
                education_required="Bachelor's",
                location="New York, NY",
                salary_min=70000,
                salary_max=100000,
                description="",
                is_remote=False
            )
        ]
    
    def test_candidate_to_job_match(self):
        """Test matching a candidate to a job"""
        match = self.engine.match_candidate_to_job(self.candidates[0], self.jobs[0])
        
        assert match.candidate_id == "C001"
        assert match.job_id == "J001"
        assert match.match_score > 0
        assert 0 <= match.match_score <= 100
    
    def test_candidate_to_multiple_jobs(self):
        """Test matching a candidate to multiple jobs"""
        matches = self.engine.match_candidate_to_jobs(self.candidates[0], self.jobs)
        
        assert len(matches) > 0
        assert all(m.candidate_id == "C001" for m in matches)
        # Should be sorted by score
        assert matches[0].match_score >= matches[-1].match_score
    
    def test_job_to_candidates(self):
        """Test matching a job to multiple candidates"""
        matches = self.engine.match_job_to_candidates(self.jobs[0], self.candidates)
        
        assert len(matches) > 0
        assert all(m.job_id == "J001" for m in matches)
    
    def test_match_threshold(self):
        """Test minimum match threshold"""
        # Create a very poor match
        poor_candidate = Candidate(
            candidate_id="C003",
            name="Charlie",
            email="charlie@test.com",
            skills=["Word"],
            years_experience=0,
            education="High School",
            preferred_location="Remote",
            expected_salary=30000,
            resume_text=""
        )
        
        matches = self.engine.match_candidate_to_jobs(poor_candidate, self.jobs, min_threshold=30)
        
        # All matches should be above threshold
        for match in matches:
            assert match.match_score >= 30


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
