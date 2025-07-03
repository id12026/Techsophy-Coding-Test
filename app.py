from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

app = Flask(__name__)

# Load expanded clinical trials data for India
with open('trials.json') as f:
    trials_data = json.load(f)

# List of common diseases in India
INDIAN_DISEASES = [
    "Diabetes", "Hypertension", "Coronary Artery Disease", "Chronic Obstructive Pulmonary Disease",
    "Tuberculosis", "Asthma", "Dengue", "Malaria", "Chikungunya", "Typhoid",
    "Hepatitis B", "Hepatitis C", "HIV/AIDS", "Cancer", "Breast Cancer", "Lung Cancer",
    "Oral Cancer", "Cervical Cancer", "Colorectal Cancer", "Leukemia", "Lymphoma",
    "Thyroid Disorders", "Osteoarthritis", "Rheumatoid Arthritis", "Osteoporosis",
    "Chronic Kidney Disease", "Alzheimer's Disease", "Parkinson's Disease",
    "Epilepsy", "Stroke", "Psoriasis", "Eczema", "Acne", "Vitiligo",
    "Irritable Bowel Syndrome", "Ulcerative Colitis", "Crohn's Disease",
    "Peptic Ulcer Disease", "Gastroesophageal Reflux Disease", "Gallstones",
    "Cirrhosis", "Pancreatitis", "Anemia", "Thalassemia", "Sickle Cell Anemia",
    "Glaucoma", "Cataract", "Diabetic Retinopathy", "Macular Degeneration",
    "Otitis Media", "Sinusitis", "Allergic Rhinitis", "Migraine", "Tension Headache",
    "Depression", "Anxiety Disorders", "Bipolar Disorder", "Schizophrenia",
    "Obsessive-Compulsive Disorder", "Autism Spectrum Disorder", "ADHD"
]

# Indian cities and states
INDIAN_LOCATIONS = [
    "Mumbai, Maharashtra", "Delhi", "Bangalore, Karnataka", "Hyderabad, Telangana",
    "Chennai, Tamil Nadu", "Kolkata, West Bengal", "Pune, Maharashtra", 
    "Ahmedabad, Gujarat", "Jaipur, Rajasthan", "Surat, Gujarat",
    "Lucknow, Uttar Pradesh", "Kanpur, Uttar Pradesh", "Nagpur, Maharashtra",
    "Patna, Bihar", "Indore, Madhya Pradesh", "Thane, Maharashtra",
    "Bhopal, Madhya Pradesh", "Visakhapatnam, Andhra Pradesh", "Vadodara, Gujarat",
    "Firozabad, Uttar Pradesh", "Ludhiana, Punjab", "Rajkot, Gujarat",
    "Agra, Uttar Pradesh", "Siliguri, West Bengal", "Nashik, Maharashtra",
    "Faridabad, Haryana", "Patiala, Punjab", "Meerut, Uttar Pradesh",
    "Kalyan-Dombivli, Maharashtra", "Vasai-Virar, Maharashtra", "Varanasi, Uttar Pradesh",
    "Srinagar, Jammu and Kashmir", "Dhanbad, Jharkhand", "Jodhpur, Rajasthan",
    "Amritsar, Punjab", "Raipur, Chhattisgarh", "Allahabad, Uttar Pradesh",
    "Coimbatore, Tamil Nadu", "Jabalpur, Madhya Pradesh", "Gwalior, Madhya Pradesh",
    "Vijayawada, Andhra Pradesh", "Madurai, Tamil Nadu", "Guwahati, Assam",
    "Chandigarh", "Hubli-Dharwad, Karnataka", "Amroha, Uttar Pradesh",
    "Moradabad, Uttar Pradesh", "Gurgaon, Haryana", "Noida, Uttar Pradesh"
]

@dataclass
class Patient:
    """Class to represent patient demographic and medical information"""
    patient_id: str
    age: int
    gender: str
    conditions: List[str]
    medications: List[str]
    allergies: List[str]
    lab_results: Dict[str, float]
    procedures: List[str]
    location: str
    last_visit: str

@dataclass
class ClinicalTrial:
    """Class to represent clinical trial eligibility criteria"""
    trial_id: str
    title: str
    description: str
    inclusion_criteria: Dict[str, str]
    exclusion_criteria: Dict[str, str]
    locations: List[str]
    phase: str
    therapeutic_area: str

