import joblib
import numpy as np

# Load the model
model = joblib.load('health_model.pkl')

# Example new symptom data (fever, cough, fatigue, no runny nose, no sneezing, no itchy eyes, headache)
new_symptoms = np.array([[1, 1, 1, 0, 0, 0, 1]])

# Predict the health condition
predicted_condition = model.predict(new_symptoms)

# Convert numerical prediction back to categorical label
condition_mapping = {0: 'Flu', 1: 'Allergy', 2: 'Cold'}
print(f"Predicted Condition: {condition_mapping[predicted_condition[0]]}")
