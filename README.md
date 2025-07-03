# Techsophy-Coding-Test

```markdown
# Clinical Trial Patient Matching System 

## Overview

This project implements a web-based Clinical Trial Patient Matching System designed to help patients in India find suitable clinical trials based on their demographic and medical profiles. The system employs AI/ML techniques, including TF-IDF for semantic similarity and a criteria-based scoring engine, to provide ranked recommendations.

The application is built with Flask for the backend and standard web technologies (HTML, CSS, JavaScript) for the frontend.

## Features

* **Patient Profile Input:** Collects essential patient information including age, gender, location, medical conditions, medications, allergies, and key lab results.
* **Location-Aware Matching:** Utilizes a predefined list of Indian cities and states for location-based trial filtering.
* **Disease-Specific Suggestions:** Provides quick-add tags for common Indian diseases to streamline patient input.
* **Dynamic Eligibility Assessment:** Evaluates inclusion and exclusion criteria (numerical ranges, specific conditions/medications) against patient data.
* **Semantic Similarity Matching:** Uses TF-IDF and Cosine Similarity to find trials semantically related to the patient's conditions and medications, even if exact keyword matches are not present.
* **Weighted Scoring & Ranking:** Assigns a match score to each trial based on satisfied criteria and semantic relevance, then ranks trials by this score.
* **Clear Results Display:** Presents matched trials with their scores, detailed descriptions, and explicit inclusion/exclusion criteria.
* **Contact Mechanism (Placeholder):** A "Contact Trial Coordinator" button provides generic contact information via a modal popup.

## Technical Skills Demonstrated

* **AI/ML:** TF-IDF Vectorization, Cosine Similarity for semantic matching, rule-based scoring algorithms.
* **Critical Thinking:** Design of complex eligibility logic, handling of inclusion/exclusion rules.
* **Problem Solving:** Parsing natural language criteria, managing multiple data points for matching.
* **Modular Architecture:** Separation of concerns into `CriteriaParser`, `PatientTrialMatcher` classes, and distinct Flask routes/templates.
* **Web Development:** Flask (Python), HTML, CSS, JavaScript for a functional user interface.
* **Data Handling:** JSON for storing clinical trial data.

## Project Structure

```

clinical-trial-matcher/
├── app.py                     \# Flask application logic, matching engine
├── trials.json                \# Sample clinical trial data (Indian context)
├── static/
│   ├── style.css              \# Frontend styling
│   └── script.js              \# Frontend JavaScript for form and modal
└── templates/
├── index.html             \# Patient input form
└── results.html           \# Display of matching results and contact modal

````

## Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repo-url>
    cd clinical-trial-matcher
    ```
    (If you received the code as files, just navigate to the `clinical-trial-matcher` directory.)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    * On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required Python packages:**
    ```bash
    pip install Flask scikit-learn
    ```

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```

6.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

1.  **Fill out the Patient Form:** On the homepage, enter the patient's demographic information, medical conditions, current medications, allergies, and optional lab results.
2.  **Select Location:** Choose an Indian city/state from the dropdown.
3.  **Click "Find Matching Trials":** The system will process the input and display a list of recommended clinical trials.
4.  **Review Results:** Each matching trial shows its match score, details, description, and specific inclusion/exclusion criteria.
5.  **Contact Coordinator:** Click the "Contact Trial Coordinator" button on any trial card to see generic contact information in a popup.

## Future Enhancements

* **More Sophisticated NLP:** Implement more advanced NLP (e.g., named entity recognition, BERT embeddings) for better understanding of medical text and more nuanced semantic matching.
* **Database Integration:** Replace `trials.json` with a proper database (e.g., SQLite, PostgreSQL) for scalable data management.
* **User Accounts & Profiles:** Allow users to create accounts, save patient profiles, and track trial applications.
* **Trial Search Filters:** Add more filtering options for trials (e.g., by phase, therapeutic area).
* **Admin Interface:** A backend interface for managing and adding new clinical trial data.
* **Real Contact Information:** Integrate actual contact details for trials (if available and permissible).
* **Robust Error Handling:** More detailed error messages and logging for production environments.
* **Unit and Integration Tests:** Comprehensive testing to ensure accuracy and reliability of the matching logic.

## License

This project is open-source and available under the [MIT License](LICENSE). (You would typically create a `LICENSE` file in the root directory if you want to explicitly define this).
````