class CriteriaParser:
    """Enhanced criteria parser with support for Indian medical terminology"""
    
    @staticmethod
    def parse_numerical_criteria(criteria: str) -> Tuple[Optional[float], Optional[float]]:
        patterns = [
            r'between\s+(\d+)\s+and\s+(\d+)',
            r'(\d+)\s*-\s*(\d+)',
            r'>=?\s*(\d+)',
            r'<=?\s*(\d+)',
            r'==?\s*(\d+)',
            r'(\d+)\s*to\s*(\d+)'  
        ]
        
        for pattern in patterns:
            matches = re.search(pattern, criteria, re.IGNORECASE)
            if matches:
                if 'between' in pattern or '-' in pattern or 'to' in pattern:
                    return float(matches.group(1)), float(matches.group(2))
                elif '>=' in criteria:
                    return float(matches.group(1)), None
                elif '<=' in criteria:
                    return None, float(matches.group(1))
                elif '>' in criteria:
                    return float(matches.group(1)) + 0.01, None 
                elif '<' in criteria:
                    return None, float(matches.group(1)) - 0.01 
                elif '=' in criteria:
                    val = float(matches.group(1))
                    return val, val
        
        return None, None
    
    @staticmethod
    def parse_list_criteria(criteria: str) -> List[str]:
        # Handle Indian English variations
        criteria = criteria.replace('viz.', '').replace('i.e.', '')
        items = re.split(r',|;| or | and |/', criteria)
        items = [item.strip().lower() for item in items if item.strip()]
        return items

class PatientTrialMatcher:
    """Enhanced matcher for Indian healthcare context"""
    
    def __init__(self, trials: List[ClinicalTrial]):
        self.trials = trials
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self._build_trial_vectors()
    
    def _build_trial_vectors(self):
        """Preprocess trial data for similarity matching"""
        trial_texts = [
            f"{trial.title} {trial.description} {trial.therapeutic_area} "
            f"{' '.join(trial.inclusion_criteria.values())}"
            for trial in self.trials
        ]
        self.trial_vectors = self.vectorizer.fit_transform(trial_texts)
    
    def _calculate_semantic_similarity(self, patient: Patient, trial: ClinicalTrial) -> float:
        """Calculate text similarity between patient conditions and trial description"""
        patient_text = ' '.join(patient.conditions + patient.medications)
        if not patient_text.strip():
            return 0.0
        patient_vector = self.vectorizer.transform([patient_text])
        try:
            trial_idx = next(i for i, t in enumerate(self.trials) if t.trial_id == trial.trial_id)
        except StopIteration:
            return 0.0 

        trial_vector = self.trial_vectors[trial_idx]
        return cosine_similarity(patient_vector, trial_vector)[0][0]
    
    def _check_numerical_criteria(self, patient_value: float, criteria: str) -> bool:
        if patient_value is None: 
            return True 
        min_val, max_val = CriteriaParser.parse_numerical_criteria(criteria)
        if min_val is not None and patient_value < min_val:
            return False
        if max_val is not None and patient_value > max_val:
            return False
        return True
    
    def _check_list_criteria(self, patient_values: List[str], criteria: str, is_exclusion: bool = False) -> bool:
        required_items = CriteriaParser.parse_list_criteria(criteria)
        if not required_items:
            return True 
        
        patient_values_lower = [pv.lower() for pv in patient_values]

        if is_exclusion:
            return not any(item in patient_values_lower for item in required_items)
        else:
            return any(item in patient_values_lower for item in required_items)
    
    def _check_location(self, patient: Patient, trial: ClinicalTrial) -> bool:
        if not trial.locations or 'any' in [loc.lower() for loc in trial.locations]:
            return True
        patient_loc_lower = patient.location.lower()
        return any(patient_loc_lower in loc.lower() or loc.lower() in patient_loc_lower
                   for loc in trial.locations)
    
    def _check_recency(self, patient: Patient, trial: ClinicalTrial) -> bool:
        recency_period_days = 365

        try:
            last_visit = datetime.strptime(patient.last_visit, '%Y-%m-%d')
            recency_threshold = datetime.now() - timedelta(days=recency_period_days)
            return last_visit >= recency_threshold
        except ValueError:
            return False
    
    def calculate_match_score(self, patient: Patient, trial: ClinicalTrial) -> float:
        score = 0.0
        
        if 'age' in trial.inclusion_criteria:
            if not self._check_numerical_criteria(patient.age, trial.inclusion_criteria['age']):
                return 0.0
        if 'gender' in trial.inclusion_criteria:
            trial_gender = trial.inclusion_criteria['gender'].lower()
            if trial_gender not in ['any', 'both', 'male or female', 'male/female']:
                if patient.gender.lower() != trial_gender:
                    return 0.0
        if not self._check_location(patient, trial):
            return 0.0
        
        if not self._check_recency(patient, trial):
            return 0.0
        condition_match_weight = 0.4
        if 'conditions' in trial.inclusion_criteria:
            if not self._check_list_criteria([c.lower() for c in patient.conditions],
                                             trial.inclusion_criteria['conditions'],
                                             is_exclusion=False):
                pass 
            else:
                score += condition_match_weight
        medication_inclusion_weight = 0.15
        if 'medications' in trial.inclusion_criteria:
            if self._check_list_criteria([m.lower() for m in patient.medications],
                                         trial.inclusion_criteria['medications'],
                                         is_exclusion=False):
                score += medication_inclusion_weight
        
        # Lab results 
        lab_inclusion_weight_per_test = 0.1
        for lab_key, criteria_str in trial.inclusion_criteria.items():
            if lab_key in patient.lab_results and lab_key not in ['age', 'gender', 'conditions', 'medications']:
                if not self._check_numerical_criteria(patient.lab_results[lab_key], criteria_str):
                    return 0.0 
                else:
                    score += lab_inclusion_weight_per_test 
        
   
        if 'conditions' in trial.exclusion_criteria:
            if not self._check_list_criteria([c.lower() for c in patient.conditions],
                                             trial.exclusion_criteria['conditions'],
                                             is_exclusion=True):
                return 0.0 
        if 'medications' in trial.exclusion_criteria:
            if not self._check_list_criteria([m.lower() for m in patient.medications],
                                             trial.exclusion_criteria['medications'],
                                             is_exclusion=True):
                return 0.0 
        for lab_key, criteria_str in trial.exclusion_criteria.items():
            if lab_key in patient.lab_results and lab_key not in ['age', 'gender', 'conditions', 'medications']:
                if not self._check_numerical_criteria(patient.lab_results[lab_key], criteria_str):
                    return 0.0 
        semantic_sim = self._calculate_semantic_similarity(patient, trial)
        score += 0.35 * semantic_sim 
        return min(score, 1.0)
    
    def get_trial_recommendations(self, patient: Patient, top_n: int = 5) -> List[Tuple[ClinicalTrial, float]]:
        scored_trials = []
        
        for trial in self.trials:
            score = self.calculate_match_score(patient, trial)
            if score > 0: 
                scored_trials.append((trial, score))
        
        scored_trials.sort(key=lambda x: x[1], reverse=True)
        return scored_trials[:top_n]

