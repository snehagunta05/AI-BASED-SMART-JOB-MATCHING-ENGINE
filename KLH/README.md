# AI-Based Smart Job Matching Engine

An intelligent job-matching platform that connects jobseekers with employers through skill-based matching, experience filtering, location-based recommendations, and salary compatibility checks.

## 🎯 Overview

This project implements a comprehensive job matching engine using machine learning and recommendation system techniques. It matches candidates to jobs based on multiple criteria with weighted scoring.

## 🚀 Features

- **Skill-Based Matching**: TF-IDF + Cosine Similarity for skill matching
- **Experience Filtering**: Experience and education level matching
- **Location Recommendations**: Location proximity and remote work support
- **Salary Compatibility**: Salary range matching and compatibility assessment
- **Match Ranking**: Weighted scoring system (Skills 40%, Experience 25%, Salary 20%, Location 15%)

## 📁 Project Structure

```
KLH/
├── SPEC.md                      # Detailed specification
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── data/
│   ├── sample_candidates.json   # 10 sample candidates
│   ├── sample_jobs.json         # 15 sample jobs
│   └── match_results.json       # Generated matches
├── src/
│   ├── main.py                  # API entry point
│   ├── models/                  # Data models
│   │   ├── candidate.py
│   │   ├── job.py
│   │   └── match_result.py
│   ├── matching/                # Matching algorithms
│   │   ├── skill_matcher.py
│   │   ├── experience_matcher.py
│   │   ├── location_matcher.py
│   │   ├── salary_matcher.py
│   │   └── matching_engine.py
│   ├── api/                     # Flask REST API
│   │   └── routes.py
│   └── utils/                   # Utilities
│       └── data_loader.py
├── dashboard/
│   └── app.py                   # Streamlit dashboard
├── reports/
│   └── performance_report.py    # Performance analysis
└── tests/
    └── test_matching.py         # Unit tests
```

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **Web Framework**: Flask, Streamlit
- **Machine Learning**: scikit-learn, NumPy, Pandas
- **Visualization**: Matplotlib, Seaborn

## 📦 Installation

1. Clone the repository:
```
bash
git clone <repository-url>
cd KLH
```

2. Create a virtual environment:
```
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
bash
pip install -r requirements.txt
```

## 🎮 Usage

### Running the API Server

```
bash
cd src
python main.py
```

API will be available at `http://localhost:5000`

### Running the Dashboard

```
bash
cd dashboard
streamlit run app.py
```

Dashboard will open at `http://localhost:8501`

### Running Tests

```
bash
pytest tests/ -v
```

### Generating Performance Report

```
bash
cd reports
python performance_report.py
```

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/candidates` | GET | List all candidates |
| `/api/jobs` | GET | List all jobs |
| `/api/match` | POST | Match candidate to jobs |
| `/api/match/candidates` | POST | Match candidates to job |
| `/api/match/all` | GET | Get all matches |

## 📊 Sample Data

- **10 Candidates**: Various skill levels, experience, locations, salary expectations
- **15 Jobs**: Different industries, locations, salary ranges

## 🔧 Configuration

### Matching Weights

Edit `src/matching/matching_engine.py` to customize weights:

```
python
DEFAULT_WEIGHTS = {
    'skills': 0.40,      # 40% - Most important
    'experience': 0.25,  # 25%
    'salary': 0.20,      # 20%
    'location': 0.15      # 15%
}
```

## 📈 Performance

- Processes 100 candidates × 50 jobs in <2 seconds
- API response time <500ms
- Dashboard loads in <3 seconds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License

## 👥 Authors

- AI Job Matching Team

---

Made with ❤️ for better job matching
