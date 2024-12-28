# PIESB (Projet Informatique Esprit School of Business)

## Overview

PIESB is a comprehensive web application designed to analyze and recommend academic programs and professional careers based on the provided user competencies and preferences. The system integrates web scraping, data cleaning, statistical analysis, clustering, and machine learning techniques to provide recommendations.

---

## Features

- **Web Scraping**: Automates data collection from Esprit School of Business and Tunisian Competence Directory.
- **Data Cleaning and Transformation**: Processes raw data into structured formats for analysis.
- **Clustering and Statistical Analysis**: Groups programs and metiers based on shared competencies using machine learning.
- **Recommendation System**: Suggests academic programs and related metiers to users based on their competencies.
- **Real-time Suggestions**: Provides suggestions as users type their competencies.
- **Interactive Frontend**: A user-friendly interface to search and view recommendations.

---

## Project Structure

PIESB/
├── analysis/
│   ├── clean_and_validate.py
│   ├── clustering.py
│   ├── generate_json.py
│   ├── stat_analysis.py
│   ├── transform_and_analyze.py
│   ├── visualize_data.py
│   └── data/
├── backend/
│   ├── app.py
│   ├── models/
│   │   ├── recommendations.py
│   │   └── similar_programs.py
│   ├── routes/
│   │   ├── competence_routes.py
│   │   ├── suggestion_routes.py
│   ├── utils/
│   │   ├── database.py
│   │   └── preprocessing.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CompetenceInput.js
│   │   │   ├── ProgramCard.js
│   │   │   ├── Recommendations.js
│   │   │   └── Search.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README.md
Setup Instructions
Prerequisites
Python 3.8 or above
Node.js and npm
Virtual environment (recommended)
Backend Setup
# Install dependencies:
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run the backend server:
flask run
Frontend Setup

# Install dependencies:
cd frontend
npm install

# Run the development server:
npm start

# Graph Analysis (Analysis Folder)
## Visualization Insights
### Competence Distribution Heatmap:

Shows the similarity between programs and metiers based on shared competencies.
High-density areas indicate overlapping or similar skill requirements.
### Clustering Visualization:

Displays clusters of academic programs and metiers.
Each cluster represents groups with similar characteristics.
### Competence Count Histogram:

Visualizes the distribution of competencies per program and metier.
Helps identify programs/metiers with high competency requirements.
Future Improvements
Enhanced Similarity Metrics: Incorporate NLP techniques like word embeddings for better similarity detection.
Advanced Filtering: Allow filtering recommendations by specific domains or job types.
User Feedback Integration: Use user feedback to refine recommendation algorithms.
### Contributors
Project Owner: Med Saief Bardi , Med Skander Hassan
Developer: Med Saief Bardi , Med Skander Hassan
License
This project is licensed under the MIT License. See the LICENSE file for details.
