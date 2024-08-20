from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
import joblib
import numpy as np

# Load the trained model
model = joblib.load('health_assistant/ML/health_model.pkl')

def index(request):
    if request.method == 'POST':
        # Get symptoms from the form
        fever = int(request.POST.get('fever', 0))
        cough = int(request.POST.get('cough', 0))
        fatigue = int(request.POST.get('fatigue', 0))
        runny_nose = int(request.POST.get('runny_nose', 0))
        sneezing = int(request.POST.get('sneezing', 0))
        itchy_eyes = int(request.POST.get('itchy_eyes', 0))
        headache = int(request.POST.get('headache', 0))

        # Prepare the input data
        input_data = np.array([[fever, cough, fatigue, runny_nose, sneezing, itchy_eyes, headache]])

        # Predict health condition
        prediction = model.predict(input_data)
        condition_mapping = {0: 'Flu', 1: 'Allergy', 2: 'Cold'}
        predicted_condition = condition_mapping[prediction[0]]

        return HttpResponse(f"Predicted Condition: {predicted_condition}")

    return render(request, 'health_assistant/index.html')
