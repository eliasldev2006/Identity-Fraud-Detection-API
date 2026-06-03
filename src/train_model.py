import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. Load dataset
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataset_path = os.path.join(base_dir, "data", "training_records.csv")
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"Dataset not found at {dataset_path}. Please run data_generator.py first.")

print(f"Loading dataset from: {dataset_path}")
df = pd.read_csv(dataset_path)

# 2. Split features (X) and target (y)
print("Splitting features and target...")
X = df.drop('target', axis=1)
y = df['target']

# 3. Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training the Random Forest model...")

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

# 6. Save the trained model to 'models' directory   
os.makedirs('models', exist_ok=True)
model_output_path = os.path.join("models", "fraud_detector_model.pkl")
joblib.dump(model, model_output_path)
print(f"\nModel successfully saved to '{model_output_path}'!")