import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

def generate_synthetic_pcos_data(n_samples=1000):
    """Generate more realistic synthetic PCOS data"""
    np.random.seed(42)
    
    # Generate features based on PCOS research
    # Features: Age, BMI, Insulin, Testosterone, LH, FSH, Glucose, Cholesterol
    
    # Non-PCOS samples (approximately 70% of data)
    n_healthy = int(n_samples * 0.7)
    healthy_data = np.column_stack([
        np.random.normal(28, 6, n_healthy),      # Age (20-40)
        np.random.normal(23, 3, n_healthy),      # BMI (normal range)
        np.random.normal(12, 4, n_healthy),      # Insulin
        np.random.normal(35, 10, n_healthy),     # Testosterone
        np.random.normal(6, 2, n_healthy),       # LH
        np.random.normal(7, 2, n_healthy),       # FSH
        np.random.normal(90, 10, n_healthy),     # Glucose
        np.random.normal(180, 30, n_healthy),    # Cholesterol
    ])
    healthy_labels = np.zeros(n_healthy)
    
    # PCOS samples (approximately 30% of data)
    n_pcos = n_samples - n_healthy
    pcos_data = np.column_stack([
        np.random.normal(26, 5, n_pcos),         # Age (slightly younger)
        np.random.normal(28, 5, n_pcos),         # BMI (higher)
        np.random.normal(18, 6, n_pcos),         # Insulin (higher)
        np.random.normal(55, 15, n_pcos),        # Testosterone (elevated)
        np.random.normal(12, 4, n_pcos),         # LH (elevated)
        np.random.normal(6, 2, n_pcos),          # FSH
        np.random.normal(105, 15, n_pcos),       # Glucose (higher)
        np.random.normal(200, 40, n_pcos),       # Cholesterol (higher)
    ])
    pcos_labels = np.ones(n_pcos)
    
    # Combine data
    X = np.vstack([healthy_data, pcos_data])
    y = np.concatenate([healthy_labels, pcos_labels])
    
    # Create feature names
    feature_names = ['Age', 'BMI', 'Insulin', 'Testosterone', 'LH', 'FSH', 'Glucose', 'Cholesterol']
    
    return X, y, feature_names

def train_and_evaluate_model():
    """Train and evaluate PCOS prediction model"""
    print("🔄 Generating synthetic PCOS dataset...")
    X, y, feature_names = generate_synthetic_pcos_data(1000)
    
    print(f"Dataset shape: {X.shape}")
    print(f"PCOS cases: {np.sum(y)} ({np.mean(y)*100:.1f}%)")
    print(f"Healthy cases: {np.sum(y==0)} ({(1-np.mean(y))*100:.1f}%)")
    
    # Create DataFrame for easier handling
    df = pd.DataFrame(X, columns=feature_names)
    df['PCOS'] = y
    
    # ---- Train/test split ----
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # ---- Feature scaling ----
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # ---- Model comparison ----
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100)
    }
    
    best_model = None
    best_score = 0
    model_results = {}
    
    print("\n🔄 Training and evaluating models...")
    
    for name, model in models.items():
        # Cross-validation
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
        
        # Train on full training set
        model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        model_results[name] = {
            'model': model,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'test_accuracy': accuracy,
            'test_roc_auc': roc_auc,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
        
        print(f"\n{name}:")
        print(f"  CV ROC-AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        print(f"  Test Accuracy: {accuracy:.3f}")
        print(f"  Test ROC-AUC: {roc_auc:.3f}")
        
        if roc_auc > best_score:
            best_score = roc_auc
            best_model = model
            best_model_name = name
    
    print(f"\n🏆 Best model: {best_model_name} (ROC-AUC: {best_score:.3f})")
    
    # ---- Detailed evaluation of best model ----
    print(f"\n📊 Detailed evaluation for {best_model_name}:")
    best_pred = model_results[best_model_name]['predictions']
    
    print("\nClassification Report:")
    print(classification_report(y_test, best_pred, target_names=['Healthy', 'PCOS']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, best_pred)
    print(cm)
    
    # ---- Feature importance (for Random Forest) ----
    if best_model_name == 'Random Forest':
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': best_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n📈 Feature Importance:")
        print(feature_importance)
    
    # ---- Save model and scaler ----
    print(f"\n💾 Saving {best_model_name} model and scaler...")
    joblib.dump(best_model, "pcos_model.pkl")
    joblib.dump(scaler, "pcos_scaler.pkl")
    
    # Save feature names for later use
    joblib.dump(feature_names, "feature_names.pkl")
    
    print("✅ Model, scaler, and feature names saved successfully!")
    
    return best_model, scaler, feature_names, model_results

if __name__ == "__main__":
    train_and_evaluate_model()
