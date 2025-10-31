import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

print("🔍 Checking saved model details...")

try:
    # Load the saved model
    model = joblib.load("pcos_model.pkl")
    scaler = joblib.load("pcos_scaler.pkl")
    feature_names = joblib.load("feature_names.pkl")
    
    print(f"✅ Model loaded successfully!")
    print(f"Model Type: {type(model).__name__}")
    print(f"Features: {feature_names}")
    print(f"Number of features: {len(feature_names)}")
    
    # Check model-specific details
    if isinstance(model, RandomForestClassifier):
        print(f"\n🌳 Random Forest Details:")
        print(f"  Number of trees: {model.n_estimators}")
        print(f"  Max depth: {model.max_depth}")
        print(f"  Random state: {model.random_state}")
        
        # Feature importance
        if hasattr(model, 'feature_importances_'):
            print(f"\n📊 Feature Importance:")
            for i, (feature, importance) in enumerate(zip(feature_names, model.feature_importances_)):
                print(f"  {i+1}. {feature}: {importance:.4f}")
    
    elif isinstance(model, LogisticRegression):
        print(f"\n📈 Logistic Regression Details:")
        print(f"  Max iterations: {model.max_iter}")
        print(f"  Random state: {model.random_state}")
        print(f"  Solver: {model.solver}")
        
        # Coefficients
        if hasattr(model, 'coef_'):
            print(f"\n📊 Feature Coefficients:")
            for i, (feature, coef) in enumerate(zip(feature_names, model.coef_[0])):
                print(f"  {i+1}. {feature}: {coef:.4f}")
    
    # Test with sample data
    print(f"\n🧪 Testing model with sample data...")
    sample_data = np.array([[25, 22, 10, 30, 5, 7, 85, 170]])  # Low risk profile
    sample_scaled = scaler.transform(sample_data)
    prediction = model.predict(sample_scaled)[0]
    probability = model.predict_proba(sample_scaled)[0]
    
    print(f"Sample prediction: {'PCOS' if prediction == 1 else 'Healthy'}")
    print(f"PCOS probability: {probability[1]:.3f}")
    print(f"Confidence: {max(probability):.3f}")
    
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    print("Please run train_model.py first to create the model files.")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\n✅ Model check complete!")
