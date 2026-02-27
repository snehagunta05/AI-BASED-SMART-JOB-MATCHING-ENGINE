"""Location-based matching algorithm"""

import re
from typing import Tuple, Dict, List


class LocationMatcher:
    """Handles location-based matching between candidates and jobs"""
    
    # Major US states mapping
    STATES = {
        'AL': 'ALABAMA', 'AK': 'ALASKA', 'AZ': 'ARIZONA', 'AR': 'ARKANSAS',
        'CA': 'CALIFORNIA', 'CO': 'COLORADO', 'CT': 'CONNECTICUT', 'DE': 'DELAWARE',
        'FL': 'FLORIDA', 'GA': 'GEORGIA', 'HI': 'HAWAII', 'ID': 'IDAHO',
        'IL': 'ILLINOIS', 'IN': 'INDIANA', 'IA': 'IOWA', 'KS': 'KANSAS',
        'KY': 'KENTUCKY', 'LA': 'LOUISIANA', 'ME': 'MAINE', 'MD': 'MARYLAND',
        'MA': 'MASSACHUSETTS', 'MI': 'MICHIGAN', 'MN': 'MINNESOTA', 'MS': 'MISSISSIPPI',
        'MO': 'MISSOURI', 'MT': 'MONTANA', 'NE': 'NEBRASKA', 'NV': 'NEVADA',
        'NH': 'NEW HAMPSHIRE', 'NJ': 'NEW JERSEY', 'NM': 'NEW MEXICO', 'NY': 'NEW YORK',
        'NC': 'NORTH CAROLINA', 'ND': 'NORTH DAKOTA', 'OH': 'OHIO', 'OK': 'OKLAHOMA',
        'OR': 'OREGON', 'PA': 'PENNSYLVANIA', 'RI': 'RHODE ISLAND', 'SC': 'SOUTH CAROLINA',
        'SD': 'SOUTH DAKOTA', 'TN': 'TENNESSEE', 'TX': 'TEXAS', 'UT': 'UTAH',
        'VT': 'VERMONT', 'VA': 'VIRGINIA', 'WA': 'WASHINGTON', 'WV': 'WEST VIRGINIA',
        'WI': 'WISCONSIN', 'WY': 'WYOMING', 'DC': 'DISTRICT OF COLUMBIA'
    }
    
    # Major tech hubs (considered as same region)
    TECH_HUBS = {
        'SAN FRANCISCO': 'BAY AREA',
        'PALO ALTO': 'BAY AREA',
        'MOUNTAIN VIEW': 'BAY AREA',
        'SUNNYVALE': 'BAY AREA',
        'SAN JOSE': 'BAY AREA',
        'OAKLAND': 'BAY AREA',
        'BERKELEY': 'BAY AREA',
        'NEW YORK': 'NEW YORK METRO',
        'BROOKLYN': 'NEW YORK METRO',
        'JERSEY CITY': 'NEW YORK METRO',
        'MANHATTAN': 'NEW YORK METRO',
        'LOS ANGELES': 'LOS ANGELES',
        'SEATTLE': 'SEATTLE',
        'AUSTIN': 'AUSTIN',
        'BOSTON': 'BOSTON',
        'CHICAGO': 'CHICAGO',
        'DENVER': 'DENVER',
        'MIAMI': 'MIAMI',
    }
    
    def __init__(self):
        pass
    
    def parse_location(self, location: str) -> Dict:
        """
        Parse location string into city and state.
        
        Args:
            location: Location string (e.g., "San Francisco, CA" or "Remote")
            
        Returns:
            Dictionary with parsed location info
        """
        if not location:
            return {'city': '', 'state': '', 'is_remote': False, 'region': ''}
        
        location = location.strip().upper()
        
        # Check for remote
        if 'REMOTE' in location or 'REMOTE' in location:
            return {'city': '', 'state': '', 'is_remote': True, 'region': 'REMOTE'}
        
        # Try to parse city, state format
        if ',' in location:
            parts = location.split(',')
            city = parts[0].strip()
            state = parts[1].strip() if len(parts) > 1 else ''
        else:
            # Check if it's a state name or abbreviation
            if len(location) == 2:
                city = ''
                state = location
            else:
                city = location
                state = ''
        
        # Resolve state abbreviation
        if state in self.STATES:
            state = self.STATES[state]
        
        # Determine region
        region = self.TECH_HUBS.get(city, state if state else city)
        
        return {
            'city': city,
            'state': state,
            'is_remote': False,
            'region': region
        }
    
    def calculate_location_match(
        self,
        candidate_location: str,
        job_location: str,
        is_remote_job: bool = False
    ) -> float:
        """
        Calculate location match percentage.
        
        Args:
            candidate_location: Candidate's preferred location
            job_location: Job location
            is_remote_job: Whether the job is remote
            
        Returns:
            Match percentage (0-100)
        """
        # Handle remote jobs
        if is_remote_job or 'REMOTE' in job_location.upper():
            # If candidate prefers remote, perfect match
            if 'REMOTE' in candidate_location.upper():
                return 100.0
            # Remote jobs are somewhat acceptable regardless of location
            return 80.0
        
        # Parse locations
        candidate_loc = self.parse_location(candidate_location)
        job_loc = self.parse_location(job_location)
        
        # If candidate wants remote only
        if candidate_loc['is_remote']:
            return 60.0  # Will consider hybrid/onsite as partial
        
        # Exact city match
        if candidate_loc['city'] and job_loc['city']:
            if candidate_loc['city'] == job_loc['city']:
                return 100.0
        
        # Same state
        if candidate_loc['state'] and job_loc['state']:
            if candidate_loc['state'] == job_loc['state']:
                return 75.0
        
        # Same region (tech hub)
        if candidate_loc['region'] and job_loc['region']:
            if candidate_loc['region'] == job_loc['region']:
                return 70.0
        
        # Different location
        return 30.0
    
    def get_location_details(
        self,
        candidate_location: str,
        job_location: str,
        is_remote_job: bool = False
    ) -> Dict:
        """
        Get detailed location matching information.
        
        Args:
            candidate_location: Candidate's preferred location
            job_location: Job location
            is_remote_job: Whether the job is remote
            
        Returns:
            Dictionary with detailed location info
        """
        candidate_loc = self.parse_location(candidate_location)
        job_loc = self.parse_location(job_location)
        match_score = self.calculate_location_match(
            candidate_location, 
            job_location, 
            is_remote_job
        )
        
        # Determine match type
        if is_remote_job or 'REMOTE' in job_location.upper():
            match_type = 'Remote'
        elif candidate_loc['city'] == job_loc['city']:
            match_type = 'Same City'
        elif candidate_loc['state'] == job_loc['state']:
            match_type = 'Same State'
        elif candidate_loc['region'] == job_loc['region']:
            match_type = 'Same Region'
        else:
            match_type = 'Different Location'
        
        return {
            'match_score': match_score,
            'match_type': match_type,
            'candidate_location': candidate_loc,
            'job_location': job_loc
        }
