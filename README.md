Clinical Trial Patient Matching System
A web-based application that helps patients in India find suitable clinical trials based on their medical and demographic profiles. The system uses AI/ML techniques, including TF-IDF and cosine similarity, to rank and recommend clinical trials with relevance scoring.

🔍 Overview
This system matches patients to trials by evaluating eligibility criteria, conditions, medications, and location proximity. Designed for ease of use with a clear interface and smart matching engine.

🧠 Key Features
Patient Profile Input: Age, gender, city, medical conditions, medications, allergies, lab results.

Location-Aware Filtering: Filters trials by Indian cities/states.

Disease-Specific Shortcuts: Quick-tag options for common Indian diseases.

Eligibility Matching: Dynamically checks inclusion/exclusion criteria.

Semantic Matching: Uses TF-IDF + cosine similarity to find relevant trials, even with varied terminology.

Weighted Scoring: Trials are ranked based on rule-based and semantic relevance.

Results with Contact Info: Displays trial details with a generic contact option (modal popup).

🛠 Tech Stack
Frontend: HTML, CSS, JavaScript

Backend: Flask (Python)

ML/NLP: Scikit-learn (TF-IDF, Cosine Similarity)

Data: JSON (for trial storage)

📁 Project Structure
php
Copy
Edit
clinical-trial-matcher/
├── app.py                 # Main Flask app and logic
├── trials.json            # Sample trial data (India-specific)
├── static/
│   ├── style.css          # Custom styling
│   └── script.js          # Form interaction and modal logic
└── templates/
    ├── index.html         # Home form page
    └── results.html       # Matched trials display
🚀 Installation
Clone this repo

bash
Copy
Edit
git clone https://github.com/your-username/clinical-trial-matcher.git
cd clinical-trial-matcher
Set up virtual environment (recommended)

bash
Copy
Edit
python -m venv venv
Activate environment

Windows:

bash
Copy
Edit
.\venv\Scripts\activate
macOS/Linux:

bash
Copy
Edit
source venv/bin/activate
Install dependencies

bash
Copy
Edit
pip install Flask scikit-learn
Run the app

bash
Copy
Edit
python app.py
Visit the app
Open your browser at: http://127.0.0.1:5000

🧪 How to Use
Fill out the patient’s form on the homepage.

Select your location and relevant conditions/medications.

Click Find Matching Trials.

Review the trial cards, each showing a match score and eligibility info.

Click Contact Trial Coordinator for general contact guidance.

🧩 Future Improvements
BERT/NER for more accurate NLP parsing.

Move from trials.json to SQL/PostgreSQL.

Add user login and patient profile saving.

Advanced trial filters (e.g., by trial phase).

Admin panel for trial data upload.

Real contact integration (if permissible).

Full testing suite and production-level logging.

📄 License
This project is licensed under the
