"""Streamlit Dashboard for AI-Based Smart Job Matching Engine"""

import streamlit as st
import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.candidate import Candidate
from src.models.job import Job
from src.matching.matching_engine import MatchingEngine
from src.utils.data_loader import DataLoader


# Page configuration
st.set_page_config(
    page_title="AI Job Matching Engine",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #1E3A5F;
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #2C3E50;
        padding: 10px;
    }
    .match-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .score-excellent {
        color: #2ECC71;
        font-weight: bold;
    }
    .score-good {
        color: #F39C12;
        font-weight: bold;
    }
    .score-fair {
        color: #E67E22;
        font-weight: bold;
    }
    .score-low {
        color: #E74C3C;
        font-weight: bold;
    }
    .skill-tag {
        background-color: #1E3A5F;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 2px;
        display: inline-block;
        font-size: 12px;
    }
    .missing-skill {
        background-color: #E74C3C;
    }
    .matched-skill {
        background-color: #2ECC71;
    }
    .stat-box {
        background-color: #F8F9FA;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: #1E3A5F;
    }
    .stat-label {
        font-size: 14px;
        color: #7F8C8D;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load sample data"""
    data_loader = DataLoader()
    candidates = data_loader.load_candidates()
    jobs = data_loader.load_jobs()
    return candidates, jobs


def get_score_class(score):
    """Get CSS class based on score"""
    if score >= 70:
        return "score-excellent"
    elif score >= 50:
        return "score-good"
    elif score >= 30:
        return "score-fair"
    else:
        return "score-low"


def display_match_card(match, job=None, candidate=None):
    """Display a match result card"""
    score_class = get_score_class(match.match_score)
    
    with st.container():
        st.markdown('<div class="match-card">', unsafe_allow_html=True)
        
        # Header with score
        col1, col2 = st.columns([3, 1])
        with col1:
            if job:
                st.markdown(f"### {job.title} at {job.company}")
            if candidate:
                st.markdown(f"### {candidate.name}")
        with col2:
            st.markdown(f"""
            <div style="text-align: right;">
                <span class="{score_class}" style="font-size: 32px;">{match.match_score:.1f}%</span>
                <br>
                <span style="color: #7F8C8D;">{match.get_match_level()}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed scores
        st.markdown("#### Match Breakdown")
        score_cols = st.columns(4)
        
        with score_cols[0]:
            st.metric("Skills", f"{match.skill_match:.1f}%")
        with score_cols[1]:
            st.metric("Experience", f"{match.experience_match:.1f}%")
        with score_cols[2]:
            st.metric("Location", f"{match.location_match:.1f}%")
        with score_cols[3]:
            st.metric("Salary", f"{match.salary_match:.1f}%")
        
        # Skills
        if match.matched_skills or match.missing_skills:
            st.markdown("##### Skills")
            
            if match.matched_skills:
                st.markdown("**Matched:** ")
                skills_html = " ".join([f'<span class="skill-tag matched-skill">{s}</span>' 
                                       for s in match.matched_skills])
                st.markdown(skills_html, unsafe_allow_html=True)
            
            if match.missing_skills:
                st.markdown("**Missing:** ")
                skills_html = " ".join([f'<span class="skill-tag missing-skill">{s}</span>' 
                                       for s in match.missing_skills])
                st.markdown(skills_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


def candidate_matching_tab(candidates, jobs, matching_engine):
    """Candidate to Job Matching tab"""
    st.markdown('<p class="sub-header">Select or Create a Candidate Profile</p>', unsafe_allow_html=True)
    
    # Candidate selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_candidate_id = st.selectbox(
            "Select a candidate from sample data:",
            options=["-- Create New --"] + [c.candidate_id for c in candidates],
            format_func=lambda x: x if x == "-- Create New --" else f"{candidates[int(x[1:])-1].name} ({x})"
        )
    
    # Initialize candidate
    candidate = None
    
    if selected_candidate_id == "-- Create New --":
        # Create new candidate form
        st.markdown("### New Candidate Profile")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", "John Doe")
            email = st.text_input("Email", "john.doe@email.com")
            years_exp = st.number_input("Years of Experience", 0, 20, 3)
            expected_salary = st.number_input("Expected Salary ($)", 30000, 300000, 80000, step=5000)
        with col2:
            education = st.selectbox("Education", 
                ["High School", "Associate", "Bachelor's", "Master's", "PhD"])
            location = st.text_input("Preferred Location", "San Francisco, CA")
        
        skills_input = st.text_area("Skills (comma separated)", 
            "Python, Machine Learning, SQL, TensorFlow")
        
        skills = [s.strip() for s in skills_input.split(",") if s.strip()]
        
        candidate = Candidate(
            candidate_id="NEW",
            name=name,
            email=email,
            skills=skills,
            years_experience=years_exp,
            education=education,
            preferred_location=location,
            expected_salary=expected_salary,
            resume_text=""
        )
    else:
        # Use selected candidate
        candidate = next(c for c in candidates if c.candidate_id == selected_candidate_id)
        st.markdown(f"**Selected:** {candidate.name} | {candidate.years_experience} yrs exp | {len(candidate.skills)} skills")
    
    # Filter options
    st.markdown("### Filter Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_score = st.slider("Minimum Match Score", 0, 100, 30)
    with col2:
        location_filter = st.text_input("Location Filter", "")
    with col3:
        max_results = st.slider("Max Results", 5, 50, 10)
    
    # Run matching
    if st.button("Find Matching Jobs", type="primary"):
        with st.spinner("Finding best job matches..."):
            matches = matching_engine.match_candidate_to_jobs(candidate, jobs, min_score)
            
            # Apply location filter
            if location_filter:
                matches = [m for m in matches if any(location_filter.lower() in j.location.lower() 
                                                      for j in jobs if j.job_id == m.job_id)]
            
            # Limit results
            matches = matches[:max_results]
            
            st.markdown(f"## Found {len(matches)} Matching Jobs")
            
            if matches:
                for match in matches:
                    job = next(j for j in jobs if j.job_id == match.job_id)
                    display_match_card(match, job=job)
            else:
                st.warning("No jobs match your criteria. Try lowering the minimum score.")


def job_matching_tab(candidates, jobs, matching_engine):
    """Job to Candidate Matching tab"""
    st.markdown('<p class="sub-header">Select a Job to Find Matching Candidates</p>', unsafe_allow_html=True)
    
    # Job selection
    job_options = {f"{j.title} at {j.company} ({j.job_id})": j for j in jobs}
    selected_job = st.selectbox("Select a job:", options=list(job_options.keys()))
    
    job = job_options[selected_job]
    
    # Display job details
    with st.expander("Job Details", expanded=True):
        st.markdown(f"""
        - **Location:** {job.location} {'(Remote)' if job.is_remote else ''}
        - **Salary:** ${job.salary_min:,} - ${job.salary_max:,}
        - **Required Skills:** {', '.join(job.required_skills)}
        - **Min Experience:** {job.min_experience} years
        - **Education Required:** {job.education_required}
        """)
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        min_score = st.slider("Minimum Match Score", 0, 100, 30, key="job_min")
    with col2:
        max_results = st.slider("Max Candidates", 5, 50, 10, key="job_max")
    
    # Run matching
    if st.button("Find Matching Candidates", type="primary"):
        with st.spinner("Finding best candidate matches..."):
            matches = matching_engine.match_job_to_candidates(job, candidates, min_score)
            
            # Limit results
            matches = matches[:max_results]
            
            st.markdown(f"## Found {len(matches)} Matching Candidates")
            
            if matches:
                for match in matches:
                    candidate = next(c for c in candidates if c.candidate_id == match.candidate_id)
                    display_match_card(match, candidate=candidate)
            else:
                st.warning("No candidates match your criteria. Try lowering the minimum score.")


def ranking_dashboard_tab(candidates, jobs, matching_engine):
    """Match Ranking Dashboard tab"""
    st.markdown('<p class="sub-header">Top Matching Pairs Across All Data</p>', unsafe_allow_html=True)
    
    # Get all top matches
    with st.spinner("Calculating all matches..."):
        top_matches = matching_engine.get_top_matches(candidates, jobs, top_n=20)
    
    if top_matches:
        # Convert to DataFrame for display
        df = pd.DataFrame(top_matches)
        
        # Display as table
        st.dataframe(
            df[['candidate_name', 'job_title', 'company', 'match_score', 'skill_match', 'experience_match']],
            use_container_width=True,
            hide_index=True
        )
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Match Score Distribution")
            hist_data = df['match_score'].values
            st.bar_chart(pd.Series(hist_data).value_counts(bins=5).sort_index())
        
        with col2:
            st.markdown("### Component Scores Comparison")
            chart_data = df[['skill_match', 'experience_match', 'location_match', 'salary_match']].head(10)
            st.line_chart(chart_data)
        
        # Detailed view
        st.markdown("### Detailed Top Matches")
        for i, match in enumerate(top_matches[:10]):
            with st.expander(f"#{i+1}: {match['candidate_name']} → {match['job_title']} ({match['match_score']:.1f}%)"):
                st.markdown(f"""
                - **Candidate:** {match['candidate_name']} ({match['candidate_id']})
                - **Job:** {match['job_title']} at {match['company']}
                - **Overall Score:** {match['match_score']:.1f}%
                - **Skills:** {match['skill_match']:.1f}% | **Experience:** {match['experience_match']:.1f}% | **Location:** {match['location_match']:.1f}% | **Salary:** {match['salary_match']:.1f}%
                - **Matched Skills:** {', '.join(match['matched_skills'])}
                - **Missing Skills:** {', '.join(match['missing_skills'])}
                """)
    else:
        st.warning("No matches found. This might be due to strict filtering.")


def main():
    """Main dashboard function"""
    # Header
    st.markdown('<p class="main-header">🎯 AI-Based Smart Job Matching Engine</p>', unsafe_allow_html=True)
    
    # Load data
    try:
        candidates, jobs = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return
    
    # Initialize matching engine
    matching_engine = MatchingEngine()
    
    # Sidebar
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    
    # Tabs
    tab_names = ["Candidate Matching", "Job Matching", "Ranking Dashboard"]
    tab_candidate, tab_job, tab_ranking = st.tabs(tab_names)
    
    with tab_candidate:
        candidate_matching_tab(candidates, jobs, matching_engine)
    
    with tab_job:
        job_matching_tab(candidates, jobs, matching_engine)
    
    with tab_ranking:
        ranking_dashboard_tab(candidates, jobs, matching_engine)
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Data Summary")
    st.sidebar.markdown(f"- **Candidates:** {len(candidates)}")
    st.sidebar.markdown(f"- **Jobs:** {len(jobs)}")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Matching Weights")
    st.sidebar.markdown("- Skills: 40%")
    st.sidebar.markdown("- Experience: 25%")
    st.sidebar.markdown("- Salary: 20%")
    st.sidebar.markdown("- Location: 15%")


if __name__ == '__main__':
    main()