# Initialize trials
trials = [
    ClinicalTrial(
        trial_id=trial['trial_id'],
        title=trial['title'],
        description=trial['description'],
        inclusion_criteria=trial['inclusion_criteria'],
        exclusion_criteria=trial['exclusion_criteria'],
        locations=trial['locations'],
        phase=trial['phase'],
        therapeutic_area=trial['therapeutic_area']
    )
    for trial in trials_data
]

matcher = PatientTrialMatcher(trials)

@app.route('/')
def index():
    return render_template('index.html', 
                           locations=INDIAN_LOCATIONS,
                           diseases=INDIAN_DISEASES)

@app.route('/match', methods=['POST'])
def match_patient():
    try:
        # Parse form data
        patient_data = {
            'patient_id': 'PAT' + str(datetime.now().timestamp()).replace('.', '')[-6:],
            'age': int(request.form['age']),
            'gender': request.form['gender'],
            'conditions': [c.strip() for c in request.form['conditions'].split(',') if c.strip()],
            'medications': [m.strip() for m in request.form['medications'].split(',') if m.strip()],
            'allergies': [a.strip() for a in request.form['allergies'].split(',') if a.strip()],
            'lab_results': {
                'hba1c': float(request.form.get('hba1c')) if request.form.get('hba1c') else None,
                'systolic_bp': float(request.form.get('systolic_bp')) if request.form.get('systolic_bp') else None,
                'bmi': float(request.form.get('bmi')) if request.form.get('bmi') else None,
                'creatinine': float(request.form.get('creatinine')) if request.form.get('creatinine') else None
            },
            'procedures': [], 
            'location': request.form['location'],
            'last_visit': datetime.now().strftime('%Y-%m-%d') 
        }
        
        patient_data['lab_results'] = {k: v for k, v in patient_data['lab_results'].items() if v is not None}
        patient = Patient(**patient_data)
        
        # Getting recommendations
        recommendations = matcher.get_trial_recommendations(patient)
        
        # Preparing the results
        results = []
        for trial, score in recommendations:
            results.append({
                'trial_id': trial.trial_id,
                'title': trial.title,
                'score': round(score * 100),
                'phase': trial.phase,
                'locations': trial.locations,
                'description': trial.description,
                'inclusion_criteria': trial.inclusion_criteria,
                'exclusion_criteria': trial.exclusion_criteria
            })
        
        return render_template('results.html', 
                               patient=patient_data, 
                               results=results,
                               diseases=INDIAN_DISEASES) 
    
    except Exception as e:
        # Logging the error for debugging
        app.logger.error(f"Error during patient matching: {e}")
        return jsonify({'error': 'An error occurred during matching. Please check your input and try again.'}), 400

if __name__ == '__main__':
    app.run(debug=True)