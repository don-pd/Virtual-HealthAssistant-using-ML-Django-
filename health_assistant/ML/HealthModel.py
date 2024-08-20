import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

# Example dataset
data = {
    'Fever': [1, 0, 1, 0, 1],
    'Cough': [1, 0, 1, 0, 0],
    'Fatigue': [1, 0, 0, 0, 1],
    'Runny Nose': [0, 1, 0, 1, 0],
    'Sneezing': [0, 1, 0, 1, 0],
    'Itchy Eyes': [0, 1, 0, 1, 0],
    'Headache': [1, 0, 1, 0, 1],
    'Condition': ['Flu', 'Allergy', 'Cold', 'Allergy', 'Flu']
}

# Create DataFrame
df = pd.DataFrame(data)

# Convert categorical labels to numerical values
df['Condition'] = df['Condition'].map({'Flu': 0, 'Allergy': 1, 'Cold': 2})

# Split the data into features (X) and labels (y)
X = df.drop('Condition', axis=1)
y = df['Condition']

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the trained model
joblib.dump(model, 'C:/Users/neo/Desktop/VirtualHealth/health_model.pkl')

