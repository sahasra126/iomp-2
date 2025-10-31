import pandas as pd
import numpy as np
import joblib

def load_model():
    """Load the trained model, scaler, and feature names"""
    try:
        model = joblib.load("pcos_model.pkl")
        scaler = joblib.load("pcos_scaler.pkl")
        feature_names = joblib.load("feature_names.pkl")
        return model, scaler, feature_names
    except FileNotFoundError as e:
        print(f"Error loading model files: {e}")
        print("Please run train_model.py first to train the model.")
        return None, None, None

def predict_pcos(patient_data, model, scaler, feature_names):
    """Make PCOS prediction for a patient"""
    # Ensure patient_data is in the correct format
    if isinstance(patient_data, dict):
        # Convert dictionary to array in correct order
        patient_array = np.array([[patient_data[feature] for feature in feature_names]])
    else:
        patient_array = np.array(patient_data).reshape(1, -1)
    
    # Scale the input data
    patient_scaled = scaler.transform(patient_array)
    
    # Make prediction
    prediction = model.predict(patient_scaled)[0]
    probability = model.predict_proba(patient_scaled)[0]
    
    return {
        'prediction': 'PCOS' if prediction == 1 else 'Healthy',
        'pcos_probability': probability[1],
        'healthy_probability': probability[0],
        'confidence': max(probability)
    }

def test_model_with_examples():
    """Test the model with some example patients"""
    print("🔄 Loading trained model...")
    model, scaler, feature_names = load_model()
    
    if model is None:
        return
    
    print(f"✅ Model loaded successfully!")
    print(f"Features: {feature_names}")
    
    # Test cases
    test_patients = [
        {
            'name': 'Healthy Patient',
            'data': {
                'Age': 25, 'BMI': 22, 'Insulin': 10, 'Testosterone': 30,
                'LH': 5, 'FSH': 7, 'Glucose': 85, 'Cholesterol': 170
            }
        },
        {
            'name': 'Likely PCOS Patient',
            'data': {
                'Age': 28, 'BMI': 30, 'Insulin': 20, 'Testosterone': 65,
                'LH': 15, 'FSH': 6, 'Glucose': 110, 'Cholesterol': 220
            }
        },
        {
            'name': 'Borderline Patient',
            'data': {
                'Age': 26, 'BMI': 26, 'Insulin': 15, 'Testosterone': 45,
                'LH': 8, 'FSH': 6, 'Glucose': 95, 'Cholesterol': 190
            }
        }
    ]
    
    print("\n🧪 Testing model with example patients:")
    print("-" * 60)
    
    for patient in test_patients:
        result = predict_pcos(patient['data'], model, scaler, feature_names)
        
        print(f"\n👤 {patient['name']}:")
        print(f"   Input: {patient['data']}")
        print(f"   Prediction: {result['prediction']}")
        print(f"   PCOS Probability: {result['pcos_probability']:.3f}")
        print(f"   Confidence: {result['confidence']:.3f}")

def interactive_prediction():
    """Interactive mode for making predictions"""
    print("\n🎯 Interactive PCOS Prediction")
    print("Enter patient data (or 'quit' to exit):")
    
    model, scaler, feature_names = load_model()
    if model is None:
        return
    
    while True:
        try:
            print(f"\nRequired features: {feature_names}")
            
            patient_data = {}
            for feature in feature_names:
                value = input(f"Enter {feature}: ")
                if value.lower() == 'quit':
                    return
                patient_data[feature] = float(value)
            
            result = predict_pcos(patient_data, model, scaler, feature_names)
            
            print(f"\n📊 Results:")
            print(f"   Prediction: {result['prediction']}")
            print(f"   PCOS Probability: {result['pcos_probability']:.3f}")
            print(f"   Confidence: {result['confidence']:.3f}")
            
            continue_prediction = input("\nMake another prediction? (y/n): ")
            if continue_prediction.lower() != 'y':
                break
                
        except ValueError:
            print("Please enter valid numeric values.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    # Run tests with example patients
    test_model_with_examples()
    
    # Option for interactive mode
    interactive = input("\n🤔 Would you like to try interactive prediction mode? (y/n): ")
    if interactive.lower() == 'y':
        interactive_prediction()
