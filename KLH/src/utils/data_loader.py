"""Data loader utility for loading sample data"""

import json
import os
from typing import List
from ..models.candidate import Candidate
from ..models.job import Job


class DataLoader:
    """Utility class for loading sample data"""
    
    @staticmethod
    def load_candidates(file_path: str = None) -> List[Candidate]:
        """
        Load candidate data from JSON file.
        
        Args:
            file_path: Path to candidates JSON file
            
        Returns:
            List of Candidate objects
        """
        if file_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            file_path = os.path.join(base_dir, 'data', 'sample_candidates.json')
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return [Candidate.from_dict(c) for c in data]
    
    @staticmethod
    def load_jobs(file_path: str = None) -> List[Job]:
        """
        Load job data from JSON file.
        
        Args:
            file_path: Path to jobs JSON file
            
        Returns:
            List of Job objects
        """
        if file_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            file_path = os.path.join(base_dir, 'data', 'sample_jobs.json')
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return [Job.from_dict(j) for j in data]
    
    @staticmethod
    def save_matches(matches: List[dict], file_path: str = None):
        """
        Save match results to JSON file.
        
        Args:
            matches: List of match dictionaries
            file_path: Path to output file
        """
        if file_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            file_path = os.path.join(base_dir, 'data', 'match_results.json')
        
        with open(file_path, 'w') as f:
            json.dump(matches, f, indent=2)
    
    @staticmethod
    def load_matches(file_path: str = None) -> List[dict]:
        """
        Load match results from JSON file.
        
        Args:
            file_path: Path to match results JSON file
            
        Returns:
            List of match dictionaries
        """
        if file_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            file_path = os.path.join(base_dir, 'data', 'match_results.json')
        
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, 'r') as f:
            return json.load(f)
