# Simple accuracy test
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Quick data generation
np.random.seed(42)

# 1000 samples: 700 healthy, 300 PCOS
healthy_data = np.random.normal([28, 23, 12, 35, 6, 7, 90, 180], [6, 3, 4, 10, 2, 2, 10, 30], (700, 8))
pcos_data = np.random.normal([26, 28, 18, 55, 12, 6, 105, 200], [5, 5, 6, 15, 4, 2, 15, 40], (300, 8))

X = np.vstack([healthy_data, pcos_data])
y = np.hstack([np.zeros(700), np.ones(300)])

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Test both models
models = {
    'Logistic Regression': LogisticRegression(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100)
}

results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    predictions = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, predictions)
    results[name] = accuracy
    print(f"{name}: {accuracy:.4f} ({accuracy*100:.2f}%)")

# Find best model
best_model_name = max(results, key=results.get)
best_accuracy = results[best_model_name]

print(f"\nBest Model: {best_model_name}")
print(f"Best Accuracy: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")

# Save best model
best_model = models[best_model_name]
import joblib
joblib.dump(best_model, "pcos_model.pkl")
joblib.dump(scaler, "pcos_scaler.pkl")
joblib.dump(['Age', 'BMI', 'Insulin', 'Testosterone', 'LH', 'FSH', 'Glucose', 'Cholesterol'], "feature_names.pkl")

print("Model saved successfully!")
