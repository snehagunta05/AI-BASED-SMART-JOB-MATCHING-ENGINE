"""Salary compatibility matching algorithm"""

from typing import Tuple, Dict


class SalaryMatcher:
    """Handles salary-based matching between candidates and jobs"""
    
    def __init__(self):
        pass
    
    def calculate_salary_match(
        self,
        expected_salary: int,
        salary_min: int,
        salary_max: int
    ) -> float:
        """
        Calculate salary match percentage.
        
        Args:
            expected_salary: Candidate's expected salary
            salary_min: Minimum salary offered by the job
            salary_max: Maximum salary offered by the job
            
        Returns:
            Match percentage (0-100)
        """
        # Handle case where no salary info is provided
        if salary_min == 0 and salary_max == 0:
            return 100.0  # Can't evaluate, assume match
        
        if expected_salary == 0:
            return 100.0  # Candidate hasn't specified, assume match
        
        # Calculate midpoint of job salary range
        salary_mid = (salary_min + salary_max) / 2
        
        # Check if expected salary is within range
        if salary_min <= expected_salary <= salary_max:
            return 100.0
        
        # Calculate percentage difference from midpoint
        if expected_salary < salary_min:
            # Candidate expects less than minimum
            diff = salary_min - expected_salary
            pct_diff = (diff / salary_mid) * 100
            # Lose up to 30% based on how much below
            match = 100.0 - min(pct_diff, 30.0)
        else:
            # Candidate expects more than maximum
            diff = expected_salary - salary_max
            pct_diff = (diff / salary_mid) * 100
            # Lose up to 40% based on how much above
            match = 100.0 - min(pct_diff, 40.0)
        
        return max(30.0, match)  # Minimum 30% match
    
    def get_salary_details(
        self,
        expected_salary: int,
        salary_min: int,
        salary_max: int
    ) -> Dict:
        """
        Get detailed salary matching information.
        
        Args:
            expected_salary: Candidate's expected salary
            salary_min: Minimum salary offered by the job
            salary_max: Maximum salary offered by the job
            
        Returns:
            Dictionary with detailed salary info
        """
        match_score = self.calculate_salary_match(
            expected_salary, 
            salary_min, 
            salary_max
        )
        
        # Determine compatibility status
        if salary_min == 0 and salary_max == 0:
            status = 'Not Specified'
        elif expected_salary < salary_min:
            status = 'Below Range'
        elif expected_salary > salary_max:
            status = 'Above Range'
        else:
            status = 'Within Range'
        
        return {
            'match_score': match_score,
            'status': status,
            'expected_salary': expected_salary,
            'salary_range': f"${salary_min:,} - ${salary_max:,}" if salary_min or salary_max else 'Not Specified',
            'salary_midpoint': (salary_min + salary_max) / 2 if salary_min or salary_max else 0
        }
    
    def calculate_salary_alignment(
        self,
        expected_salary: int,
        salary_min: int,
        salary_max: int
    ) -> Dict:
        """
        Calculate salary alignment with recommendations.
        
        Args:
            expected_salary: Candidate's expected salary
            salary_min: Minimum salary offered by the job
            salary_max: Maximum salary offered by the job
            
        Returns:
            Dictionary with alignment analysis
        """
        if salary_min == 0 and salary_max == 0:
            return {
                'alignment': 'neutral',
                'recommendation': 'Salary not disclosed - discuss during interview',
                'candidate_advantage': 0
            }
        
        salary_mid = (salary_min + salary_max) / 2
        
        if expected_salary < salary_min:
            diff_pct = ((salary_min - expected_salary) / salary_mid) * 100
            return {
                'alignment': 'below_market',
                'recommendation': 'Candidate may be undervalued - great hire value',
                'candidate_advantage': diff_pct
            }
        elif expected_salary > salary_max:
            diff_pct = ((expected_salary - salary_max) / salary_mid) * 100
            return {
                'alignment': 'above_market',
                'recommendation': 'Candidate salary expectation exceeds budget',
                'candidate_advantage': -diff_pct
            }
        else:
            return {
                'alignment': 'market_competitive',
                'recommendation': 'Salary expectations align with offer range',
                'candidate_advantage': 0
            }
