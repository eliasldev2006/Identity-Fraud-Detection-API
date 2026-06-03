import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. load dataset
data = pd.read_csv('dataset.csv')
if not os.path.exists('models'):
    raise FileNotFoundError("The 'models' directory does not exist. Please create it before running the script.")
print("Loading dataset...")
df = pd.read_csv('dataset.csv')

# 2. Split features (X) and target (y)
print("Splitting features and target...")
X = df.drop('target', axis=1)
y = df['target']

# 3. Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training the Random Forest model")

# 4. Initialize and train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n=== Model Evaluation ===")
print(f"Accuracy Score: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 6. save the trained model to 'models' directory   
os.makedirs('models', exist_ok=True)
model_output_path = "models\fraud_detector_model.pkl"
joblib.dump(model, model_output_path)
print(f"\nModel successfully saved to '{model_output_path}'!")