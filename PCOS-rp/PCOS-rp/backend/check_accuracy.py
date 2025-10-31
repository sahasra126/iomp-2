import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, roc_auc_score, classification_report, 
                           confusion_matrix)

def generate_test_data(n_samples=1000):
    """Generate synthetic PCOS data for testing"""
    np.random.seed(42)
    
    n_healthy = int(n_samples * 0.7)
    n_pcos = n_samples - n_healthy
    
    # Healthy samples - lower risk values
    healthy_data = np.column_stack([
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
    
    # PCOS samples - higher risk values
    pcos_data = np.column_stack([
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
    
    X = np.vstack([healthy_data, pcos_data])
    y = np.concatenate([healthy_labels, pcos_labels])
    feature_names = ['Age', 'BMI', 'Insulin', 'Testosterone', 'LH', 'FSH', 'Glucose', 'Cholesterol']
    
    return X, y, feature_names

def train_and_evaluate():
    """Train models and show comprehensive accuracy metrics"""
    print("🚀 PCOS Model Accuracy Evaluation")
    print("=" * 50)
    
    # Generate data
    print("📊 Generating synthetic PCOS dataset...")
    X, y, feature_names = generate_test_data(1000)
    
    print(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features")
    print(f"PCOS cases: {np.sum(y)} ({np.mean(y)*100:.1f}%)")
    print(f"Healthy cases: {np.sum(y==0)} ({(1-np.mean(y))*100:.1f}%)")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Models to compare
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100)
    }
    
    results = {}
    
    print("\n🔄 Training and Evaluating Models...")
    print("-" * 50)
    
    for name, model in models.items():
        print(f"\n📈 {name}:")
        
        # Cross-validation scores
        cv_accuracy = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
        cv_precision = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='precision')
        cv_recall = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='recall')
        cv_f1 = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='f1')
        cv_roc_auc = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
        
        # Train model
        model.fit(X_train_scaled, y_train)
        
        # Test predictions
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        # Calculate test metrics
        test_accuracy = accuracy_score(y_test, y_pred)
        test_precision = precision_score(y_test, y_pred)
        test_recall = recall_score(y_test, y_pred)
        test_f1 = f1_score(y_test, y_pred)
        test_roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        # Store results
        results[name] = {
            'model': model,
            'cv_accuracy': cv_accuracy,
            'test_accuracy': test_accuracy,
            'test_precision': test_precision,
            'test_recall': test_recall,
            'test_f1': test_f1,
            'test_roc_auc': test_roc_auc,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
        
        # Print cross-validation results
        print(f"  📊 Cross-Validation (5-fold):")
        print(f"    Accuracy:  {cv_accuracy.mean():.3f} ± {cv_accuracy.std()*2:.3f}")
        print(f"    Precision: {cv_precision.mean():.3f} ± {cv_precision.std()*2:.3f}")
        print(f"    Recall:    {cv_recall.mean():.3f} ± {cv_recall.std()*2:.3f}")
        print(f"    F1-Score:  {cv_f1.mean():.3f} ± {cv_f1.std()*2:.3f}")
        print(f"    ROC-AUC:   {cv_roc_auc.mean():.3f} ± {cv_roc_auc.std()*2:.3f}")
        
        # Print test results
        print(f"  🎯 Test Set Performance:")
        print(f"    Accuracy:  {test_accuracy:.3f}")
        print(f"    Precision: {test_precision:.3f}")
        print(f"    Recall:    {test_recall:.3f}")
        print(f"    F1-Score:  {test_f1:.3f}")
        print(f"    ROC-AUC:   {test_roc_auc:.3f}")
    
    # Find best model
    best_model_name = max(results.keys(), key=lambda k: results[k]['test_roc_auc'])
    best_model = results[best_model_name]['model']
    
    print(f"\n🏆 BEST MODEL: {best_model_name}")
    print(f"🎯 Best Test ROC-AUC: {results[best_model_name]['test_roc_auc']:.3f}")
    
    # Detailed analysis of best model
    print(f"\n📋 Detailed Analysis - {best_model_name}:")
    best_pred = results[best_model_name]['predictions']
    
    # Classification report
    print("\n📊 Classification Report:")
    print(classification_report(y_test, best_pred, target_names=['Healthy', 'PCOS']))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, best_pred)
    print(f"\n🔢 Confusion Matrix:")
    print(f"                 Predicted")
    print(f"Actual    Healthy  PCOS")
    print(f"Healthy     {cm[0,0]:3d}    {cm[0,1]:3d}")
    print(f"PCOS        {cm[1,0]:3d}    {cm[1,1]:3d}")
    
    # Calculate additional metrics
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp)  # True negative rate
    sensitivity = tp / (tp + fn)  # Same as recall/true positive rate
    
    print(f"\n📈 Additional Metrics:")
    print(f"Sensitivity (True Positive Rate): {sensitivity:.3f}")
    print(f"Specificity (True Negative Rate): {specificity:.3f}")
    print(f"False Positive Rate: {fp/(fp+tn):.3f}")
    print(f"False Negative Rate: {fn/(fn+tp):.3f}")
    
    # Save the best model
    print(f"\n💾 Saving best model ({best_model_name})...")
    joblib.dump(best_model, "pcos_model.pkl")
    joblib.dump(scaler, "pcos_scaler.pkl")
    joblib.dump(feature_names, "feature_names.pkl")
    
    print("✅ Model files saved!")
    
    # Test with example cases
    print(f"\n🧪 Testing with Example Cases:")
    test_cases = [
        ("Low Risk", [25, 21, 8, 25, 4, 8, 80, 160]),
        ("Moderate Risk", [28, 26, 15, 45, 8, 6, 95, 190]),
        ("High Risk", [30, 32, 25, 70, 18, 5, 120, 240])
    ]
    
    for case_name, values in test_cases:
        sample = np.array([values])
        sample_scaled = scaler.transform(sample)
        pred = best_model.predict(sample_scaled)[0]
        prob = best_model.predict_proba(sample_scaled)[0, 1]
        print(f"  {case_name:12}: {'PCOS' if pred == 1 else 'Healthy':7} (probability: {prob:.3f})")
    
    return results, best_model_name

if __name__ == "__main__":
    results, best_model = train_and_evaluate()
    print(f"\n✅ Evaluation complete! Best model: {best_model}")
