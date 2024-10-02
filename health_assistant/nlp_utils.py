import speech_recognition as sr
import spacy

# Load the general spaCy model for symptom extraction
nlp = spacy.load("en_core_web_md")  # Using general spaCy model instead of scispaCy

# Define a set of keywords related to symptoms
symptom_keywords = {
    'cough', 'fever', 'headache', 'nausea', 'fatigue', 'pain', 'dizziness',
    'sore throat', 'shortness of breath', 'chest pain', 'abdominal pain',
    'vomiting', 'diarrhea', 'muscle ache', 'joint pain', 'rash', 'swelling',
    'chills', 'sweating', 'loss of appetite', 'weight loss', 'anxiety',
    'depression', 'insomnia', 'palpitations', 'constipation', 'blurry vision',
    'hearing loss', 'itching', 'bleeding', 'numbness', 'tingling', 'weakness'
}
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for symptoms...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None

def extract_symptoms(text):
    doc = nlp(text)
    # Use keyword matching to extract symptoms
    symptoms = [token.text for token in doc if token.lemma_.lower() in symptom_keywords]

    return symptoms


# Symptom-to-disease mapping
disease_map = {
    'cough': ['Cold', 'Bronchitis', 'Pneumonia'],
    'fever': ['Flu', 'Malaria', 'COVID-19'],
    'headache': ['Migraine', 'Tension Headache', 'Sinusitis'],
    'nausea': ['Food Poisoning', 'Gastritis', 'Pregnancy'],
    'fatigue': ['Anemia', 'Hypothyroidism', 'Chronic Fatigue Syndrome'],
    'pain': ['Fibromyalgia', 'Arthritis', 'Injury'],
    'dizziness': ['Vertigo', 'Low Blood Pressure', 'Dehydration'],
    'sore throat': ['Tonsillitis', 'Strep Throat', 'Common Cold'],
    'shortness of breath': ['Asthma', 'Heart Failure', 'Pneumonia'],
    'chest pain': ['Heart Attack', 'Angina', 'Panic Attack'],
    'abdominal pain': ['Appendicitis', 'Irritable Bowel Syndrome', 'Gastritis'],
    'vomiting': ['Gastroenteritis', 'Food Poisoning', 'Pregnancy'],
    'diarrhea': ['Gastroenteritis', 'Irritable Bowel Syndrome', 'Food Poisoning'],
    'muscle ache': ['Influenza', 'Fibromyalgia', 'Muscle Injury'],
    'joint pain': ['Arthritis', 'Lupus', 'Gout'],
    'rash': ['Allergic Reaction', 'Eczema', 'Psoriasis'],
    'swelling': ['Edema', 'Injury', 'Lymph Node Infection'],
    'chills': ['Flu', 'Malaria', 'Infection'],
    'sweating': ['Hyperthyroidism', 'Menopause', 'Infection'],
    'loss of appetite': ['Depression', 'Anorexia', 'Infection'],
    'weight loss': ['Cancer', 'Hyperthyroidism', 'Diabetes'],
    'anxiety': ['Generalized Anxiety Disorder', 'Panic Disorder', 'Stress'],
    'depression': ['Major Depressive Disorder', 'Bipolar Disorder', 'Chronic Illness'],
    'insomnia': ['Stress', 'Anxiety', 'Depression'],
    'palpitations': ['Arrhythmia', 'Anxiety', 'Hyperthyroidism'],
    'constipation': ['Irritable Bowel Syndrome', 'Hypothyroidism', 'Dehydration'],
    'blurry vision': ['Diabetes', 'Cataracts', 'Glaucoma'],
    'hearing loss': ['Ear Infection', 'Aging', 'Noise Exposure'],
    'itching': ['Allergic Reaction', 'Eczema', 'Scabies'],
    'bleeding': ['Injury', 'Hemophilia', 'Gastric Ulcer'],
    'numbness': ['Diabetes', 'Multiple Sclerosis', 'Nerve Compression'],
    'tingling': ['Carpal Tunnel Syndrome', 'Diabetes', 'Vitamin Deficiency'],
    'weakness': ['Anemia', 'Muscle Strain', 'Stroke']
}


def predict_disease(symptoms):
    predicted_diseases = set()

    for symptom in symptoms:
        diseases = disease_map.get(symptom.lower(), ["Unknown"])  # Default to ["Unknown"] if not found
        
        # Add all diseases to the set
        for disease in diseases:
            if disease != "Unknown":
                predicted_diseases.add(disease)

    return list(predicted_diseases)


# Example usage
if __name__ == "__main__":
    spoken_text = speech_to_text()
    if spoken_text:
        print("You said:", spoken_text)
        symptoms = extract_symptoms(spoken_text)
        print("Extracted Symptoms:", symptoms)
        predicted_diseases = predict_disease(symptoms)
        print("Predicted Diseases:", predicted_diseases)
    else:
        print("Sorry, I couldn't understand you.")
