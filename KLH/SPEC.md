# AI-Based Smart Job Matching Engine - Specification

## 1. Project Overview

**Project Title:** AI-Based Smart Job Matching Engine  
**Project Type:** Machine Learning / Recommendation System  
**Core Functionality:** An intelligent job-matching platform that connects jobseekers with employers through skill-based matching, experience filtering, location-based recommendations, and salary compatibility checks.  
**Target Users:** Jobseekers seeking employment and Employers/HR teams looking for candidates

---

## 2. Tech Stack

- **Language:** Python 3.9+
- **Framework:** Flask (API), Streamlit (Dashboard)
- **Machine Learning:** scikit-learn, NumPy, Pandas
- **Data Processing:** Python collections, difflib (string matching)
- **Visualization:** Matplotlib, Seaborn (for performance reports)

---

## 3. UI/UX Specification

### Color Palette
- **Primary:** `#1E3A5F` (Deep Navy Blue)
- **Secondary:** `#2ECC71` (Emerald Green - for matches/success)
- **Accent:** `#F39C12` (Amber - for highlights)
- **Background:** `#F8F9FA` (Light Gray)
- **Text Primary:** `#2C3E50` (Dark Slate)
- **Text Secondary:** `#7F8C8D` (Gray)
- **Error:** `#E74C3C` (Red)
- **Card Background:** `#FFFFFF` (White)

### Typography
- **Headings:** 'Poppins', sans-serif (bold, sizes: 32px/24px/18px)
- **Body:** 'Open Sans', sans-serif (regular, size: 14px)
- **Monospace:** 'Fira Code' (for code/data display)

### Layout Structure
- **Navigation:** Top horizontal bar with logo and menu items
- **Main Content:** Centered container, max-width 1200px
- **Cards:** Rounded corners (12px), subtle shadows
- **Spacing:** 16px base unit, multiples of 8px

### Dashboard Components
- **Match Score Cards:** Display percentage match with color coding (green >70%, amber 40-70%, red <40%)
- **Skill Tags:** Pill-shaped badges with primary color
- **Progress Bars:** For skill match visualization
- **Data Tables:** Alternating row colors, sortable headers

---

## 4. Functionality Specification

### 4.1 Core Features

#### A. Skill-Based Matching Algorithm
- Extract skills from job descriptions and candidate profiles
- Use text similarity (TF-IDF + cosine similarity) for skill matching
- Calculate skill match percentage: (matched skills / total required skills) × 100
- Support both exact and fuzzy matching for skill names

#### B. Experience & Qualification Filtering
- Parse years of experience from job postings and candidate resumes
- Filter jobs where candidate's experience meets minimum requirements
- Consider education level qualifications
- Experience weight: 25% of total match score

#### C. Location-Based Recommendation
- Support city, state, and remote work preferences
- Calculate location proximity score (exact match = 100%, same state = 70%, different = 30%)
- Support remote work matching
- Location weight: 15% of total match score

#### D. Salary Compatibility Assessment
- Parse salary ranges from job postings
- Compare candidate's expected salary with job salary range
- Calculate salary match: 100% if within range, lower if below/above
- Salary weight: 20% of total match score

#### E. Overall Match Ranking
- Weighted scoring system:
  - Skills: 40%
  - Experience: 25%
  - Salary: 20%
  - Location: 15%
- Rank candidates/jobs by match score
- Display top N matches with detailed breakdown

### 4.2 Data Models

#### Candidate Profile
```
- candidate_id: unique identifier
- name: full name
- email: contact email
- skills: list of skills
- years_experience: integer
- education: highest education level
- preferred_location: city/state
- expected_salary: integer (annual)
- resume_text: full resume text
```

#### Job Posting
```
- job_id: unique identifier
- title: job title
- company: company name
- required_skills: list of skills
- min_experience: integer
- education_required: minimum education
- location: city/state
- salary_min: integer
- salary_max: integer
- description: full job description
- is_remote: boolean
```

#### Match Result
```
- candidate_id: reference
- job_id: reference
- match_score: float (0-100)
- skill_match: float
- experience_match: float
- location_match: float
- salary_match: float
- matched_skills: list
- missing_skills: list
```

### 4.3 User Interfaces

#### A. Candidate-Job Matching Demo (Streamlit)
- Input form for candidate profile
- Display matched jobs with scores
- Show skill gap analysis
- Filter by location, salary range

#### B. Match Ranking Dashboard (Streamlit)
- Employer view: ranked candidates for their jobs
- Candidate view: ranked jobs for their profile
- Interactive charts showing match distribution
- Detailed breakdown of each matching criterion

#### C. API Endpoints (Flask)
- POST /api/match - Get matches for a candidate
- POST /api/match/candidates - Get candidates for a job
- GET /api/jobs - List all jobs
- GET /api/candidates - List all candidates
- GET /api/health - Health check

### 4.4 Algorithm Performance Report
- Precision, Recall, F1-Score metrics
- Confusion matrix visualization
- Match score distribution histogram
- Feature importance analysis
- Sample predictions with explanations

---

## 5. Project Structure

```
KLH/
├── SPEC.md
├── README.md
├── requirements.txt
├── data/
│   ├── sample_candidates.json
│   ├── sample_jobs.json
│   └── match_results.json
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── candidate.py
│   │   ├── job.py
│   │   └── match_result.py
│   ├── matching/
│   │   ├── __init__.py
│   │   ├── skill_matcher.py
│   │   ├── experience_matcher.py
│   │   ├── location_matcher.py
│   │   ├── salary_matcher.py
│   │   └── matching_engine.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── utils/
│       ├── __init__.py
│       └── data_loader.py
├── dashboard/
│   ├── __init__.py
│   └── app.py
├── reports/
│   └── performance_report.py
└── tests/
    ├── __init__.py
    └── test_matching.py
```

---

## 6. Acceptance Criteria

### Functional Requirements
- [ ] Skill matching algorithm returns accurate match percentages
- [ ] Experience filter correctly excludes non-qualifying candidates
- [ ] Location matching handles remote work preferences
- [ ] Salary compatibility accurately assesses range overlaps
- [ ] Overall match ranking produces sensible results

### User Interface Requirements
- [ ] Demo interface accepts candidate input and displays matches
- [ ] Dashboard shows ranked results with visual indicators
- [ ] Match breakdown displays individual component scores
- [ ] Interactive filters work correctly

### Performance Requirements
- [ ] Matching algorithm processes 100 candidates × 50 jobs in <2 seconds
- [ ] API responds within 500ms for match requests
- [ ] Dashboard loads within 3 seconds

### Deliverables
- [ ] Smart matching engine (Python modules)
- [ ] Candidate-job matching demo (Streamlit app)
- [ ] Match ranking dashboard (Streamlit app)
- [ ] Algorithm performance report (generated output)

---

## 7. Sample Data

### Sample Candidates (10)
Include diverse profiles with varying skill sets, experience levels, locations, and salary expectations

### Sample Jobs (15)
Include various job types across different industries, locations, and salary ranges

---

## 8. Algorithm Details

### Skill Matching (TF-IDF + Cosine Similarity)
1. Combine all skills into a corpus
2. Create TF-IDF vectors for candidate skills and job requirements
3. Calculate cosine similarity between vectors
4. Extract matched and missing skills

### Weight Assignment
- Skills: 40% (most important for job fit)
- Experience: 25% (requirement fulfillment)
- Salary: 20% (mutual compatibility)
- Location: 15% (preference matching)

### Score Normalization
- All scores scaled to 0-100
- Weighted average for final score
- Minimum threshold: 30% (below = no match)
