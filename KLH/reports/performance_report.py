"""
Performance Report Generator for AI Job Matching Engine

This module generates algorithm performance reports including:
- Precision, Recall, F1-Score metrics
- Match score distribution analysis
- Feature importance visualization
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

from src.models.candidate import Candidate
from src.models.job import Job
from src.matching.matching_engine import MatchingEngine
from src.utils.data_loader import DataLoader


class PerformanceReporter:
    """Generate performance reports for the matching algorithm"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.engine = MatchingEngine()
        
    def load_sample_data(self):
        """Load sample candidates and jobs"""
        self.candidates = self.data_loader.load_candidates()
        self.jobs = self.data_loader.load_jobs()
        
    def run_matching(self):
        """Run matching on all candidates and jobs"""
        self.all_matches = []
        
        for candidate in self.candidates:
            matches = self.engine.match_candidate_to_jobs(candidate, self.jobs, min_threshold=0)
            for match in matches:
                self.all_matches.append(match)
        
        return self.all_matches
    
    def calculate_match_distribution(self):
        """Calculate match score distribution"""
        if not self.all_matches:
            return {}
        
        scores = [m.match_score for m in self.all_matches]
        
        return {
            'mean': np.mean(scores),
            'median': np.median(scores),
            'std': np.std(scores),
            'min': np.min(scores),
            'max': np.max(scores),
            'q25': np.percentile(scores, 25),
            'q75': np.percentile(scores, 75)
        }
    
    def categorize_matches(self):
        """Categorize matches by score levels"""
        if not self.all_matches:
            return {}
        
        scores = [m.match_score for m in self.all_matches]
        
        excellent = len([s for s in scores if s >= 70])
        good = len([s for s in scores if 50 <= s < 70])
        fair = len([s for s in scores if 30 <= s < 50])
        low = len([s for s in scores if s < 30])
        
        total = len(scores)
        
        return {
            'excellent': {'count': excellent, 'percentage': (excellent/total)*100},
            'good': {'count': good, 'percentage': (good/total)*100},
            'fair': {'count': fair, 'percentage': (fair/total)*100},
            'low': {'count': low, 'percentage': (low/total)*100},
            'total': total
        }
    
    def analyze_component_scores(self):
        """Analyze individual component scores"""
        if not self.all_matches:
            return {}
        
        skill_scores = [m.skill_match for m in self.all_matches]
        exp_scores = [m.experience_match for m in self.all_matches]
        loc_scores = [m.location_match for m in self.all_matches]
        sal_scores = [m.salary_match for m in self.all_matches]
        
        return {
            'skill_match': {
                'mean': np.mean(skill_scores),
                'std': np.std(skill_scores),
                'min': np.min(skill_scores),
                'max': np.max(skill_scores)
            },
            'experience_match': {
                'mean': np.mean(exp_scores),
                'std': np.std(exp_scores),
                'min': np.min(exp_scores),
                'max': np.max(exp_scores)
            },
            'location_match': {
                'mean': np.mean(loc_scores),
                'std': np.std(loc_scores),
                'min': np.min(loc_scores),
                'max': np.max(loc_scores)
            },
            'salary_match': {
                'mean': np.mean(sal_scores),
                'std': np.std(sal_scores),
                'min': np.min(sal_scores),
                'max': np.max(sal_scores)
            }
        }
    
    def find_top_performing_pairs(self, top_n=10):
        """Find top performing candidate-job pairs"""
        if not self.all_matches:
            return []
        
        sorted_matches = sorted(self.all_matches, key=lambda x: x.match_score, reverse=True)
        
        results = []
        for match in sorted_matches[:top_n]:
            candidate = next((c for c in self.candidates if c.candidate_id == match.candidate_id), None)
            job = next((j for j in self.jobs if j.job_id == match.job_id), None)
            
            if candidate and job:
                results.append({
                    'candidate_name': candidate.name,
                    'job_title': job.title,
                    'company': job.company,
                    'match_score': match.match_score,
                    'skill_match': match.skill_match,
                    'experience_match': match.experience_match,
                    'location_match': match.location_match,
                    'salary_match': match.salary_match
                })
        
        return results
    
    def generate_visualizations(self, output_dir='reports/output'):
        """Generate visualization plots"""
        os.makedirs(output_dir, exist_ok=True)
        
        if not self.all_matches:
            print("No matches to visualize")
            return
        
        # Set style
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # 1. Match Score Distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        scores = [m.match_score for m in self.all_matches]
        ax.hist(scores, bins=20, edgecolor='black', alpha=0.7, color='#1E3A5F')
        ax.axvline(np.mean(scores), color='red', linestyle='--', label=f'Mean: {np.mean(scores):.1f}')
        ax.axvline(np.median(scores), color='orange', linestyle='--', label=f'Median: {np.median(scores):.1f}')
        ax.set_xlabel('Match Score (%)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Match Score Distribution', fontsize=14, fontweight='bold')
        ax.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'match_distribution.png'), dpi=150)
        plt.close()
        
        # 2. Component Scores Comparison
        fig, ax = plt.subplots(figsize=(10, 6))
        component_data = {
            'Skills': [m.skill_match for m in self.all_matches],
            'Experience': [m.experience_match for m in self.all_matches],
            'Location': [m.location_match for m in self.all_matches],
            'Salary': [m.salary_match for m in self.all_matches]
        }
        
        df = pd.DataFrame(component_data)
        df.boxplot(ax=ax)
        ax.set_ylabel('Score (%)', fontsize=12)
        ax.set_title('Component Scores Distribution', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'component_scores.png'), dpi=150)
        plt.close()
        
        # 3. Match Categories Pie Chart
        fig, ax = plt.subplots(figsize=(8, 8))
        categories = self.categorize_matches()
        if categories:
            labels = ['Excellent (≥70%)', 'Good (50-70%)', 'Fair (30-50%)', 'Low (<30%)']
            sizes = [
                categories['excellent']['percentage'],
                categories['good']['percentage'],
                categories['fair']['percentage'],
                categories['low']['percentage']
            ]
            colors = ['#2ECC71', '#F39C12', '#E67E22', '#E74C3C']
            explode = (0.05, 0.05, 0.05, 0.05)
            
            ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', shadow=True, startangle=90)
            ax.axis('equal')
            ax.set_title('Match Categories Distribution', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'match_categories.png'), dpi=150)
            plt.close()
        
        print(f"Visualizations saved to {output_dir}")
    
    def generate_report(self):
        """Generate comprehensive performance report"""
        print("=" * 60)
        print("AI Job Matching Engine - Performance Report")
        print("=" * 60)
        
        # Load data
        print("\n1. Loading data...")
        self.load_sample_data()
        print(f"   - Candidates: {len(self.candidates)}")
        print(f"   - Jobs: {len(self.jobs)}")
        
        # Run matching
        print("\n2. Running matching algorithm...")
        matches = self.run_matching()
        print(f"   - Total matches generated: {len(matches)}")
        
        # Distribution analysis
        print("\n3. Match Score Distribution:")
        distribution = self.calculate_match_distribution()
        print(f"   - Mean: {distribution['mean']:.2f}%")
        print(f"   - Median: {distribution['median']:.2f}%")
        print(f"   - Std Dev: {distribution['std']:.2f}%")
        print(f"   - Range: {distribution['min']:.2f}% - {distribution['max']:.2f}%")
        print(f"   - IQR: {distribution['q25']:.2f}% - {distribution['q75']:.2f}%")
        
        # Categories
        print("\n4. Match Categories:")
        categories = self.categorize_matches()
        print(f"   - Excellent (≥70%): {categories['excellent']['count']} ({categories['excellent']['percentage']:.1f}%)")
        print(f"   - Good (50-70%): {categories['good']['count']} ({categories['good']['percentage']:.1f}%)")
        print(f"   - Fair (30-50%): {categories['fair']['count']} ({categories['fair']['percentage']:.1f}%)")
        print(f"   - Low (<30%): {categories['low']['count']} ({categories['low']['percentage']:.1f}%)")
        
        # Component analysis
        print("\n5. Component Score Analysis:")
        components = self.analyze_component_scores()
        for comp, stats in components.items():
            print(f"   - {comp}:")
            print(f"       Mean: {stats['mean']:.2f}%, Std: {stats['std']:.2f}%")
        
        # Top matches
        print("\n6. Top 10 Matching Pairs:")
        top_matches = self.find_top_performing_pairs(10)
        for i, match in enumerate(top_matches, 1):
            print(f"   {i}. {match['candidate_name']} → {match['job_title']} at {match['company']}")
            print(f"      Score: {match['match_score']:.1f}% "
                  f"(Skills: {match['skill_match']:.1f}%, "
                  f"Exp: {match['experience_match']:.1f}%, "
                  f"Loc: {match['location_match']:.1f}%, "
                  f"Sal: {match['salary_match']:.1f}%)")
        
        # Generate visualizations
        print("\n7. Generating visualizations...")
        self.generate_visualizations()
        
        print("\n" + "=" * 60)
        print("Report Generation Complete!")
        print("=" * 60)


def main():
    """Main function to run the performance report"""
    reporter = PerformanceReporter()
    reporter.generate_report()


if __name__ == '__main__':
    import pandas as pd
    main()
