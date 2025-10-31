import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib

print("🎯 PCOS Model Accuracy Calculator")
print("=" * 40)

# Generate synthetic PCOS data
np.random.seed(42)
n_samples = 1000

# Create realistic PCOS vs Healthy data
print("📊 Creating dataset...")

# Healthy patients (70%)
n_healthy = 700
healthy_features = np.column_stack([
    np.random.normal(28, 6, n_healthy),      # Age
    np.random.normal(23, 3, n_healthy),      # BMI (normal)
    np.random.normal(12, 4, n_healthy),      # Insulin (normal)
    np.random.normal(35, 10, n_healthy),     # Testosterone (normal)
    np.random.normal(6, 2, n_healthy),       # LH (normal)
    np.random.normal(7, 2, n_healthy),       # FSH (normal)
    np.random.normal(90, 10, n_healthy),     # Glucose (normal)
    np.random.normal(180, 30, n_healthy),    # Cholesterol (normal)
])
healthy_labels = np.zeros(n_healthy)

# PCOS patients (30%)
n_pcos = 300
pcos_features = np.column_stack([
    np.random.normal(26, 5, n_pcos),         # Age
    np.random.normal(28, 5, n_pcos),         # BMI (higher)
    np.random.normal(18, 6, n_pcos),         # Insulin (elevated)
    np.random.normal(55, 15, n_pcos),        # Testosterone (elevated)
    np.random.normal(12, 4, n_pcos),         # LH (elevated)
    np.random.normal(6, 2, n_pcos),          # FSH
    np.random.normal(105, 15, n_pcos),       # Glucose (higher)
    np.random.normal(200, 40, n_pcos),       # Cholesterol (higher)
])
pcos_labels = np.ones(n_pcos)

# Combine data
X = np.vstack([healthy_features, pcos_features])
y = np.concatenate([healthy_labels, pcos_labels])

print(f"✅ Dataset created: {len(X)} samples")
print(f"   Healthy: {len(healthy_labels)} patients")
print(f"   PCOS: {len(pcos_labels)} patients")

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📚 Training set: {len(X_train)} samples")
print(f"🧪 Test set: {len(X_test)} samples")

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n🔄 Training models...")

# Train Logistic Regression
lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train_scaled, y_train)
lr_predictions = lr_model.predict(X_test_scaled)
lr_accuracy = accuracy_score(y_test, lr_predictions)

print(f"\n📈 Logistic Regression:")
print(f"   Accuracy: {lr_accuracy:.4f} ({lr_accuracy*100:.2f}%)")

# Train Random Forest
rf_model = RandomForestClassifier(random_state=42, n_estimators=100)
rf_model.fit(X_train_scaled, y_train)
rf_predictions = rf_model.predict(X_test_scaled)
rf_accuracy = accuracy_score(y_test, rf_predictions)

print(f"\n🌳 Random Forest:")
print(f"   Accuracy: {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")

# Choose the best model
if rf_accuracy > lr_accuracy:
    best_model = rf_model
    best_name = "Random Forest"
    best_accuracy = rf_accuracy
else:
    best_model = lr_model
    best_name = "Logistic Regression"
    best_accuracy = lr_accuracy

print(f"\n🏆 BEST MODEL: {best_name}")
print(f"🎯 FINAL ACCURACY: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")

# Save the best model
feature_names = ['Age', 'BMI', 'Insulin', 'Testosterone', 'LH', 'FSH', 'Glucose', 'Cholesterol']
joblib.dump(best_model, "pcos_model.pkl")
joblib.dump(scaler, "pcos_scaler.pkl")
joblib.dump(feature_names, "feature_names.pkl")

print(f"\n💾 Model saved!")

# Test with sample cases
print(f"\n🧪 Testing with sample patients:")

test_cases = [
    ("Healthy Patient", [25, 21, 8, 25, 4, 8, 80, 160]),
    ("PCOS Patient", [30, 32, 25, 70, 18, 5, 120, 240])
]

for case_name, values in test_cases:
    sample = np.array([values])
    sample_scaled = scaler.transform(sample)
    prediction = best_model.predict(sample_scaled)[0]
    probability = best_model.predict_proba(sample_scaled)[0]
    
    result = "PCOS" if prediction == 1 else "Healthy"
    confidence = probability[1] if prediction == 1 else probability[0]
    
    print(f"   {case_name}: {result} ({confidence*100:.1f}% confidence)")

print(f"\n✅ Model accuracy evaluation complete!")
print(f"📊 Your PCOS prediction model achieves {best_accuracy*100:.2f}% accuracy!")
