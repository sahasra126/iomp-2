import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score
from sklearn.model_selection import learning_curve
import warnings
warnings.filterwarnings('ignore')

def evaluate_model_performance():
    """Comprehensive evaluation of the trained PCOS model"""
    try:
        # Load model artifacts
        model = joblib.load("pcos_model.pkl")
        scaler = joblib.load("pcos_scaler.pkl")
        feature_names = joblib.load("feature_names.pkl")
        print("✅ Model artifacts loaded successfully!")
    except FileNotFoundError as e:
        print(f"❌ Error loading model files: {e}")
        print("Please run train_model.py first.")
        return
    
    # Generate test data (same as training for consistency)
    print("\n🔄 Generating test dataset...")
    from train_model import generate_synthetic_pcos_data
    X, y, _ = generate_synthetic_pcos_data(500)  # Fresh test set
    
    # Scale the data
    X_scaled = scaler.transform(X)
    
    # Make predictions
    y_pred = model.predict(X_scaled)
    y_pred_proba = model.predict_proba(X_scaled)[:, 1]
    
    print("\n📊 Model Performance Summary")
    print("=" * 50)
    
    # Basic metrics
    accuracy = np.mean(y_pred == y)
    roc_auc = roc_auc_score(y, y_pred_proba)
    
    print(f"Test Accuracy: {accuracy:.3f}")
    print(f"ROC-AUC Score: {roc_auc:.3f}")
    
    # Classification report
    print("\n📋 Detailed Classification Report:")
    print(classification_report(y, y_pred, target_names=['Healthy', 'PCOS']))
    
    # Confusion matrix
    print("\n🔢 Confusion Matrix:")
    cm = confusion_matrix(y, y_pred)
    print(f"True Negatives (Healthy correctly identified): {cm[0,0]}")
    print(f"False Positives (Healthy misclassified as PCOS): {cm[0,1]}")
    print(f"False Negatives (PCOS misclassified as Healthy): {cm[1,0]}")
    print(f"True Positives (PCOS correctly identified): {cm[1,1]}")
    
    # Feature importance (if available)
    if hasattr(model, 'feature_importances_'):
        print("\n📈 Feature Importance:")
        feature_importance = pd.DataFrame({
            'Feature': feature_names,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        for _, row in feature_importance.iterrows():
            print(f"  {row['Feature']}: {row['Importance']:.3f}")
    
    elif hasattr(model, 'coef_'):
        print("\n📈 Feature Coefficients (Logistic Regression):")
        coefficients = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': model.coef_[0]
        }).sort_values('Coefficient', key=abs, ascending=False)
        
        for _, row in coefficients.iterrows():
            print(f"  {row['Feature']}: {row['Coefficient']:.3f}")
    
    # Prediction distribution
    print(f"\n🎯 Prediction Distribution:")
    print(f"Predicted Healthy: {np.sum(y_pred == 0)} ({np.mean(y_pred == 0)*100:.1f}%)")
    print(f"Predicted PCOS: {np.sum(y_pred == 1)} ({np.mean(y_pred == 1)*100:.1f}%)")
    print(f"Actual Healthy: {np.sum(y == 0)} ({np.mean(y == 0)*100:.1f}%)")
    print(f"Actual PCOS: {np.sum(y == 1)} ({np.mean(y == 1)*100:.1f}%)")
    
    # Probability distribution analysis
    print(f"\n📊 Probability Analysis:")
    healthy_probs = y_pred_proba[y == 0]
    pcos_probs = y_pred_proba[y == 1]
    
    print(f"Average PCOS probability for healthy patients: {healthy_probs.mean():.3f}")
    print(f"Average PCOS probability for PCOS patients: {pcos_probs.mean():.3f}")
    
    # High confidence predictions
    high_confidence_threshold = 0.8
    high_conf_mask = (y_pred_proba > high_confidence_threshold) | (y_pred_proba < (1 - high_confidence_threshold))
    print(f"\nHigh confidence predictions (>{high_confidence_threshold:.1f} or <{1-high_confidence_threshold:.1f}): {np.sum(high_conf_mask)} ({np.mean(high_conf_mask)*100:.1f}%)")
    
    return {
        'model': model,
        'scaler': scaler,
        'feature_names': feature_names,
        'test_accuracy': accuracy,
        'roc_auc': roc_auc,
        'predictions': y_pred,
        'probabilities': y_pred_proba,
        'true_labels': y
    }

def create_prediction_examples():
    """Create examples of different risk profiles"""
    examples = {
        'Low Risk Profile': {
            'Age': 25, 'BMI': 21, 'Insulin': 8, 'Testosterone': 25,
            'LH': 4, 'FSH': 8, 'Glucose': 80, 'Cholesterol': 160
        },
        'Moderate Risk Profile': {
            'Age': 28, 'BMI': 26, 'Insulin': 15, 'Testosterone': 45,
            'LH': 8, 'FSH': 6, 'Glucose': 95, 'Cholesterol': 190
        },
        'High Risk Profile': {
            'Age': 30, 'BMI': 32, 'Insulin': 25, 'Testosterone': 70,
            'LH': 18, 'FSH': 5, 'Glucose': 120, 'Cholesterol': 240
        }
    }
    
    try:
        model = joblib.load("pcos_model.pkl")
        scaler = joblib.load("pcos_scaler.pkl")
        feature_names = joblib.load("feature_names.pkl")
    except FileNotFoundError:
        print("Model files not found. Please train the model first.")
        return
    
    print("\n🎯 PCOS Risk Assessment Examples")
    print("=" * 50)
    
    for profile_name, data in examples.items():
        # Prepare data
        patient_array = np.array([[data[feature] for feature in feature_names]])
        patient_scaled = scaler.transform(patient_array)
        
        # Make prediction
        prediction = model.predict(patient_scaled)[0]
        probability = model.predict_proba(patient_scaled)[0, 1]
        
        print(f"\n👤 {profile_name}:")
        print(f"   Features: {data}")
        print(f"   PCOS Risk: {probability:.1%}")
        print(f"   Classification: {'PCOS' if prediction == 1 else 'Healthy'}")
        
        # Risk interpretation
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.7:
            risk_level = "Moderate"
        else:
            risk_level = "High"
        
        print(f"   Risk Level: {risk_level}")

if __name__ == "__main__":
    # Run comprehensive evaluation
    results = evaluate_model_performance()
    
    # Show risk assessment examples
    create_prediction_examples()
    
    print("\n✅ Model evaluation complete!")
    print("\nNext steps:")
    print("1. Review the performance metrics above")
    print("2. If accuracy is satisfactory, the model is ready for deployment")
    print("3. Consider collecting real PCOS data to improve the model")
    print("4. Update the frontend to use the new model features")
