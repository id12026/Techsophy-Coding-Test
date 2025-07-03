## 🏥Clinical Trial Patient Matching System

## Overview

This tool helps patients to find suitable clinical trials based on their medical and demographic profiles. The system utilizes AI/ML techniques, including TF-IDF and cosine similarity, to rank and recommend clinical trials with relevance scoring.

## Problem Statement: 

Build a tool that matches patients to relevant clinical trials based on eligibility criteria.

## Key Features

- **Patient Profile Input**: Collects age, gender, city, medical conditions, medications, allergies, and lab results.
  
- **Location-Aware Filtering**: Filters trials by Indian cities/states.
  
- **Disease-Specific Shortcuts**: Quick-tag options for common diseases.
  
- **Eligibility Matching**: Dynamically checks inclusion/exclusion criteria.
  
- **Semantic Matching**: Uses TF-IDF + cosine similarity to find relevant trials, accommodating varied terminology.
  
- **Weighted Scoring**: Trials are ranked based on rule-based and semantic relevance.
  
- **Results with Contact Info**: Displays trial details with a generic contact option (modal popup).

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
  
- **Backend**: Flask (Python)
  
- **ML/NLP**: Scikit-learn (TF-IDF, Cosine Similarity)
  
- **Data**: JSON 

## Project Structure

```plaintext
clinical-trial-matcher/
├── app.py                 # Main Flask app and logic
├── trials.json            # Sample trial data (India-specific)
├── static/
│   ├── style.css          # Custom styling
│   └── script.js          # Form interaction and modal logic
└── templates/
    ├── index.html         # Home form page
    └── results.html       # Matched trials display
```

## Installation

1. **Clone this repo**:

   ```bash
   git clone https://github.com/id12026/Techsophy-Coding-Test.git
   cd Techsophy
   ```

2. **Set up virtual environment (recommended)**:

   ```bash
   python -m venv venv
   ```

3. **Activate environment**:

   - **Windows**:

     ```bash
     .\venv\Scripts\activate
     ```

   - **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:

   ```bash
   pip install Flask scikit-learn
   ```

5. **Run the app**:

   ```bash
   python app.py
   ```

6. **Visit the app**: Open your browser at: [http://127.0.0.1:5000](http://127.0.0.1:5000)


## Screenshots: 
![WhatsApp Image 2025-07-03 at 12 28 49_e5a7a840](https://github.com/user-attachments/assets/9906fecd-a42a-46e3-a06f-7685bd25f7f7)

![WhatsApp Image 2025-07-03 at 12 29 07_f80eb11b](https://github.com/user-attachments/assets/8dc2a147-b27d-4046-a363-336559bc952a)

![WhatsApp Image 2025-07-03 at 12 29 31_2cfebfc1](https://github.com/user-attachments/assets/1299f89e-24be-4afb-9d57-c8b937f26f08)

![WhatsApp Image 2025-07-03 at 12 29 51_56a7694d](https://github.com/user-attachments/assets/3a6a7823-d855-493e-9730-0663b638c7a5)

![WhatsApp Image 2025-07-03 at 12 33 30_835c15ed](https://github.com/user-attachments/assets/70c21ee3-08df-4de5-8804-9a9f6b970cec)

![WhatsApp Image 2025-07-03 at 12 33 48_376c9da3](https://github.com/user-attachments/assets/9b3a0eac-6c00-4aea-9fb4-74018eb7e7b8)



## How to Use

- Fill out the patient’s form on the homepage.
  
- Select your location and relevant conditions/medications.
  
- Click **Find Matching Trials**.
  
- Review the trial cards, each showing a match score and eligibility info.
  
- Click **Contact Trial Coordinator** for general contact guidance.

## Future Improvements

- Implement BERT/NER for more accurate NLP parsing.
  
- Transition from `trials.json` to SQL.
  
- Add user login and patient profile saving.
  
- Introduce advanced trial filters (e.g., by trial phase).
  
- Create an admin panel for trial data upload.
  
- Integrate real contact options (if permissible).
  
- Develop a full testing suite and production-level logging.

## License

This project is licensed under the Apache License.

## BY

## Name: Mohitha Bandi
## Student ID: 22WU0105037
## B.Tech: C.S.E - Data Science
## E-mail: mohitha.bandi_2026@woxsen.edu.in
