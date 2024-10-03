from django.shortcuts import render, redirect
from django.http import HttpResponse
import joblib
import numpy as np
from django.contrib import messages
from .forms import UserRegisterForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout 
from .models import Patient
from .nlp_utils import speech_to_text, extract_symptoms, predict_disease


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



def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user form first
            user = user_form.save()
            # Link the profile form to the user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            messages.success(request, 'Account created successfully!')
            auth_login(request, user)  # Log the user in after registration
            return redirect('index')  # Redirect to a home or dashboard page
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    return render(request, 'health_assistant/register.html', {'user_form': user_form, 'profile_form': profile_form})


def profile_view(request):
    if request.user.is_authenticated:
        # Get the user and their profile if logged in
        user = request.user
        profile = user.profile  # Assuming a OneToOne relationship with User
        return render(request, 'health_assistant/profile.html', {'user': user, 'profile': profile})
    else:
        # Handle unauthenticated users by redirecting or showing a different message
        messages.error(request, "You need to be logged in to view your profile.")
        return redirect('login')


def edit_profile(request):
    return redirect('profile')
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')  # Redirect to a home page or dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'health_assistant/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect to login page after logout



def all_patients_view(request):
   
    # Get all patients from the database
    patients = Patient.objects.all()
    
    # Render the patient list for the doctor
    return render(request, 'health_assistant/all_patient.html', {'patients': patients})

def diagnose(request):
    result = None  # Variable to store the diagnosis result
    error_message = None  # Variable to store any error message

    if request.method == 'POST':
        # Get patient name from form, if available, or use "Guest" for anonymous users
        patient_name = request.POST.get('name', 'Guest')

        # Get the voice input and process it
        speech_text = speech_to_text()  # This function will handle audio input from the microphone
        if speech_text:
            # Extract symptoms from the spoken text and predict diseases
            symptoms = extract_symptoms(speech_text)
            predicted_diseases = predict_disease(symptoms)

            # Convert predicted diseases to a comma-separated string
            predicted_disease_str = ', '.join(predicted_diseases)

            # Only save the diagnosis to the database if the user is authenticated
            if request.user.is_authenticated:
                patient = Patient.objects.create(
                    user=request.user,
                    name=patient_name,
                    symptoms=speech_text,
                    predicted_disease=predicted_disease_str
                )

            # Store the diagnosis result to display on the same page
            result = predicted_disease_str
        else:
            # If the speech input fails, show an error message
            error_message = 'Unable to process audio input'

    # Render the diagnosis form and result
    return render(request, 'health_assistant/diagnose.html', {'result': result, 'error_message': error_message})


def result(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    return render(request, 'health_assistant/result.html', {'patient': patient})
